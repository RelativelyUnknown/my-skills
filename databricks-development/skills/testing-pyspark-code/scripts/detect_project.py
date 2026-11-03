"""Print a Databricks project's bundle, compute, Spark client and tooling facts as key=value lines.

Needs Python 3.11+ and the standard library only; a copy of this file ships in every skill.
YAML is scanned line by line, not parsed, so unusual layouts may print `# default`.
"""

import re
import shutil
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    sys.exit("error: needs Python 3.11+ (tomllib); read pyproject.toml directly instead")

TOOLS = ("databricks", "uv", "java", "ruff", "mypy", "pytest")
SKIP_DIRS = frozenset({".git", ".venv", "venv", "node_modules", "dist", "build", ".databricks", "__pycache__"})
BUNDLE_FILES = ("databricks.yml", "databricks.yaml")
NOTEBOOK_HEADER = "# Databricks notebook source"
TOP_LEVEL_KEY = re.compile(r"^(\S[^:#]*):")
CHILD_KEY = re.compile(r"^(\s+)([A-Za-z0-9_.-]+):\s*(#.*)?$")
SPARK_VERSION = re.compile(r"^\s*spark_version:\s*[\"']?([^\"'\s#]+)")
ENV_VERSION = re.compile(r"^\s*(?:environment_version|client):\s*[\"']?([^\"'\s#]+)")
SERVERLESS = re.compile(r"^\s*serverless:\s*true\b")
ENV_KEY = re.compile(r"^\s*-?\s*environment_key:")
SDP_PYTHON = re.compile(r"^\s*(from pyspark import pipelines|import pyspark\.pipelines|import dlt\b|from dlt import)", re.MULTILINE)
SDP_LEGACY = re.compile(r"^\s*(import dlt\b|from dlt import)", re.MULTILINE)
SDP_SQL = re.compile(r"\bCREATE\s+(OR\s+REFRESH\s+)?(STREAMING\s+TABLE|MATERIALIZED\s+VIEW)\b", re.IGNORECASE)
DATA_SOURCE = re.compile(r"^\s*from pyspark\.sql\.datasource import", re.MULTILINE)
REQUIREMENT_NAME = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")


@dataclass(frozen=True, slots=True)
class Fact:
    value: str
    source: str


