"""Check skills against the Agent Skills spec and this repo's token budgets."""

import argparse
import importlib.util
import re
import string
import sys
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path

import yaml

SPEC_KEYS = frozenset({"name", "description", "license", "compatibility", "metadata", "allowed-tools"})
EXTRA_KEYS = frozenset({"argument-hint"})  # Claude Code and VS Code Copilot; outside the open spec
ARGUMENT_KEYS = frozenset({"python", "runner", "types", "layout", "backend", "rigor", "report", "kind"})
RESERVED_WORDS = ("claude", "anthropic")
NAME_MAX = 64
DESCRIPTION_SPEC_MAX = 1024
DESCRIPTION_BUDGET = 350
COMPATIBILITY_SPEC_MAX = 500
BODY_LINE_BUDGET = 200
REFERENCE_CONTENTS_LINES = 100
CHARS_PER_TOKEN = 2.8  # measured with the claude CLI's usage over 13 real skill bodies (range 2.6 to 3.0)
SCRIPT = "detect_project.py"
FACTS = "python-project-facts"  # the one skill that owns the script every other skill runs
SHARED = "shared"  # the bundle folder that holds the facts skill; installed with every other bundle
CORE = "core"  # skills every kind of Python work may name
LINK = re.compile(r"\]\(([^)\s]+)\)")
NAME_CHARS = frozenset(string.ascii_lowercase + string.digits + "-")


@dataclass(frozen=True, slots=True)
class SkillReport:
    name: str
    errors: list[str]
    description_chars: int
    body_lines: int
    body_tokens: int
    bundle: str = ""


