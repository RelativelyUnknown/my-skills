import json
from collections.abc import Mapping
from pathlib import Path

import pytest
from check_skills import (
    ARGUMENT_KEYS,
    FACTS,
    SHARED,
    check_all,
    check_family,
    check_skill,
    find_bundles,
    find_notices,
    main,
    render_table,
)

DESCRIPTION = "Writes pytest tests. Use when adding or fixing tests."
COMPAT = "Needs the python-project-facts skill installed in the same folder."
RUN = "Run `../python-project-facts/scripts/detect_project.py` first."


def make_skill(
    root: Path,
    name: str = "demo-skill",
    *,
    frontmatter: Mapping[str, object] | None = None,
    body: str = f"# Demo\n\n{RUN}\n",
    files: Mapping[str, str] | None = None,
) -> Path:
    fields = (
        {"name": name, "description": DESCRIPTION, "compatibility": COMPAT}
        if frontmatter is None
        else frontmatter
    )
    header = "".join(f"{key}: {json.dumps(value)}\n" for key, value in fields.items())
    skill = root / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(f"---\n{header}---\n{body}")
    for rel, content in (files or {}).items():
        path = skill / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return skill


def errors_for(skill: Path) -> list[str]:
    return check_skill(skill).errors


def test_valid_skill_has_no_errors(tmp_path: Path) -> None:
    assert errors_for(make_skill(tmp_path / "skills")) == []


def test_missing_skill_md_is_an_error(tmp_path: Path) -> None:
    empty = tmp_path / "skills" / "empty-skill"
    empty.mkdir(parents=True)

    assert errors_for(empty) == ["empty-skill: SKILL.md is missing"]


def test_frontmatter_must_start_on_the_first_line(tmp_path: Path) -> None:
    skill = make_skill(tmp_path / "skills")
    (skill / "SKILL.md").write_text("\n---\nname: demo-skill\n---\nbody\n")

    assert any("first line" in e for e in errors_for(skill))


def test_invalid_yaml_frontmatter_is_an_error(tmp_path: Path) -> None:
    skill = make_skill(tmp_path / "skills")
    (skill / "SKILL.md").write_text("---\nname: [unclosed\n---\nbody\n")

    assert any("not valid YAML" in e for e in errors_for(skill))


def test_keys_outside_the_spec_are_rejected(tmp_path: Path) -> None:
    skill = make_skill(
        tmp_path / "skills",
        frontmatter={"name": "demo-skill", "description": DESCRIPTION, "context": "fork"},
    )

    assert any("unknown frontmatter key 'context'" in e for e in errors_for(skill))


def test_argument_hint_with_known_keys_is_allowed(tmp_path: Path) -> None:
    hint = "[python=3.12 runner=uv rigor=full]"
    skill = make_skill(
        tmp_path / "skills",
        frontmatter={"name": "demo-skill", "description": DESCRIPTION, "compatibility": COMPAT, "argument-hint": hint},
    )

    assert errors_for(skill) == []


def test_argument_hint_with_unknown_key_is_an_error(tmp_path: Path) -> None:
    skill = make_skill(
        tmp_path / "skills",
        frontmatter={
            "name": "demo-skill",
            "description": DESCRIPTION,
            "argument-hint": "[python=3.12 colour=red]",
        },
    )

    assert any("argument-hint key 'colour'" in e for e in errors_for(skill))


def test_argument_keys_match_the_documented_set() -> None:
    assert {"python", "runner", "types", "layout", "backend", "rigor", "report", "kind"} == ARGUMENT_KEYS


@pytest.mark.parametrize(
    ("name", "problem"),
    [
        ("Demo-Skill", "lowercase"),
        ("demo--skill", "consecutive hyphens"),
        ("-demo", "start or end with a hyphen"),
        ("demo-", "start or end with a hyphen"),
        ("claude-helper", "reserved word"),
        ("anthropic-tools", "reserved word"),
        ("a" * 65, "64 characters"),
    ],
)
def test_invalid_names_are_rejected(
    tmp_path: Path, name: str, problem: str
) -> None:
    skill = make_skill(tmp_path / "skills", name)

    assert any(problem in e for e in errors_for(skill))


