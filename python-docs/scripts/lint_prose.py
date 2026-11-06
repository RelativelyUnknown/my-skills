"""Flag wording that documentation style guides advise against, in Markdown, reST or text files.

Needs Python 3.11+ and the standard library only. Skips fenced code, indented code under `::`,
inline code, URLs, quoted text and front matter. A line containing `lint-prose: ignore` is skipped,
and so is everything between lines containing `lint-prose: off` and `lint-prose: on`.
Findings are advice: read each one in context and keep the wording when it is right.
"""

import argparse
import re
import sys
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path

SUFFIXES = (".md", ".markdown", ".rst", ".txt")
IGNORE_MARK = "lint-prose: ignore"
OFF_MARK = "lint-prose: off"
ON_MARK = "lint-prose: on"
LONG_SENTENCE_WORDS = 35
EM_DASHES_PER_PARAGRAPH = 2

# (rule, alternatives, message). Alternatives are regex fragments matched as whole words, ignoring case.
WORD_RULES: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("puffery", (
        r"seamless(ly)?", "robust", r"cutting[- ]edge", r"state[- ]of[- ]the[- ]art", r"world[- ]class",
        r"best[- ]in[- ]class", r"game[- ]chang(er|ing)", r"revolutioni[sz]e\w*", "groundbreaking",
        r"blazing(ly)?[- ]fast", r"lightning[- ]fast", "powerful", r"effortless(ly)?", "comprehensive", "pivotal",
        "crucial", "vital", "testament", "unparalleled", r"next[- ]generation",
    ), "promotional word; say what it does and give a number if speed or size matters"),
    ("ai-vocabulary", (
        r"delve[sd]?", "delving", r"leverag(e|es|ed|ing)", r"utili[sz](e|es|ed|ing)", "tapestry", "multifaceted",
        r"foster(s|ed|ing)?", "realm", r"embark(s|ed|ing)?", r"elevat(e|es|ed|ing)", r"unlock(s|ed|ing)?",
        r"empower(s|ed|ing)?", r"streamlin(e|es|ed|ing)", r"harness(es|ed|ing)?", "holistic", r"synerg(y|ies)",
        "paradigm", "landscape", r"ever[- ]evolving", r"navigat(e|es|ing) the complexit(y|ies)",
        r"in today's \w+ world", r"it'?s worth noting", "it is worth noting", r"it'?s important to note",
        "it is important to note", "in conclusion", "in summary",
    ), "generic AI-style wording; use the plain word or delete"),
    ("minimizer", (
        "simply", "just", "easy", "easily", "obviously", "of course", "clearly", "straightforward",
        r"trivial(ly)?", "merely",
    ), "implies the reader should find this easy; delete it"),
    ("filler", (
        "in order to", "please note( that)?", "note that", "due to the fact that", "at this point in time",
        "is able to", "are able to", "make use of", "a number of", "basically", "actually", "really", "very",
        "quite", "in fact", "needless to say", "it should be noted", "for all intents and purposes", "whether or not",
    ), "filler; cut it or use the short form (to, because, now, can, use, some)"),
    ("latin", (r"e\.g\.", r"i\.e\.", r"etc\.", r"viz\.", r"cf\.", r"vs\."),
     "Latin abbreviation; write 'for example', 'that is', 'and so on', 'compare', 'versus'"),
    ("timeless", (
        "currently", "recently", "nowadays", "as of now", "at the moment", "new(ly)? (added|introduced)",
        "no longer", "soon", "coming soon", "in the future", "now supports?",
    ), "ages badly; state the behavior, and put history in the changelog"),
    ("residue", (
        "as discussed", "as mentioned (above|earlier|before)", "as requested", "per your request",
        "i hope this helps", "let me know", "feel free to", "great question", "certainly", "happy to help",
        "we decided", "as an ai",
    ), "conversation residue; documentation describes the software, not the chat"),
    ("directional", (
        "(see|shown|listed|described|mentioned) (above|below)",
        "the (above|below) (example|table|list|code|section)",
        "(example|table|list|code|section) (above|below)",
    ), "directional reference breaks when content moves; link or name the section"),
)
LINK_TEXT = re.compile(r"\[(click here|here|this link|link|this|read more)\]\(", re.IGNORECASE)
HISTORY_FILES = ("CHANGELOG", "CHANGES", "HISTORY", "NEWS", "RELEASE")
FUTURE = re.compile(r"\b(will|won't)\s+(be\s+)?\w+", re.IGNORECASE)
EXCLAMATION = re.compile(r"\w!(\s|$)")
EMOJI = re.compile("[\U0001f300-\U0001faff\u2600-\u27bf]")
HEADING_MD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
INLINE_CODE = re.compile(r"`[^`]*`")
URL = re.compile(r"https?://\S+|<[^>]+>")
QUOTED = re.compile(r"\"[^\"]*\"|\u201c[^\u201d]*\u201d")  # quoted words are mentions, not uses
LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
# Generic words that are lowercase in sentence-case headings; product names are not in this list.
COMMON_WORDS = frozenset(["about", "access", "add", "adding", "advanced", "api", "architecture", "asked", "authentication", "authorization", "basic", "basics", "best", "build", "building", "changes", "class", "classes", "client", "command", "commands", "concepts", "config", "configuration", "configure", "configuring", "contributing", "create", "creating", "data", "debugging", "deploy", "deploying", "deployment", "design", "developer", "developers", "development", "error", "errors", "example", "examples", "feature", "features", "file", "files", "first", "frequently", "function", "functions", "getting", "guide", "handling", "how", "install", "installation", "installing", "interface", "issues", "known", "license", "limitations", "line", "load", "loading", "local", "logging", "manage", "managing", "method", "methods", "migrate", "migrating", "migration", "model", "models", "monitoring", "more", "new", "next", "notes", "option", "options", "overview", "package", "packages", "performance", "practice", "practices", "project", "projects", "queries", "query", "questions", "quick", "read", "reading", "reference", "release", "remove", "removing", "request", "requests", "requirements", "response", "run", "running", "save", "saving", "schema", "security", "server", "set", "setting", "settings", "setup", "start", "started", "step", "steps", "storage", "store", "support", "supported", "table", "tables", "test", "testing", "tests", "troubleshooting", "tuning", "tutorial", "tutorials", "type", "types", "up", "update", "updating", "upgrade", "upgrading", "use", "user", "users", "using", "variable", "variables", "version", "versions", "what", "when", "why", "work", "working", "write", "writing", "your"])
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")


