from pathlib import Path

import lint_prose as lp
import pytest


def rules(text: str, path: str = "doc.md", *, future: bool = False) -> list[str]:
    return [finding.rule for finding in lp.check_text(path, text, future=future)]


@pytest.mark.parametrize(
    ("text", "rule"),
    [
        ("Our robust engine is fast.", "puffery"),
        ("We leverage the cache to delve into data.", "ai-vocabulary"),
        ("Simply run the command.", "minimizer"),
        ("Run it in order to start.", "filler"),
        ("Use a format, e.g. JSON.", "latin"),
        ("The client currently retries twice.", "timeless"),
        ("As discussed, the flag is gone.", "residue"),
        ("See the table below for options.", "directional"),
        ("Read the guide [here](https://example.com).", "link-text"),
        ("It works!", "exclamation"),
    ],
    ids=["puffery", "ai-vocabulary", "minimizer", "filler", "latin", "timeless", "residue", "directional",
         "link-text", "exclamation"],
)
def test_each_word_rule_fires_on_its_example(text: str, rule: str) -> None:
    assert rule in rules(text)


def test_clean_sentence_has_no_findings() -> None:
    assert rules("Run `uv sync` to install the dependencies listed in `pyproject.toml`.") == []


def test_fenced_code_inline_code_and_urls_are_skipped() -> None:
    text = "```python\n# simply leverage this\n```\nCall `simply()` at https://example.com/robust.\n"

    assert rules(text) == []


def test_quoted_words_are_mentions_not_uses() -> None:
    assert rules('Avoid words like "seamless" and "robust".') == []


def test_rst_literal_block_is_skipped() -> None:
    text = "Example::\n\n    simply leverage it\n\nBack to prose.\n"

    assert rules(text, "doc.rst") == []


def test_front_matter_is_skipped() -> None:
    assert rules("---\ntitle: A robust guide\n---\nPlain text.\n") == []


def test_ignore_marker_skips_the_line() -> None:
    assert rules("This is robust. <!-- lint-prose: ignore -->") == []


@pytest.mark.parametrize(
    ("heading", "flagged"),
    [
        ("Getting Started With the CLI", True),
        ("Configure Logging", True),
        ("Getting started with the CLI", False),
        ("Install Databricks Connect", False),
        ("Using Delta Lake with Unity Catalog", False),
    ],
    ids=["title-case", "two-words", "sentence-case", "product-name", "product-names-sentence-case"],
)
def test_heading_case_flags_generic_capitalized_words_only(heading: str, *, flagged: bool) -> None:
    assert ("heading-case" in rules(f"## {heading}")) is flagged


def test_emoji_in_heading_is_flagged() -> None:
    assert "emoji" in rules("## Install \U0001f680")


def test_long_sentence_spanning_lines_is_flagged_once() -> None:
    words = " ".join(f"word{i}" for i in range(40))
    text = f"{words[:100]}\n{words[100:]}.\n"

    assert rules(text) == ["long-sentence"]


def test_list_items_are_separate_paragraphs() -> None:
    item = " ".join(["word"] * 20)
    text = f"- {item}.\n- {item}.\n"

    assert "long-sentence" not in rules(text)


def test_em_dash_density_is_flagged() -> None:
    assert "em-dash" in rules("One — two — three — four.")


def test_future_tense_only_when_asked() -> None:
    text = "The function will return a list."

    assert "future-tense" not in rules(text)
    assert "future-tense" in rules(text, future=True)


def test_changelog_skips_timeless_rule() -> None:
    text = "- The parser no longer accepts tabs.\n"

    assert rules(text, "CHANGELOG.md") == []
    assert rules(text, "guide.md") == ["timeless"]


def test_main_exit_code_and_rule_filter(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    doc = tmp_path / "guide.md"
    doc.write_text("Simply run it. Our robust tool.\n")

    assert lp.main([str(tmp_path), "--rules", "puffery"]) == 1
    out = capsys.readouterr().out
    assert "puffery" in out
    assert "minimizer" not in out
    assert lp.main([str(tmp_path), "--rules", "latin"]) == 0


def test_off_and_on_markers_skip_a_block() -> None:
    text = "<!-- lint-prose: off -->\nrobust, seamless\n<!-- lint-prose: on -->\nThis is robust.\n"

    assert rules(text) == ["puffery"]


def test_skill_copy_matches_canonical_script() -> None:
    root = Path(__file__).parent.parent
    canonical = root / "scripts" / "lint_prose.py"
    copy = root / "skills" / "writing-documentation" / "scripts" / "lint_prose.py"

    assert copy.read_bytes() == canonical.read_bytes(), f"run: cp {canonical} {copy}"


def test_acronyms_in_headings_are_not_title_case() -> None:
    assert "heading-case" not in rules("## OWASP API Top 10 checks")