def _split_frontmatter(text: str) -> tuple[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    return None


def _name_errors(name: str, folder: str) -> list[str]:
    errors = []
    if not set(name) <= NAME_CHARS:
        errors.append("name must use only lowercase letters, digits and hyphens")
    if name.startswith("-") or name.endswith("-"):
        errors.append("name must not start or end with a hyphen")
    if "--" in name:
        errors.append("name must not contain consecutive hyphens")
    if len(name) > NAME_MAX:
        errors.append(f"name is {len(name)} characters; the limit is {NAME_MAX} characters")
    errors.extend(f"name contains reserved word '{word}'" for word in RESERVED_WORDS if word in name)
    if name != folder:
        errors.append(f"name '{name}' must equal the folder name '{folder}'")
    return errors


def _description_errors(description: object) -> list[str]:
    if not isinstance(description, str) or not description.strip():
        return ["description is missing"]
    errors = []
    if len(description) > DESCRIPTION_SPEC_MAX:
        errors.append(
            f"description is {len(description)} characters, over the spec limit of {DESCRIPTION_SPEC_MAX}"
        )
    if len(description) > DESCRIPTION_BUDGET:
        errors.append(
            f"description is {len(description)} characters, over the {DESCRIPTION_BUDGET}-character budget"
        )
    return errors


def _argument_hint_errors(hint: object, allowed: frozenset[str] | None) -> list[str]:
    if not isinstance(hint, str):
        return ["argument-hint must be a quoted string like \"[python=3.12 runner=uv]\""]
    keys = [token.partition("=")[0] for token in hint.strip("[] ").split()]
    if allowed is None:
        return []
    return [
        f"argument-hint key '{key}' is not one of {sorted(allowed)}" for key in keys if key not in allowed
    ]


def _frontmatter_errors(
    fields: Mapping[str, object], folder: str, argument_keys: frozenset[str] | None
) -> list[str]:
    errors = [
        f"unknown frontmatter key '{key}'" for key in fields if key not in SPEC_KEYS | EXTRA_KEYS
    ]
    name = fields.get("name")
    if isinstance(name, str) and name:
        errors.extend(_name_errors(name, folder))
    else:
        errors.append("name is missing")
    errors.extend(_description_errors(fields.get("description")))
    compatibility = fields.get("compatibility")
    if isinstance(compatibility, str) and len(compatibility) > COMPATIBILITY_SPEC_MAX:
        errors.append(
            f"compatibility is {len(compatibility)} characters, over the spec limit of {COMPATIBILITY_SPEC_MAX}"
        )
    if "argument-hint" in fields:
        errors.extend(_argument_hint_errors(fields["argument-hint"], argument_keys))
    return errors


def _is_local(target: str) -> bool:
    return "://" not in target and not target.startswith(("#", "mailto:"))


def _link_errors(skill: Path, body: str) -> list[str]:
    errors = []
    for raw in LINK.findall(body):
        if not _is_local(raw):
            continue
        target = raw.partition("#")[0]
        if not target:
            continue
        if len(Path(target).parts) > 2:
            errors.append(f"{target} is nested deeper than one folder")
        elif not (skill / target).is_file():
            errors.append(f"{target} does not exist")
    return errors


def _reference_errors(skill: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(skill.rglob("*.md")):
        if path.name == "SKILL.md":
            continue
        rel = path.relative_to(skill).as_posix()
        text = path.read_text()
        lines = text.splitlines()
        errors.extend(
            f"{rel} links to another file ({target})"
            for target in LINK.findall(text)
            if _is_local(target) and target.partition("#")[0]
        )
        has_contents = any(
            line.strip().lstrip("#").strip().lower() == "contents" for line in lines[:20]
        )
        if len(lines) > REFERENCE_CONTENTS_LINES and not has_contents:
            errors.append(f"{rel} has {len(lines)} lines and no Contents list")
    return errors


def _dependency_errors(skill: Path, fields: Mapping[str, object], body: str) -> list[str]:
    """Skills share one detection script, owned by the facts skill; they depend on it, never copy it."""
    script = skill / "scripts" / SCRIPT
    if skill.name == FACTS:
        return [] if script.is_file() else [f"scripts/{SCRIPT} is missing; this skill owns it"]
    errors = []
    shared = f"{FACTS}/scripts/{SCRIPT}"
    if script.exists():
        errors.append(f"scripts/{SCRIPT} is a private copy; run {shared} instead")
    runs_script = SCRIPT in body
    if runs_script and shared not in body:
        errors.append(f"{SCRIPT} must be run through the {FACTS} skill ({shared})")
    if (runs_script or FACTS in body) and FACTS not in str(fields.get("compatibility", "")):
        errors.append(f"uses {FACTS} but its compatibility field does not say so")
    return errors


def check_skill(skill: Path, *, argument_keys: frozenset[str] | None = ARGUMENT_KEYS) -> SkillReport:
    skill_md = skill / "SKILL.md"
    if not skill_md.is_file():
        return SkillReport(skill.name, [f"{skill.name}: SKILL.md is missing"], 0, 0, 0)
    text = skill_md.read_text()
    parts = _split_frontmatter(text)
    if parts is None:
        message = "frontmatter must start on the first line with --- and end with ---"
        return SkillReport(skill.name, [f"{skill.name}: {message}"], 0, 0, 0)
    raw, body = parts
    try:
        fields = yaml.safe_load(raw)
    except yaml.YAMLError as error:
        message = f"frontmatter is not valid YAML: {' '.join(str(error).split())}"
        return SkillReport(skill.name, [f"{skill.name}: {message}"], 0, 0, 0)
    if not isinstance(fields, dict):
        return SkillReport(skill.name, [f"{skill.name}: frontmatter must be a mapping"], 0, 0, 0)

    messages = _frontmatter_errors(fields, skill.name, argument_keys)
    body_lines = len(body.splitlines())
    if body_lines > BODY_LINE_BUDGET:
        messages.append(f"{body_lines} body lines, over the budget of {BODY_LINE_BUDGET}")
    messages.extend(_link_errors(skill, body))
    messages.extend(_reference_errors(skill))
    if any(f"{folder}\\" in text for folder in ("scripts", "references", "assets")):
        messages.append("backslash path found; use forward slashes")
    messages.extend(_dependency_errors(skill, fields, body))
    description = fields.get("description")
    return SkillReport(
        name=skill.name,
        errors=[f"{skill.name}: {message}" for message in messages],
        description_chars=len(description) if isinstance(description, str) else 0,
        body_lines=body_lines,
        body_tokens=round(len(body) / CHARS_PER_TOKEN),
    )


def _skill_folders(skills_root: Path) -> list[Path]:
    return sorted(p for p in skills_root.iterdir() if p.is_dir() and not p.name.startswith("."))


def check_all(
    skills_root: Path, *, argument_keys: frozenset[str] | None = ARGUMENT_KEYS
) -> list[SkillReport]:
    return [check_skill(folder, argument_keys=argument_keys) for folder in _skill_folders(skills_root)]


def find_bundles(root: Path) -> dict[str, Path]:
    """Bundle name -> its skills folder, for a family root laid out as <bundle>/skills/<skill>."""
    return {
        folder.name: folder / "skills"
        for folder in sorted(root.iterdir())
        if folder.is_dir() and not folder.name.startswith(".") and (folder / "skills").is_dir()
    }


def is_family(root: Path) -> bool:
    return bool(find_bundles(root)) and not any((c / "SKILL.md").is_file() for c in root.iterdir() if c.is_dir())


def _skill_text(skill: Path) -> str:
    return "\n".join(path.read_text() for path in sorted(skill.rglob("*.md")) if "evals" not in path.parts)


def _mentions(text: str, name: str) -> bool:
    return re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", text) is not None


def _layout_errors(found: Mapping[str, Sequence[str]], bundles: Mapping[str, tuple[str, ...]]) -> list[str]:
    errors = []
    for bundle, names in found.items():
        if bundle == SHARED:
            continue
        if bundle not in bundles:
            errors.append(f"bundle folder '{bundle}' is not in the bundle map of {FACTS}")
            continue
        errors.extend(
            f"{bundle}/{name} is not in the bundle map for {bundle}" for name in names if name not in bundles[bundle]
        )
    for bundle, expected in bundles.items():
        have = found.get(bundle, ())
        errors.extend(f"{bundle}/{name} is in the bundle map but missing" for name in expected if name not in have)
    return errors


def _family_errors(
    found: Mapping[str, Sequence[str]], texts: Mapping[tuple[str, str], str], bundles: Mapping[str, tuple[str, ...]] | None
) -> list[str]:
    errors: list[str] = []
    owners: dict[str, list[str]] = defaultdict(list)
    for bundle, names in found.items():
        for name in names:
            owners[name].append(bundle)
    if FACTS not in found.get(SHARED, ()):
        errors.append(f"{SHARED}/{FACTS} is missing; every other skill depends on it")
    errors.extend(
        f"{name} is in more than one bundle ({', '.join(where)})" for name, where in owners.items() if len(where) > 1
    )
    for (bundle, skill), text in texts.items():
        allowed = {bundle, CORE, SHARED}
        errors.extend(
            f"{skill}: names {other}, a skill of the {where[0]} bundle; "
            f"say 'the {where[0]} bundle, if installed' instead"
            for other, where in owners.items()
            if other != skill and not allowed.intersection(where) and _mentions(text, other)
        )
    if bundles is not None:
        errors.extend(_layout_errors(found, bundles))
    return errors


def load_bundle_map(root: Path) -> Mapping[str, tuple[str, ...]] | None:
    """The BUNDLES map that the facts skill's script carries, or None when it cannot be loaded."""
    script = root / SHARED / "skills" / FACTS / "scripts" / SCRIPT
    if not script.is_file():
        return None
    spec = importlib.util.spec_from_file_location("_bundle_map_source", script)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    bundles = getattr(module, "BUNDLES", None)
    return bundles if isinstance(bundles, dict) else None


def check_family(
    root: Path,
    *,
    argument_keys: frozenset[str] | None = ARGUMENT_KEYS,
    bundles: Mapping[str, tuple[str, ...]] | None = None,
) -> tuple[list[SkillReport], list[str]]:
    """Check every skill of every bundle, then the rules that span bundles."""
    reports: list[SkillReport] = []
    found: dict[str, list[str]] = {}
    texts: dict[tuple[str, str], str] = {}
    for bundle, skills_root in find_bundles(root).items():
        found[bundle] = []
        for folder in _skill_folders(skills_root):
            reports.append(replace(check_skill(folder, argument_keys=argument_keys), bundle=bundle))
            found[bundle].append(folder.name)
            texts[(bundle, folder.name)] = _skill_text(folder)
    return reports, _family_errors(found, texts, bundles)


def render_table(reports: Sequence[SkillReport]) -> str:
    labels = [f"{r.bundle}/{r.name}" if r.bundle else r.name for r in reports]
    width = max([34, *(len(label) + 2 for label in labels)])
    rows = [f"{'skill':<{width}}{'description chars':>18}{'body lines':>12}{'body tokens':>13}"]
    rows.extend(
        f"{label:<{width}}{r.description_chars:>18}{r.body_lines:>12}{r.body_tokens:>13}"
        for label, r in zip(labels, reports, strict=True)
    )
    total = sum(r.description_chars for r in reports)
    rows.append(f"total: description chars {total} -> always-on description tokens {round(total / CHARS_PER_TOKEN)}")
    return "\n".join(rows) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skills_dir", nargs="?", type=Path, default=Path("skills"),
        help="a folder of skills, or a family root laid out as <bundle>/skills/<skill>",
    )
    parser.add_argument(
        "--argument-keys",
        help="comma-separated keys allowed in argument-hint (default: this repo's Python set; "
        "an empty value accepts any key)",
    )
    args = parser.parse_args(argv)
    if not args.skills_dir.is_dir():
        sys.stderr.write(f"error: {args.skills_dir} is not a directory\n")
        return 2
    keys: frozenset[str] | None = ARGUMENT_KEYS
    if args.argument_keys is not None:
        keys = frozenset(k for k in args.argument_keys.split(",") if k) or None
    family_errors: list[str] = []
    if is_family(args.skills_dir):
        reports, family_errors = check_family(
            args.skills_dir, argument_keys=keys, bundles=load_bundle_map(args.skills_dir)
        )
    else:
        reports = check_all(args.skills_dir, argument_keys=keys)
    sys.stdout.write(render_table(reports))
    errors = [*(error for report in reports for error in report.errors), *family_errors]
    for error in errors:
        sys.stderr.write(f"error: {error}\n")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
