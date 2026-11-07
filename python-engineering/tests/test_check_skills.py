import json
from collections.abc import Mapping
from pathlib import Path

import pytest
from check_skills import (
    ARGUMENT_KEYS,
    check_all,
    check_skill,
    main,
    render_table,
    sync_script,
)

DESCRIPTION = "Writes pytest tests. Use when adding or fixing tests."
CANONICAL = "# canonical detect script\n"


def make_skill(
    root: Path,
    name: str = "demo-skill",
    *,
    frontmatter: Mapping[str, object] | None = None,
    body: str = "# Demo\n\nRun `scripts/detect_project.py` first.\n",
    files: Mapping[str, str] | None = None,
) -> Path:
    fields = {"name": name, "description": DESCRIPTION} if frontmatter is None else frontmatter
    header = "".join(f"{key}: {json.dumps(value)}\n" for key, value in fields.items())
    skill = root / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(f"---\n{header}---\n{body}")
    vendored = {"scripts/detect_project.py": CANONICAL, **(files or {})}
    for rel, content in vendored.items():
        path = skill / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return skill


@pytest.fixture
def canonical(tmp_path: Path) -> Path:
    path = tmp_path / "canonical" / "detect_project.py"
    path.parent.mkdir()
    path.write_text(CANONICAL)
    return path


def errors_for(skill: Path, canonical: Path) -> list[str]:
    return check_skill(skill, canonical=canonical).errors


def test_valid_skill_has_no_errors(tmp_path: Path, canonical: Path) -> None:
    assert errors_for(make_skill(tmp_path / "skills"), canonical) == []


def test_missing_skill_md_is_an_error(tmp_path: Path, canonical: Path) -> None:
    empty = tmp_path / "skills" / "empty-skill"
    empty.mkdir(parents=True)

    assert errors_for(empty, canonical) == ["empty-skill: SKILL.md is missing"]


def test_frontmatter_must_start_on_the_first_line(tmp_path: Path, canonical: Path) -> None:
    skill = make_skill(tmp_path / "skills")
    (skill / "SKILL.md").write_text("\n---\nname: demo-skill\n---\nbody\n")

    assert any("first line" in e for e in errors_for(skill, canonical))


def test_invalid_yaml_frontmatter_is_an_error(tmp_path: Path, canonical: Path) -> None:
    skill = make_skill(tmp_path / "skills")
    (skill / "SKILL.md").write_text("---\nname: [unclosed\n---\nbody\n")

    assert any("not valid YAML" in e for e in errors_for(skill, canonical))


def test_keys_outside_the_spec_are_rejected(tmp_path: Path, canonical: Path) -> None:
    skill = make_skill(
        tmp_path / "skills",
        frontmatter={"name": "demo-skill", "description": DESCRIPTION, "context": "fork"},
    )

    assert any("unknown frontmatter key 'context'" in e for e in errors_for(skill, canonical))


def test_argument_hint_with_known_keys_is_allowed(tmp_path: Path, canonical: Path) -> None:
    hint = "[python=3.12 runner=uv rigor=full]"
    skill = make_skill(
        tmp_path / "skills",
        frontmatter={"name": "demo-skill", "description": DESCRIPTION, "argument-hint": hint},
    )

    assert errors_for(skill, canonical) == []


def test_argument_hint_with_unknown_key_is_an_error(tmp_path: Path, canonical: Path) -> None:
    skill = make_skill(
        tmp_path / "skills",
        frontmatter={
            "name": "demo-skill",
            "description": DESCRIPTION,
            "argument-hint": "[python=3.12 colour=red]",
        },
    )

    assert any("argument-hint key 'colour'" in e for e in errors_for(skill, canonical))


def test_argument_keys_match_the_documented_set() -> None:
    assert {"python", "runner", "types", "layout", "backend", "rigor", "report"} == ARGUMENT_KEYS


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
    tmp_path: Path, canonical: Path, name: str, problem: str
) -> None:
    skill = make_skill(tmp_path / "skills", name)

    assert any(problem in e for e in errors_for(skill, canonical))


def test_name_must_equal_the_folder_name(tmp_path: Path, canonical: Path) -> None:
    skill = make_skill(
        tmp_path / "skills",
        "demo-skill",
        frontmatter={"name": "other-name", "description": DESCRIPTION},
    )

    assert any("must equal the folder name" in e for e in errors_for(skill, canonical))


