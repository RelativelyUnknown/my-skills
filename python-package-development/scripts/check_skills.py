"""Check skills against the Agent Skills spec and this repo's token budgets."""

import argparse
import re
import string
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import yaml

SPEC_KEYS = frozenset({"name", "description", "license", "compatibility", "metadata", "allowed-tools"})
EXTRA_KEYS = frozenset({"argument-hint"})  # Claude Code and VS Code Copilot; outside the open spec
ARGUMENT_KEYS = frozenset({"python", "runner", "types", "layout", "backend", "rigor", "report"})
RESERVED_WORDS = ("claude", "anthropic")
NAME_MAX = 64
DESCRIPTION_SPEC_MAX = 1024
DESCRIPTION_BUDGET = 350
BODY_LINE_BUDGET = 200
REFERENCE_CONTENTS_LINES = 100
SCRIPT = "detect_project.py"
LINK = re.compile(r"\]\(([^)\s]+)\)")
NAME_CHARS = frozenset(string.ascii_lowercase + string.digits + "-")


@dataclass(frozen=True, slots=True)
class SkillReport:
    name: str
    errors: list[str]
    description_chars: int
    body_lines: int
    body_tokens: int


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


def _argument_hint_errors(hint: object) -> list[str]:
    if not isinstance(hint, str):
        return ["argument-hint must be a quoted string like \"[python=3.12 runner=uv]\""]
    keys = [token.partition("=")[0] for token in hint.strip("[] ").split()]
    return [
        f"argument-hint key '{key}' is not one of {sorted(ARGUMENT_KEYS)}"
        for key in keys
        if key not in ARGUMENT_KEYS
    ]


def _frontmatter_errors(fields: Mapping[str, object], folder: str) -> list[str]:
    errors = [
        f"unknown frontmatter key '{key}'" for key in fields if key not in SPEC_KEYS | EXTRA_KEYS
    ]
    name = fields.get("name")
    if isinstance(name, str) and name:
        errors.extend(_name_errors(name, folder))
    else:
        errors.append("name is missing")
    errors.extend(_description_errors(fields.get("description")))
    if "argument-hint" in fields:
        errors.extend(_argument_hint_errors(fields["argument-hint"]))
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


def _script_errors(skill: Path, body: str, canonical: Path) -> list[str]:
    if SCRIPT not in body:
        return []
    copy = skill / "scripts" / SCRIPT
    command = f"cp {canonical} {copy}"
    if not copy.is_file():
        return [f"scripts/{SCRIPT} is missing; run: {command}"]
    if copy.read_bytes() != canonical.read_bytes():
        return [f"scripts/{SCRIPT} differs from the canonical script; run: {command}"]
    return []


def check_skill(skill: Path, *, canonical: Path) -> SkillReport:
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

    messages = _frontmatter_errors(fields, skill.name)
    body_lines = len(body.splitlines())
    if body_lines > BODY_LINE_BUDGET:
        messages.append(f"{body_lines} body lines, over the budget of {BODY_LINE_BUDGET}")
    messages.extend(_link_errors(skill, body))
    messages.extend(_reference_errors(skill))
    if any(f"{folder}\\" in text for folder in ("scripts", "references", "assets")):
        messages.append("backslash path found; use forward slashes")
    messages.extend(_script_errors(skill, body, canonical))
    description = fields.get("description")
    return SkillReport(
        name=skill.name,
        errors=[f"{skill.name}: {message}" for message in messages],
        description_chars=len(description) if isinstance(description, str) else 0,
        body_lines=body_lines,
        body_tokens=len(body) // 4,
    )


def check_all(skills_root: Path, *, canonical: Path) -> list[SkillReport]:
    folders = sorted(p for p in skills_root.iterdir() if p.is_dir() and not p.name.startswith("."))
    return [check_skill(folder, canonical=canonical) for folder in folders]


def render_table(reports: Sequence[SkillReport]) -> str:
    rows = [f"{'skill':<34}{'description chars':>18}{'body lines':>12}{'body tokens':>13}"]
    rows.extend(
        f"{r.name:<34}{r.description_chars:>18}{r.body_lines:>12}{r.body_tokens:>13}" for r in reports
    )
    total = sum(r.description_chars for r in reports)
    rows.append(f"total: description chars {total} -> always-on description tokens {total // 4}")
    return "\n".join(rows) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills_dir", nargs="?", type=Path, default=Path("skills"))
    parser.add_argument("--canonical", type=Path, default=Path(__file__).parent / SCRIPT)
    args = parser.parse_args(argv)
    if not args.skills_dir.is_dir():
        sys.stderr.write(f"error: {args.skills_dir} is not a directory\n")
        return 2
    reports = check_all(args.skills_dir, canonical=args.canonical)
    sys.stdout.write(render_table(reports))
    errors = [error for report in reports for error in report.errors]
    for error in errors:
        sys.stderr.write(f"error: {error}\n")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