def _files(root: Path, suffixes: Iterable[str]) -> list[Path]:
    wanted = tuple(suffixes)
    found = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file() and path.name.endswith(wanted):
            found.append(path)
    return sorted(found)


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _block_children(text: str, key: str) -> list[str]:
    """Return the child key names of a top-level YAML block such as `targets:`."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.rstrip() != f"{key}:":
            continue
        indent: str | None = None
        children = []
        for child in lines[index + 1 :]:
            if not child.strip() or child.lstrip().startswith("#"):
                continue
            if TOP_LEVEL_KEY.match(child):
                break
            match = CHILD_KEY.match(child)
            if match is None:
                continue
            if indent is None:
                indent = match.group(1)
            if match.group(1) == indent:
                children.append(match.group(2))
        return children
    return []


def bundle_facts(root: Path) -> dict[str, Fact]:
    bundle = next((root / name for name in BUNDLE_FILES if (root / name).is_file()), None)
    if bundle is None:
        return {"bundle": Fact("none", "# default: no databricks.yml in this folder")}
    text = _read(bundle)
    targets = _block_children(text, "targets")
    default = next((t for t in targets if _target_is_default(text, t)), None)
    return {
        "bundle": Fact(bundle.name, ""),
        "bundle.targets": Fact(",".join(targets) or "none", "" if targets else "# default: no targets block"),
        "bundle.default_target": Fact(default or "none", "" if default else "# default: no target sets default: true"),
    }


def _target_is_default(text: str, target: str) -> bool:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != f"{target}:":
            continue
        own_indent = len(line) - len(line.lstrip())
        for child in lines[index + 1 :]:
            if not child.strip():
                continue
            if len(child) - len(child.lstrip()) <= own_indent:
                break
            if child.strip().replace(" ", "") == "default:true":
                return True
    return False


def compute_facts(root: Path) -> dict[str, Fact]:
    spark_versions: set[str] = set()
    env_versions: set[str] = set()
    serverless = False
    for path in _files(root, (".yml", ".yaml")):
        for line in _read(path).splitlines():
            if match := SPARK_VERSION.match(line):
                spark_versions.add(match.group(1))
            if match := ENV_VERSION.match(line):
                env_versions.add(match.group(1))
            if SERVERLESS.match(line) or ENV_KEY.match(line):
                serverless = True
    classic = bool(spark_versions)
    if classic and serverless:
        compute = Fact("mixed", "")
    elif classic:
        compute = Fact("classic", "")
    elif serverless:
        compute = Fact("serverless", "")
    else:
        compute = Fact("serverless", "# default: no spark_version or environments found in YAML")
    return {
        "compute": compute,
        "runtime": Fact(",".join(sorted(spark_versions)) or "none", "" if spark_versions else "# default"),
        "serverless.environment_version": Fact(
            ",".join(sorted(env_versions)) or "none", "" if env_versions else "# default"
        ),
    }


def _requirement_names(items: object) -> set[str]:
    names: set[str] = set()
    if not isinstance(items, list):
        return names
    for item in items:
        if isinstance(item, str) and (match := REQUIREMENT_NAME.match(item)):
            names.add(match.group(1).lower().replace("_", "-"))
    return names


def dependency_names(pyproject: Mapping[str, object]) -> tuple[set[str], set[str]]:
    """Return (runtime dependencies, dev-only dependencies) by normalized name."""
    project = pyproject.get("project")
    runtime: set[str] = set()
    dev: set[str] = set()
    if isinstance(project, Mapping):
        runtime |= _requirement_names(project.get("dependencies"))
        extras = project.get("optional-dependencies")
        if isinstance(extras, Mapping):
            for group in extras.values():
                dev |= _requirement_names(group)
    groups = pyproject.get("dependency-groups")
    if isinstance(groups, Mapping):
        for group in groups.values():
            dev |= _requirement_names(group)
    return runtime, dev


def spark_client_facts(root: Path) -> dict[str, Fact]:
    pyproject_path = root / "pyproject.toml"
    runtime: set[str] = set()
    dev: set[str] = set()
    source = ""
    if pyproject_path.is_file():
        try:
            data = tomllib.loads(_read(pyproject_path))
        except tomllib.TOMLDecodeError as error:
            return {"spark.client": Fact("unknown", f"# pyproject.toml is not valid TOML: {error}")}
        runtime, dev = dependency_names(data)
        source = "pyproject.toml"
    for req in sorted(root.glob("requirements*.txt")):
        for line in _read(req).splitlines():
            if match := REQUIREMENT_NAME.match(line):
                dev.add(match.group(1).lower().replace("_", "-"))
        source = source or req.name
    every = runtime | dev
    has_connect = "databricks-connect" in every
    has_pyspark = "pyspark" in every
    if has_connect and has_pyspark:
        client = Fact("conflict", "# databricks-connect and pyspark cannot share one environment")
    elif has_connect:
        client = Fact("databricks-connect", "")
    elif has_pyspark:
        client = Fact("pyspark", "")
    else:
        client = Fact("none", "# default: neither databricks-connect nor pyspark declared")
    facts = {"spark.client": client}
    shipped = sorted(runtime & {"pyspark", "databricks-connect", "delta-spark"})
    facts["spark.in_runtime_deps"] = Fact(
        ",".join(shipped) or "none",
        "# the runtime provides these; keep them out of [project].dependencies" if shipped else "",
    )
    testing = sorted(every & {"chispa", "pytest", "pytest-spark"})
    facts["test.tools"] = Fact(",".join(testing) or "none", "" if testing else "# default")
    if not source:
        facts["spark.client"] = Fact("none", "# default: no pyproject.toml or requirements*.txt")
    return facts


def code_facts(root: Path) -> dict[str, Fact]:
    notebooks = 0
    sdp_files = 0
    sdp_legacy = 0
    data_sources = 0
    for path in _files(root, (".py", ".ipynb", ".sql")):
        text = _read(path)
        if path.suffix == ".ipynb" or text.startswith(NOTEBOOK_HEADER):
            notebooks += 1
        if path.suffix == ".sql":
            sdp_files += bool(SDP_SQL.search(text))
            continue
        if SDP_PYTHON.search(text):
            sdp_files += 1
            sdp_legacy += bool(SDP_LEGACY.search(text))
        data_sources += bool(DATA_SOURCE.search(text))
    if sdp_legacy:
        api = Fact("dlt", "# legacy import; current API is `from pyspark import pipelines as dp`")
    elif sdp_files:
        api = Fact("pyspark.pipelines", "")
    else:
        api = Fact("none", "# default")
    return {
        "notebooks": Fact(str(notebooks), ""),
        "pipelines.files": Fact(str(sdp_files), ""),
        "pipelines.api": api,
        "python_data_sources": Fact(str(data_sources), ""),
    }


def python_facts(root: Path) -> dict[str, Fact]:
    pyproject = root / "pyproject.toml"
    runner = Fact("uv", "# default")
    if (root / "uv.lock").is_file():
        runner = Fact("uv", "")
    elif (root / "poetry.lock").is_file():
        runner = Fact("poetry", "")
    elif any(root.glob("requirements*.txt")):
        runner = Fact("pip", "")
    target = Fact("3.12", "# default: no requires-python")
    if pyproject.is_file():
        try:
            data = tomllib.loads(_read(pyproject))
        except tomllib.TOMLDecodeError:
            data = {}
        project = data.get("project")
        requires = project.get("requires-python") if isinstance(project, Mapping) else None
        if isinstance(requires, str) and (match := re.search(r">=\s*(\d+\.\d+)", requires)):
            target = Fact(match.group(1), "")
    return {"python.target": target, "runner": runner}


def tool_facts() -> dict[str, Fact]:
    missing = [tool for tool in TOOLS if shutil.which(tool) is None]
    return {"tools.missing": Fact(",".join(missing) or "none", "")}


def collect(root: Path) -> dict[str, Fact]:
    facts: dict[str, Fact] = {}
    for part in (bundle_facts, compute_facts, spark_client_facts, code_facts, python_facts):
        facts |= part(root)
    facts |= tool_facts()
    return facts


def render(facts: Mapping[str, Fact]) -> str:
    lines = []
    for key, fact in facts.items():
        line = f"{key}={fact.value}"
        lines.append(f"{line}  {fact.source}" if fact.source else line)
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = Path(args[0]) if args else Path.cwd()
    if not root.is_dir():
        sys.stderr.write(f"error: {root} is not a directory\n")
        return 2
    sys.stdout.write(render(collect(root)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
