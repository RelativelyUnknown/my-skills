"""Print a Python project's version, tooling and installed tools as key=value lines.

Needs Python 3.11+ and the standard library only; a copy of this file ships in every skill.
"""

import configparser
import shutil
import sys
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from itertools import takewhile
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    sys.exit("error: needs Python 3.11+ (tomllib); read pyproject.toml directly instead")

TOOLS = (
    "uv", "poetry", "pdm", "hatch", "ruff", "mypy", "pyright", "basedpyright", "ty", "pyrefly", "pytest",
    "black", "flake8", "pylint", "isort", "nox", "tox", "xenon", "radon",
)  # fmt: skip
BACKENDS = {
    "hatchling.build": "hatchling",
    "setuptools.build_meta": "setuptools",
    "poetry.core.masonry.api": "poetry-core",
    "pdm.backend": "pdm-backend",
    "flit_core.buildapi": "flit-core",
    "uv_build": "uv_build",
    "maturin": "maturin",
}
ASYNC_PLUGINS = ("anyio", "pytest-asyncio", "trio")
NOT_PACKAGES = frozenset({"tests", "test", "docs", "scripts", "examples", "benchmarks"})
# (tool, [tool.<table>] name, config files); order is the order used in the output.
TYPE_CHECKERS = (
    ("mypy", "mypy", ("mypy.ini", ".mypy.ini")),
    ("pyright", "pyright", ("pyrightconfig.json",)),
    ("basedpyright", "basedpyright", ()),
    ("ty", "ty", ("ty.toml",)),
    ("pyrefly", "pyrefly", ("pyrefly.toml",)),
)
LINTERS = (
    ("ruff", "ruff", ("ruff.toml", ".ruff.toml")),
    ("flake8", "flake8", (".flake8",)),
    ("pylint", "pylint", (".pylintrc", "pylintrc")),
    ("black", "black", ()),
    ("isort", "isort", (".isort.cfg",)),
)


@dataclass(frozen=True, slots=True)
class Fact:
    value: str
    source: str


def _get(data: object, *keys: str) -> object:
    """Return the nested value at keys, or None when any level is missing."""
    for key in keys:
        if not isinstance(data, Mapping):
            return None
        data = data.get(key)
    return data


def _load_pyproject(root: Path) -> Mapping[str, object]:
    path = root / "pyproject.toml"
    if not path.exists():
        return {}
    with path.open("rb") as file:
        return tomllib.load(file)


def _normalize(name: str) -> str:
    return name.lower().replace("_", "-")


def _requirement_name(requirement: str) -> str:
    return _normalize("".join(takewhile(lambda ch: ch.isalnum() or ch in "-_.", requirement.strip())))


def _dependency_names(pyproject: Mapping[str, object]) -> set[str]:
    requirement_lists: list[object] = [
        _get(pyproject, "project", "dependencies"),
        _get(pyproject, "tool", "uv", "dev-dependencies"),
    ]
    for key in (("project", "optional-dependencies"), ("dependency-groups",)):
        table = _get(pyproject, *key)
        if isinstance(table, Mapping):
            requirement_lists.extend(table.values())
    names = {
        _requirement_name(item)
        for requirements in requirement_lists
        if isinstance(requirements, list)
        for item in requirements
        if isinstance(item, str)
    }
    poetry = _get(pyproject, "tool", "poetry")
    poetry_tables = [_get(poetry, "dependencies"), _get(poetry, "dev-dependencies")]
    groups = _get(poetry, "group")
    if isinstance(groups, Mapping):
        poetry_tables.extend(_get(group, "dependencies") for group in groups.values())
    for table in poetry_tables:
        if isinstance(table, Mapping):
            names.update(_normalize(key) for key in table)
    return names


def _lower_bound(spec: str) -> str | None:
    """Return major.minor of the first lower-bound clause in a version constraint."""
    for clause in spec.split(","):
        for operator in ("~=", ">=", "==", "^", "~", ">"):
            if clause.strip().startswith(operator):
                parts = clause.strip().removeprefix(operator).strip().split(".")
                return ".".join(parts[:2]) if len(parts) >= 2 else None
    return None


def _python_target(pyproject: Mapping[str, object]) -> Fact | None:
    spec = _get(pyproject, "project", "requires-python")
    if isinstance(spec, str) and (version := _lower_bound(spec)):
        return Fact(version, f'requires-python "{spec}"')
    poetry_spec = _get(pyproject, "tool", "poetry", "dependencies", "python")
    if isinstance(poetry_spec, str) and (version := _lower_bound(poetry_spec)):
        return Fact(version, f'tool.poetry python "{poetry_spec}"')
    return None


def _runner(root: Path, pyproject: Mapping[str, object]) -> Fact | None:
    for lockfile, name in (("uv.lock", "uv"), ("poetry.lock", "poetry"), ("pdm.lock", "pdm")):
        if (root / lockfile).exists():
            return Fact(name, lockfile)
    for name in ("uv", "poetry", "pdm"):
        if _get(pyproject, "tool", name) is not None:
            return Fact(name, f"[tool.{name}]")
    if (root / "hatch.toml").exists():
        return Fact("hatch", "hatch.toml")
    if _get(pyproject, "tool", "hatch", "envs") is not None:
        return Fact("hatch", "[tool.hatch.envs]")
    requirements = sorted(root.glob("requirements*.txt"))
    return Fact("pip", requirements[0].name) if requirements else None