@pytest.mark.parametrize(
    ("description", "problem"),
    [
        (None, "description is missing"),
        ("", "description is missing"),
        ("x" * 351, "over the 350-character budget"),
    ],
)
def test_description_rules(
    tmp_path: Path, canonical: Path, description: str | None, problem: str
) -> None:
    fields: dict[str, object] = {"name": "demo-skill"}
    if description is not None:
        fields["description"] = description
    skill = make_skill(tmp_path / "skills", frontmatter=fields)

    assert any(problem in e for e in errors_for(skill, canonical))


def test_description_over_the_spec_limit_is_reported_as_spec_violation(
    tmp_path: Path, canonical: Path
) -> None:
    skill = make_skill(
        tmp_path / "skills", frontmatter={"name": "demo-skill", "description": "x" * 1025}
    )

    assert any("over the spec limit of 1024" in e for e in errors_for(skill, canonical))


def test_body_over_the_line_budget_is_an_error(tmp_path: Path, canonical: Path) -> None:
    body = "Run `scripts/detect_project.py`.\n" + "line\n" * 200
    skill = make_skill(tmp_path / "skills", body=body)

    assert any("201 body lines" in e and "budget of 200" in e for e in errors_for(skill, canonical))


def test_link_to_missing_file_is_an_error(tmp_path: Path, canonical: Path) -> None:
    body = "Run `scripts/detect_project.py`. See [more](references/more.md).\n"
    skill = make_skill(tmp_path / "skills", body=body)

    assert any("references/more.md does not exist" in e for e in errors_for(skill, canonical))


def test_link_to_existing_file_one_level_down_is_fine(tmp_path: Path, canonical: Path) -> None:
    body = "Run `scripts/detect_project.py`. See [more](references/more.md).\n"
    skill = make_skill(tmp_path / "skills", body=body, files={"references/more.md": "# More\n"})

    assert errors_for(skill, canonical) == []


def test_link_nested_deeper_than_one_folder_is_an_error(tmp_path: Path, canonical: Path) -> None:
    body = "Run `scripts/detect_project.py`. See [deep](references/a/b.md).\n"
    skill = make_skill(tmp_path / "skills", body=body, files={"references/a/b.md": "# B\n"})

    assert any("references/a/b.md is nested" in e for e in errors_for(skill, canonical))


def test_reference_file_linking_to_another_reference_is_an_error(
    tmp_path: Path, canonical: Path
) -> None:
    body = "Run `scripts/detect_project.py`. See [a](references/a.md).\n"
    files = {"references/a.md": "See [b](b.md).\n", "references/b.md": "# B\n"}
    skill = make_skill(tmp_path / "skills", body=body, files=files)

    assert any("references/a.md links to another file" in e for e in errors_for(skill, canonical))


def test_web_links_and_anchors_are_not_checked_as_files(tmp_path: Path, canonical: Path) -> None:
    body = "Run `scripts/detect_project.py`. [docs](https://example.com/x) [top](#top)\n"
    skill = make_skill(tmp_path / "skills", body=body)

    assert errors_for(skill, canonical) == []


def test_long_reference_needs_a_contents_list(tmp_path: Path, canonical: Path) -> None:
    body = "Run `scripts/detect_project.py`. See [a](references/a.md).\n"
    skill = make_skill(
        tmp_path / "skills", body=body, files={"references/a.md": "# A\n" + "text\n" * 101}
    )

    assert any("references/a.md has 102 lines and no Contents" in e for e in errors_for(skill, canonical))


def test_long_reference_with_contents_is_fine(tmp_path: Path, canonical: Path) -> None:
    body = "Run `scripts/detect_project.py`. See [a](references/a.md).\n"
    content = "# A\n\n## Contents\n\n- one\n" + "text\n" * 101
    skill = make_skill(tmp_path / "skills", body=body, files={"references/a.md": content})

    assert errors_for(skill, canonical) == []


def test_windows_style_paths_are_an_error(tmp_path: Path, canonical: Path) -> None:
    body = "Run `scripts\\detect_project.py`.\n"
    skill = make_skill(tmp_path / "skills", body=body)

    assert any("backslash path" in e for e in errors_for(skill, canonical))


def test_skill_that_runs_the_script_needs_the_vendored_copy(
    tmp_path: Path, canonical: Path
) -> None:
    skill = make_skill(tmp_path / "skills")
    (skill / "scripts" / "detect_project.py").unlink()

    assert any("scripts/detect_project.py is missing" in e and "cp " in e for e in errors_for(skill, canonical))


def test_vendored_copy_must_match_the_canonical_script(tmp_path: Path, canonical: Path) -> None:
    skill = make_skill(tmp_path / "skills", files={"scripts/detect_project.py": "# edited\n"})

    errors = errors_for(skill, canonical)

    assert any("differs from the canonical" in e and f"cp {canonical} " in e for e in errors)