def test_name_must_equal_the_folder_name(tmp_path: Path) -> None:
    skill = make_skill(
        tmp_path / "skills",
        "demo-skill",
        frontmatter={"name": "other-name", "description": DESCRIPTION},
    )

    assert any("must equal the folder name" in e for e in errors_for(skill))


@pytest.mark.parametrize(
    ("description", "problem"),
    [
        (None, "description is missing"),
        ("", "description is missing"),
        ("x" * 351, "over the 350-character budget"),
    ],
)
def test_description_rules(
    tmp_path: Path, description: str | None, problem: str
) -> None:
    fields: dict[str, object] = {"name": "demo-skill"}
    if description is not None:
        fields["description"] = description
    skill = make_skill(tmp_path / "skills", frontmatter=fields)

    assert any(problem in e for e in errors_for(skill))


def test_description_over_the_spec_limit_is_reported_as_spec_violation(
    tmp_path: Path
) -> None:
    skill = make_skill(
        tmp_path / "skills", frontmatter={"name": "demo-skill", "description": "x" * 1025}
    )

    assert any("over the spec limit of 1024" in e for e in errors_for(skill))


def test_body_over_the_line_budget_is_an_error(tmp_path: Path) -> None:
    body = "Run `../python-project-facts/scripts/detect_project.py`.\n" + "line\n" * 200
    skill = make_skill(tmp_path / "skills", body=body)

    assert any("201 body lines" in e and "budget of 200" in e for e in errors_for(skill))


def test_link_to_missing_file_is_an_error(tmp_path: Path) -> None:
    body = "Run `../python-project-facts/scripts/detect_project.py`. See [more](references/more.md).\n"
    skill = make_skill(tmp_path / "skills", body=body)

    assert any("references/more.md does not exist" in e for e in errors_for(skill))


def test_link_to_existing_file_one_level_down_is_fine(tmp_path: Path) -> None:
    body = "Run `../python-project-facts/scripts/detect_project.py`. See [more](references/more.md).\n"
    skill = make_skill(tmp_path / "skills", body=body, files={"references/more.md": "# More\n"})

    assert errors_for(skill) == []


def test_link_nested_deeper_than_one_folder_is_an_error(tmp_path: Path) -> None:
    body = "Run `../python-project-facts/scripts/detect_project.py`. See [deep](references/a/b.md).\n"
    skill = make_skill(tmp_path / "skills", body=body, files={"references/a/b.md": "# B\n"})

    assert any("references/a/b.md is nested" in e for e in errors_for(skill))


def test_reference_file_linking_to_another_reference_is_an_error(
    tmp_path: Path
) -> None:
    body = "Run `../python-project-facts/scripts/detect_project.py`. See [a](references/a.md).\n"
    files = {"references/a.md": "See [b](b.md).\n", "references/b.md": "# B\n"}
    skill = make_skill(tmp_path / "skills", body=body, files=files)

    assert any("references/a.md links to another file" in e for e in errors_for(skill))


def test_web_links_and_anchors_are_not_checked_as_files(tmp_path: Path) -> None:
    body = "Run `../python-project-facts/scripts/detect_project.py`. [docs](https://example.com/x) [top](#top)\n"
    skill = make_skill(tmp_path / "skills", body=body)

    assert errors_for(skill) == []


def test_long_reference_needs_a_contents_list(tmp_path: Path) -> None:
    body = "Run `../python-project-facts/scripts/detect_project.py`. See [a](references/a.md).\n"
    skill = make_skill(
        tmp_path / "skills", body=body, files={"references/a.md": "# A\n" + "text\n" * 101}
    )

    assert any("references/a.md has 102 lines and no Contents" in e for e in errors_for(skill))