@dataclass(frozen=True, slots=True)
class Finding:
    path: str
    line: int
    rule: str
    text: str
    message: str

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.rule}: '{self.text}': {self.message}"


def prose_lines(text: str) -> Iterator[tuple[int, str]]:
    """Yield (line number, line) for prose lines, with inline code, URLs and quoted text blanked."""
    lines = text.splitlines()
    in_fence = False
    fence = ""
    in_front_matter = bool(lines) and lines[0].strip() == "---"
    rst_literal_indent: int | None = None
    switched_off = False
    for number, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if OFF_MARK in raw or ON_MARK in raw:
            switched_off = OFF_MARK in raw
            continue
        if switched_off:
            continue
        if in_front_matter:
            if number > 1 and stripped in {"---", "..."}:
                in_front_matter = False
            continue
        if in_fence:
            if stripped.startswith(fence):
                in_fence = False
            continue
        if stripped.startswith(("```", "~~~")):
            in_fence, fence = True, stripped[:3]
            continue
        indent = len(raw) - len(raw.lstrip())
        if rst_literal_indent is not None:
            if not stripped or indent > rst_literal_indent:
                continue
            rst_literal_indent = None
        if stripped.endswith("::") or stripped.startswith(".. code"):
            rst_literal_indent = indent
        if (indent >= 4 and not stripped.startswith(("-", "*", "+"))) or IGNORE_MARK in raw:
            continue
        yield number, QUOTED.sub('" "', URL.sub(" ", INLINE_CODE.sub(" ", raw)))


def _word_pattern(alternatives: Iterable[str]) -> re.Pattern[str]:
    return re.compile(rf"(?<![\w-])({'|'.join(alternatives)})(?![\w-])", re.IGNORECASE)


COMPILED = tuple((rule, _word_pattern(alternatives), message) for rule, alternatives, message in WORD_RULES)