def test_skill_that_never_mentions_the_script_needs_no_copy(
    tmp_path: Path, canonical: Path
) -> None:
    skill = make_skill(tmp_path / "skills", body="# Demo\n")
    (skill / "scripts" / "detect_project.py").unlink()

    assert errors_for(skill, canonical) == []


def test_check_all_reads_every_skill_folder_and_ignores_files(
    tmp_path: Path, canonical: Path
) -> None:
    skills = tmp_path / "skills"
    make_skill(skills, "first-skill")
    make_skill(skills, "second-skill")
    (skills / "README.md").write_text("not a skill")

    reports = check_all(skills, canonical=canonical)

    assert [r.name for r in reports] == ["first-skill", "second-skill"]


def test_token_estimate_uses_the_measured_chars_per_token(tmp_path: Path, canonical: Path) -> None:
    # 2.8 chars per token: measured with the claude CLI's usage over 13 real skill bodies.
    body = "x" * 280
    skill = make_skill(tmp_path / "skills", "sized-skill", body=body)

    assert check_skill(skill, canonical=canonical).body_tokens == 100


def test_table_lists_each_skill_and_the_always_on_total(tmp_path: Path, canonical: Path) -> None:
    skills = tmp_path / "skills"
    make_skill(skills, "first-skill")
    make_skill(skills, "second-skill")

    table = render_table(check_all(skills, canonical=canonical))

    assert "first-skill" in table
    assert "second-skill" in table
    assert f"description chars {2 * len(DESCRIPTION)}" in table
    assert "always-on description tokens" in table


def test_main_returns_zero_for_valid_skills(
    tmp_path: Path, canonical: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_skill(tmp_path / "skills")

    assert main([str(tmp_path / "skills"), "--canonical", str(canonical)]) == 0

    assert "demo-skill" in capsys.readouterr().out


def test_main_returns_one_and_prints_errors_for_invalid_skills(
    tmp_path: Path, canonical: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_skill(tmp_path / "skills", frontmatter={"name": "demo-skill", "description": ""})

    assert main([str(tmp_path / "skills"), "--canonical", str(canonical)]) == 1

    assert "description is missing" in capsys.readouterr().err


def test_main_returns_two_when_the_skills_folder_is_missing(
    tmp_path: Path, canonical: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "nope"

    assert main([str(missing), "--canonical", str(canonical)]) == 2

    assert f"error: {missing} is not a directory" in capsys.readouterr().err


def test_argument_keys_can_be_configured(tmp_path: Path, canonical: Path) -> None:
    fields = {"name": "demo-skill", "description": DESCRIPTION, "argument-hint": "[scene=a fps=25]"}
    skill = make_skill(tmp_path / "skills", frontmatter=fields)

    assert check_skill(skill, canonical=canonical, argument_keys=frozenset({"scene", "fps"})).errors == []
    assert check_skill(skill, canonical=canonical, argument_keys=None).errors == []
    assert any("argument-hint key 'scene'" in e for e in errors_for(skill, canonical))


def test_main_argument_keys_option(
    tmp_path: Path, canonical: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    fields = {"name": "demo-skill", "description": DESCRIPTION, "argument-hint": "[scene=a]"}
    make_skill(tmp_path / "skills", frontmatter=fields)
    base = [str(tmp_path / "skills"), "--canonical", str(canonical)]

    assert main(base) == 1
    assert main([*base, "--argument-keys", "scene"]) == 0
    assert main([*base, "--argument-keys", ""]) == 0
    capsys.readouterr()


def test_sync_script_copies_only_where_needed(tmp_path: Path, canonical: Path) -> None:
    skills = tmp_path / "skills"
    stale = make_skill(skills, "stale-skill", files={"scripts/detect_project.py": "# old\n"})
    current = make_skill(skills, "current-skill")
    unused = make_skill(skills, "unused-skill", body="# Demo\n")
    (unused / "scripts" / "detect_project.py").unlink()
    (unused / "scripts").rmdir()

    written = sync_script(skills, canonical=canonical)

    assert written == [stale / "scripts" / "detect_project.py"]
    assert (stale / "scripts" / "detect_project.py").read_text() == CANONICAL
    assert (current / "scripts" / "detect_project.py").read_text() == CANONICAL
    assert not (unused / "scripts").exists()


def test_main_sync_fixes_a_missing_copy(tmp_path: Path, canonical: Path) -> None:
    skill = make_skill(tmp_path / "skills")
    (skill / "scripts" / "detect_project.py").unlink()
    base = [str(tmp_path / "skills"), "--canonical", str(canonical)]

    assert main(base) == 1
    assert main([*base, "--sync"]) == 0