def test_long_reference_with_contents_is_fine(tmp_path: Path) -> None:
    body = "Run `../python-project-facts/scripts/detect_project.py`. See [a](references/a.md).\n"
    content = "# A\n\n## Contents\n\n- one\n" + "text\n" * 101
    skill = make_skill(tmp_path / "skills", body=body, files={"references/a.md": content})

    assert errors_for(skill) == []


def test_windows_style_paths_are_an_error(tmp_path: Path) -> None:
    body = "Run `scripts\\detect_project.py`.\n"
    skill = make_skill(tmp_path / "skills", body=body)

    assert any("backslash path" in e for e in errors_for(skill))


def test_skill_that_runs_the_shared_script_must_declare_the_dependency(tmp_path: Path) -> None:
    fields = {"name": "demo-skill", "description": DESCRIPTION}
    skill = make_skill(tmp_path / "skills", frontmatter=fields)

    assert any(FACTS in e and "compatibility" in e for e in errors_for(skill))


def test_declared_dependency_is_clean(tmp_path: Path) -> None:
    assert errors_for(make_skill(tmp_path / "skills")) == []


def test_script_must_be_run_through_the_facts_skill(tmp_path: Path) -> None:
    skill = make_skill(tmp_path / "skills", body="Run `scripts/detect_project.py` first.\n")

    assert any("must be run through" in e and FACTS in e for e in errors_for(skill))


def test_skill_must_not_carry_its_own_copy_of_the_script(tmp_path: Path) -> None:
    skill = make_skill(tmp_path / "skills", files={"scripts/detect_project.py": "# copy\n"})

    assert any("private copy" in e and FACTS in e for e in errors_for(skill))


def test_skill_that_never_mentions_the_script_needs_no_declaration(tmp_path: Path) -> None:
    fields = {"name": "demo-skill", "description": DESCRIPTION}
    skill = make_skill(tmp_path / "skills", frontmatter=fields, body="# Demo\n")

    assert errors_for(skill) == []


def test_facts_skill_needs_its_own_script(tmp_path: Path) -> None:
    fields = {"name": FACTS, "description": DESCRIPTION}
    skill = make_skill(tmp_path / "skills", FACTS, frontmatter=fields, body="# Facts\n")

    assert any("scripts/detect_project.py is missing" in e for e in errors_for(skill))


def test_facts_skill_with_its_script_is_clean(tmp_path: Path) -> None:
    fields = {"name": FACTS, "description": DESCRIPTION}
    skill = make_skill(
        tmp_path / "skills", FACTS, frontmatter=fields, body="# Facts\n",
        files={"scripts/detect_project.py": "# the one copy\n"},
    )

    assert errors_for(skill) == []


def test_compatibility_over_the_spec_limit_is_an_error(tmp_path: Path) -> None:
    fields = {"name": "demo-skill", "description": DESCRIPTION, "compatibility": COMPAT + "x" * 500}
    skill = make_skill(tmp_path / "skills", frontmatter=fields)

    assert any("compatibility is" in e and "500" in e for e in errors_for(skill))


def test_check_all_reads_every_skill_folder_and_ignores_files(
    tmp_path: Path
) -> None:
    skills = tmp_path / "skills"
    make_skill(skills, "first-skill")
    make_skill(skills, "second-skill")
    (skills / "README.md").write_text("not a skill")

    reports = check_all(skills)

    assert [r.name for r in reports] == ["first-skill", "second-skill"]


def test_token_estimate_uses_the_measured_chars_per_token(tmp_path: Path) -> None:
    # 2.8 chars per token: measured with the claude CLI's usage over 13 real skill bodies.
    body = "x" * 280
    skill = make_skill(tmp_path / "skills", "sized-skill", body=body)

    assert check_skill(skill).body_tokens == 100


def test_table_lists_each_skill_and_the_always_on_total(tmp_path: Path) -> None:
    skills = tmp_path / "skills"
    make_skill(skills, "first-skill")
    make_skill(skills, "second-skill")

    table = render_table(check_all(skills))

    assert "first-skill" in table
    assert "second-skill" in table
    assert f"description chars {2 * len(DESCRIPTION)}" in table
    assert "always-on description tokens" in table