def is_title_case(heading: str) -> bool:
    """True when a generic word after the first is capitalized and none is lowercase."""
    words = re.findall(r"[A-Za-z][\w'-]*", heading)[1:]
    common = [w for w in words if w.lower() in COMMON_WORDS and not w.isupper()]  # acronyms (API, CLI) stay
    return bool(common) and all(w[0].isupper() for w in common)


def check_line(path: str, number: int, line: str, *, future: bool, skip: frozenset[str]) -> list[Finding]:
    findings = [
        Finding(path, number, rule, match.group(0), message)
        for rule, pattern, message in COMPILED
        if rule not in skip
        for match in pattern.finditer(line)
    ]
    findings.extend(
        Finding(path, number, "link-text", m.group(1), "link text must say where it goes")
        for m in LINK_TEXT.finditer(line)
    )
    heading = HEADING_MD.match(line)
    if heading and is_title_case(heading.group(2)):
        findings.append(Finding(path, number, "heading-case", heading.group(2), "use sentence case for headings"))
    if heading and EMOJI.search(heading.group(2)):
        findings.append(Finding(path, number, "emoji", heading.group(2), "no emoji in headings"))
    if EXCLAMATION.search(line):
        findings.append(Finding(path, number, "exclamation", line.strip()[:40], "drop the exclamation mark"))
    if future:
        findings.extend(
            Finding(path, number, "future-tense", m.group(0), "describe behavior in the present tense")
            for m in FUTURE.finditer(line)
        )
    return findings


def check_paragraphs(path: str, numbered: Sequence[tuple[int, str]]) -> list[Finding]:
    findings = []
    paragraph: list[tuple[int, str]] = []
    for item in [*numbered, (0, "")]:
        line = item[1]
        is_item = LIST_ITEM.match(line) is not None
        is_break = is_item or not line.strip() or HEADING_MD.match(line) is not None or line.lstrip().startswith("|")
        if not is_break:
            paragraph.append(item)
            continue
        if paragraph:
            findings.extend(_paragraph_findings(path, paragraph))
            paragraph = []
        if is_item:
            paragraph.append(item)
    return findings


def _paragraph_findings(path: str, paragraph: Sequence[tuple[int, str]]) -> list[Finding]:
    start = paragraph[0][0]
    text = " ".join(line.strip() for _, line in paragraph)
    findings = []
    for sentence in SENTENCE_END.split(text):
        words = sentence.split()
        if len(words) > LONG_SENTENCE_WORDS:
            findings.append(
                Finding(path, start, "long-sentence", " ".join(words[:8]) + " ...",
                        f"{len(words)} words; split it (aim for under 25)")
            )
    dashes = text.count("\u2014")
    if dashes > EM_DASHES_PER_PARAGRAPH:
        findings.append(Finding(path, start, "em-dash", f"{dashes} em dashes", "use commas, colons or full stops"))
    return findings


def check_text(path: str, text: str, *, future: bool = False) -> list[Finding]:
    """Return findings for one document. History files (changelogs) skip the timeless rule."""
    skip = frozenset({"timeless"}) if Path(path).name.upper().startswith(HISTORY_FILES) else frozenset()
    numbered = list(prose_lines(text))
    findings = [f for number, line in numbered for f in check_line(path, number, line, future=future, skip=skip)]
    findings.extend(check_paragraphs(path, numbered))
    return sorted(findings, key=lambda f: (f.line, f.rule))


def iter_files(paths: Iterable[Path]) -> Iterator[Path]:
    for path in paths:
        if path.is_dir():
            yield from sorted(p for p in path.rglob("*") if p.suffix in SUFFIXES and ".venv" not in p.parts)
        elif path.is_file():
            yield path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+", type=Path, help="files or folders to check")
    parser.add_argument("--rules", help="comma-separated rules to report (default: all)")
    parser.add_argument("--future", action="store_true", help="also flag future tense ('will ...')")
    args = parser.parse_args(argv)
    wanted = set(args.rules.split(",")) if args.rules else None
    findings = [
        finding
        for path in iter_files(args.paths)
        for finding in check_text(str(path), path.read_text(encoding="utf-8", errors="replace"), future=args.future)
        if wanted is None or finding.rule in wanted
    ]
    for finding in findings:
        sys.stdout.write(finding.render() + "\n")
    sys.stdout.write(f"{len(findings)} findings\n")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