def _layout(root: Path) -> Fact | None:
    src_init = next(iter(sorted((root / "src").glob("*/__init__.py"))), None)
    if src_init:
        return Fact("src", src_init.relative_to(root).as_posix())
    flat_init = next(
        (p for p in sorted(root.glob("*/__init__.py")) if p.parent.name not in NOT_PACKAGES),
        None,
    )
    return Fact("flat", f"{flat_init.parent.name}/__init__.py at root") if flat_init else None


def _backend(pyproject: Mapping[str, object]) -> Fact | None:
    build_backend = _get(pyproject, "build-system", "build-backend")
    if isinstance(build_backend, str):
        return Fact(BACKENDS.get(build_backend, build_backend), build_backend)
    return None


def _addopts(root: Path, pyproject: Mapping[str, object]) -> str:
    options = _get(pyproject, "tool", "pytest", "ini_options", "addopts")
    if isinstance(options, list):
        return " ".join(str(option) for option in options)
    if isinstance(options, str):
        return options
    ini = root / "pytest.ini"
    if ini.exists():
        parser = configparser.ConfigParser()
        parser.read(ini)
        return parser.get("pytest", "addopts", fallback="")
    return ""


def _pytest(
    root: Path, pyproject: Mapping[str, object], dependencies: set[str]
) -> tuple[Fact, Fact]:
    if _get(pyproject, "tool", "pytest", "ini_options") is not None:
        found = Fact("pytest", "[tool.pytest.ini_options]")
    elif (root / "pytest.ini").exists():
        found = Fact("pytest", "pytest.ini")
    elif "pytest" in dependencies:
        found = Fact("pytest", "dependency pytest")
    else:
        return Fact("pytest", "default"), Fact("prepend", "default")
    mode = next(
        (
            option.partition("=")[2]
            for option in _addopts(root, pyproject).split()
            if option.startswith("--import-mode=")
        ),
        None,
    )
    return found, Fact(mode, "addopts") if mode else Fact("prepend", "pytest default")


def _tools_in_use(
    root: Path,
    pyproject: Mapping[str, object],
    dependencies: set[str],
    candidates: Sequence[tuple[str, str, tuple[str, ...]]],
) -> Fact | None:
    found: list[tuple[str, str]] = []
    for tool, table, files in candidates:
        config_file = next((f for f in files if (root / f).exists()), None)
        if _get(pyproject, "tool", table) is not None:
            found.append((tool, f"[tool.{table}]"))
        elif config_file:
            found.append((tool, config_file))
        elif tool in dependencies:
            found.append((tool, f"dependency {tool}"))
    if not found:
        return None
    return Fact("+".join(t for t, _ in found), ", ".join(s for _, s in found))


def _ci(root: Path) -> Fact:
    workflow = next(iter(sorted(root.glob(".github/workflows/*.y*ml"))), None)
    if workflow:
        return Fact("github-actions", workflow.relative_to(root).as_posix())
    if (root / ".gitlab-ci.yml").exists():
        return Fact("gitlab-ci", ".gitlab-ci.yml")
    return Fact("none", "not found")


def detect(root: Path, *, available: Collection[str], interpreter: str) -> dict[str, Fact]:
    """Collect project facts; `available` names the tools found on PATH or in .venv."""
    pyproject = _load_pyproject(root)
    dependencies = _dependency_names(pyproject)
    default = Fact
    runner = _runner(root, pyproject) or default("uv", "default")
    test, import_mode = _pytest(root, pyproject, dependencies)
    types = _tools_in_use(root, pyproject, dependencies, TYPE_CHECKERS) or default("mypy", "default")
    lint = _tools_in_use(root, pyproject, dependencies, LINTERS) or default("ruff", "default")
    plugins = sorted(set(ASYNC_PLUGINS) & dependencies)
    declared = {
        tool
        for fact in (runner, test, types, lint)
        if fact.source != "default"
        for tool in fact.value.split("+")
    } & set(TOOLS)
    missing = sorted(declared - set(available))
    return {
        "python.target": _python_target(pyproject) or default("3.12", "default"),
        "python.interpreter": Fact(interpreter, "running interpreter"),
        "runner": runner,
        "layout": _layout(root) or default("src", "default"),
        "backend": _backend(pyproject) or default("hatchling", "default"),
        "test": test,
        "test.import_mode": import_mode,
        "types": types,
        "lint": lint,
        "async": Fact("+".join(plugins), "dependencies") if plugins else Fact("none", "not found"),
        "ci": _ci(root),
        "tools.available": Fact(",".join(sorted(available)) or "none", ""),
        "tools.missing": Fact(
            ",".join(missing) or "none", "declared, not on PATH or .venv/bin" if missing else ""
        ),
    }


def render(facts: Mapping[str, Fact]) -> str:
    return "".join(
        f"{key}={fact.value}" + (f"  # {fact.source}" if fact.source else "") + "\n"
        for key, fact in facts.items()
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    root = Path(args[0]) if args else Path.cwd()
    if not root.is_dir():
        sys.stderr.write(f"error: {root} is not a directory\n")
        return 2
    available = frozenset(
        tool for tool in TOOLS if shutil.which(tool) or (root / ".venv" / "bin" / tool).exists()
    )
    version = sys.version_info
    try:
        facts = detect(
            root,
            available=available,
            interpreter=f"{version.major}.{version.minor}.{version.micro}",
        )
    except tomllib.TOMLDecodeError as error:
        sys.stderr.write(f"error: pyproject.toml is not valid TOML: {' '.join(str(error).split())}\n")
        return 1
    sys.stdout.write(render(facts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