def test_main_returns_zero_for_valid_skills(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_skill(tmp_path / "skills")

    assert main([str(tmp_path / "skills")]) == 0

    assert "demo-skill" in capsys.readouterr().out


def test_main_returns_one_and_prints_errors_for_invalid_skills(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_skill(tmp_path / "skills", frontmatter={"name": "demo-skill", "description": ""})

    assert main([str(tmp_path / "skills")]) == 1

    assert "description is missing" in capsys.readouterr().err


def test_main_returns_two_when_the_skills_folder_is_missing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "nope"

    assert main([str(missing)]) == 2

    assert f"error: {missing} is not a directory" in capsys.readouterr().err


def test_argument_keys_can_be_configured(tmp_path: Path) -> None:
    fields = {"name": "demo-skill", "description": DESCRIPTION, "compatibility": COMPAT, "argument-hint": "[scene=a fps=25]"}
    skill = make_skill(tmp_path / "skills", frontmatter=fields)

    assert check_skill(skill, argument_keys=frozenset({"scene", "fps"})).errors == []
    assert check_skill(skill, argument_keys=None).errors == []
    assert any("argument-hint key 'scene'" in e for e in errors_for(skill))


def test_main_argument_keys_option(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    fields = {"name": "demo-skill", "description": DESCRIPTION, "compatibility": COMPAT, "argument-hint": "[scene=a]"}
    make_skill(tmp_path / "skills", frontmatter=fields)
    base = [str(tmp_path / "skills")]

    assert main(base) == 1
    assert main([*base, "--argument-keys", "scene"]) == 0
    assert main([*base, "--argument-keys", ""]) == 0
    capsys.readouterr()


# ---- bundles: <family>/<bundle>/skills/<skill> ----------------------------------------------

STUB_SCRIPT = 'BUNDLES = {"core": ("base-skill",), "library": ("lib-skill",), "extra": ()}\n'


def make_family(
    root: Path,
    layout: Mapping[str, list[str]],
    *,
    bodies: Mapping[str, str] | None = None,
) -> Path:
    """layout maps bundle -> skill names; the shared bundle always holds the facts skill."""
    full = {SHARED: [FACTS], **layout}
    for bundle, names in full.items():
        for name in names:
            extra = {"scripts/detect_project.py": STUB_SCRIPT} if name == FACTS else None
            make_skill(
                root / bundle / "skills",
                name,
                body=(bodies or {}).get(name, f"# {name}\n\n{RUN}\n"),
                files=extra,
            )
    return root


BUNDLE_MAP = {"core": ("base-skill",), "library": ("lib-skill",), "extra": ()}


def family_errors(root: Path, bundles: Mapping[str, tuple[str, ...]] | None = None) -> list[str]:
    reports, family = check_family(root, bundles=BUNDLE_MAP if bundles is None else bundles)
    return [*(e for r in reports for e in r.errors), *family]


def test_find_bundles_maps_each_folder_that_holds_skills(tmp_path: Path) -> None:
    make_family(tmp_path / "fam", {"core": ["base-skill"], "library": ["lib-skill"]})
    (tmp_path / "fam" / "scripts").mkdir()

    found = find_bundles(tmp_path / "fam")

    assert sorted(found) == ["core", "library", SHARED]
    assert found["core"] == tmp_path / "fam" / "core" / "skills"


def test_valid_family_has_no_errors(tmp_path: Path) -> None:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"], "library": ["lib-skill"]})

    assert family_errors(root) == []


def test_reports_carry_their_bundle(tmp_path: Path) -> None:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"], "library": ["lib-skill"]})

    reports, _ = check_family(root, bundles=BUNDLE_MAP)

    assert {(r.bundle, r.name) for r in reports} == {
        (SHARED, FACTS), ("core", "base-skill"), ("library", "lib-skill"),
    }


def test_core_skill_must_not_name_a_skill_of_another_bundle(tmp_path: Path) -> None:
    root = make_family(
        tmp_path / "fam",
        {"core": ["base-skill"], "library": ["lib-skill"]},
        bodies={"base-skill": f"# Base\n\n{RUN}\nSee lib-skill for packaging.\n"},
    )

    errors = family_errors(root)

    assert any("base-skill" in e and "lib-skill" in e and "library bundle" in e for e in errors)


def test_a_reference_file_counts_too(tmp_path: Path) -> None:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"], "library": ["lib-skill"]})
    (root / "core" / "skills" / "base-skill" / "references").mkdir()
    (root / "core" / "skills" / "base-skill" / "references" / "a.md").write_text("Use `lib-skill`.\n")

    assert any("lib-skill" in e for e in family_errors(root))


def test_core_and_shared_and_own_bundle_may_be_named(tmp_path: Path) -> None:
    root = make_family(
        tmp_path / "fam",
        {"core": ["base-skill"], "library": ["lib-skill", "lib-two"]},
        bodies={"lib-skill": f"# Lib\n\n{RUN}\nSee base-skill, {FACTS} and lib-two.\n"},
    )

    assert family_errors(root, {**BUNDLE_MAP, "library": ("lib-skill", "lib-two")}) == []


def test_a_longer_name_that_contains_a_skill_name_is_not_a_mention(tmp_path: Path) -> None:
    root = make_family(
        tmp_path / "fam",
        {"core": ["base-skill"], "library": ["lib-skill"]},
        bodies={"base-skill": f"# Base\n\n{RUN}\nSee not-lib-skill-at-all.\n"},
    )

    assert family_errors(root) == []


def test_duplicate_skill_names_across_bundles_are_an_error(tmp_path: Path) -> None:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"], "library": ["lib-skill", "base-skill"]})

    assert any("base-skill" in e and "more than one bundle" in e for e in family_errors(root))


def test_layout_must_match_the_bundle_map(tmp_path: Path) -> None:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"], "library": ["lib-skill", "stray-skill"]})

    errors = family_errors(root)

    assert any("stray-skill" in e and "library" in e and "not in the bundle map" in e for e in errors)


def test_a_mapped_skill_that_is_missing_is_an_error(tmp_path: Path) -> None:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"]})

    assert any("lib-skill" in e and "library" in e and "missing" in e for e in family_errors(root))


def test_a_planned_bundle_with_no_skills_needs_no_folder(tmp_path: Path) -> None:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"], "library": ["lib-skill"]})

    assert not (root / "extra").exists()
    assert family_errors(root) == []


def test_a_bundle_folder_that_is_not_in_the_map_is_an_error(tmp_path: Path) -> None:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"], "library": ["lib-skill"], "other": ["x-skill"]})

    assert any("other" in e and "bundle map" in e for e in family_errors(root))


def test_family_needs_the_facts_skill_in_the_shared_bundle(tmp_path: Path) -> None:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"], "library": ["lib-skill"]})
    for path in sorted((root / SHARED).rglob("*"), reverse=True):
        path.unlink() if path.is_file() else path.rmdir()
    (root / SHARED).rmdir()

    assert any(FACTS in e and SHARED in e for e in family_errors(root))


def test_main_checks_a_family_root_and_prints_bundle_names(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"], "library": ["lib-skill"]})

    assert main([str(root)]) == 0

    out = capsys.readouterr().out
    assert "core/base-skill" in out
    assert f"{SHARED}/{FACTS}" in out


def test_main_reports_family_errors_and_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"]})

    assert main([str(root)]) == 1

    assert "lib-skill" in capsys.readouterr().err


# ---- folded-in skills: licence, source and notices ------------------------------------------

SOURCE = (
    "# Source\n\n- Upstream: https://github.com/example/agents\n"
    "- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d\n- Changed: shortened, rules deduplicated.\n"
)
MIT_FIELDS = {"name": "folded-skill", "description": DESCRIPTION, "compatibility": COMPAT, "license": "MIT"}


def make_folded(root: Path, *, extra: Mapping[str, str] | None = None, fields: Mapping[str, object] | None = None) -> Path:
    files = {"SOURCE.md": SOURCE, "LICENSE": "MIT License\nCopyright (c) Example\n", **(extra or {})}
    return make_skill(root, "folded-skill", frontmatter=MIT_FIELDS if fields is None else fields, files=files)


def test_folded_skill_with_licence_source_and_license_field_is_clean(tmp_path: Path) -> None:
    assert errors_for(make_folded(tmp_path / "skills")) == []


def test_source_md_without_a_licence_file_is_an_error(tmp_path: Path) -> None:
    skill = make_folded(tmp_path / "skills")
    (skill / "LICENSE").unlink()

    assert any("SOURCE.md" in e and "licence file" in e for e in errors_for(skill))


@pytest.mark.parametrize("licence", ["LICENSE.wshobson", "LICENSE-MIT", "LICENCE", "LICENSE.md"])
def test_licence_file_name_variants_are_accepted(tmp_path: Path, licence: str) -> None:
    skill = make_folded(tmp_path / "skills")
    (skill / "LICENSE").rename(skill / licence)

    assert errors_for(skill) == []


def test_source_md_must_name_an_upstream_url(tmp_path: Path) -> None:
    skill = make_folded(tmp_path / "skills", extra={"SOURCE.md": "- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d\n"})

    assert any("Upstream" in e for e in errors_for(skill))


def test_source_md_must_name_a_commit(tmp_path: Path) -> None:
    skill = make_folded(tmp_path / "skills", extra={"SOURCE.md": "- Upstream: https://github.com/example/agents\n"})

    assert any("Commit" in e for e in errors_for(skill))


def test_folded_skill_must_declare_its_license(tmp_path: Path) -> None:
    fields = {"name": "folded-skill", "description": DESCRIPTION, "compatibility": COMPAT}

    assert any("license" in e for e in errors_for(make_folded(tmp_path / "skills", fields=fields)))


def test_skill_without_source_md_needs_no_licence(tmp_path: Path) -> None:
    assert errors_for(make_skill(tmp_path / "skills")) == []


def make_notices_family(tmp_path: Path, notices: str | None) -> Path:
    root = make_family(tmp_path / "fam", {"core": ["base-skill"], "library": ["lib-skill"]})
    folded = make_folded(root / "core" / "skills")
    assert folded.name == "folded-skill"
    if notices is not None:
        (tmp_path / "THIRD_PARTY_NOTICES.md").write_text(notices)
    return root


def test_find_notices_looks_upward(tmp_path: Path) -> None:
    (tmp_path / "THIRD_PARTY_NOTICES.md").write_text("x")
    deep = tmp_path / "a" / "b"
    deep.mkdir(parents=True)

    assert find_notices(deep) == tmp_path / "THIRD_PARTY_NOTICES.md"
    assert find_notices(tmp_path / "a") == tmp_path / "THIRD_PARTY_NOTICES.md"


def test_find_notices_returns_none_when_absent(tmp_path: Path) -> None:
    deep = tmp_path / "a"
    deep.mkdir()

    assert find_notices(deep, limit=1) is None


def test_every_upstream_must_be_in_the_notices(tmp_path: Path) -> None:
    root = make_notices_family(tmp_path, "Nothing relevant here.\n")

    reports, errors = check_family(root, bundles=None, notices=find_notices(root))

    assert any("https://github.com/example/agents" in e and "THIRD_PARTY_NOTICES" in e for e in errors)
    assert all(not r.errors for r in reports)


def test_notices_that_list_the_upstream_are_clean(tmp_path: Path) -> None:
    root = make_notices_family(tmp_path, "- https://github.com/example/agents (MIT, Example)\n")

    _, errors = check_family(root, bundles=None, notices=find_notices(root))

    assert errors == []


def test_missing_notices_file_is_an_error_when_a_skill_has_a_source(tmp_path: Path) -> None:
    root = make_notices_family(tmp_path, None)

    _, errors = check_family(root, bundles=None, notices=None)

    assert any("THIRD_PARTY_NOTICES.md" in e for e in errors)
