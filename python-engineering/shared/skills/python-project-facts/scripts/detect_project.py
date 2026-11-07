"""Print a Python project's version, tooling, kind and installed tools as key=value lines.

Needs Python 3.11+ and the standard library only. It lives in the python-project-facts skill and the
other python-* skills run it; `kind=<kind>` as an argument overrides the detected kind.
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

# Bundle name -> skills in it. check_skills.py keeps this equal to the repository layout.
BUNDLES: Mapping[str, tuple[str, ...]] = {
    "core": (
        "writing-python-code", "avoiding-code-snags", "choosing-python-design-patterns",
        "testing-python-packages", "reviewing-python-changes", "profiling-python-code",
        "writing-python-scripts-and-clis", "auditing-python-dependencies", "managing-python-resources",
        "typing-python-code", "using-uv",
    ),
    "library": ("designing-package-apis", "setting-up-python-packages", "releasing-python-packages"),
    "application": ("building-python-web-services", "writing-async-python", "running-background-jobs"),
    "native-extension": (),
    "data-engineering": (),
    "machine-learning": (),
    "ai-applications": (),
    "data-analysis": (),
    "scientific-computing": (),
    "automation-and-scraping": (),
    "legacy-and-migration": (),
    "agent-tooling": (),
    "cli-and-distribution": (),
    "security-hardening": (),
}  # fmt: skip
# Kind -> bundles recommended on top of core, in the order they are listed.
KIND_BUNDLES: Mapping[str, tuple[str, ...]] = {
    "extension": ("native-extension", "library"),
    "mcp-server": ("agent-tooling",),
    "application": ("application",),
    "llm-app": ("ai-applications",),
    "ml": ("machine-learning",),
    "data-pipeline": ("data-engineering",),
    "scraper": ("automation-and-scraping",),
    "cli": ("cli-and-distribution", "library"),
    "notebook": ("data-analysis",),
    "library": ("library",),
    "script": (),
    "unknown": (),
}
WEB = frozenset({"fastapi", "django", "flask", "starlette", "litestar", "aiohttp", "sanic", "tornado", "quart", "uvicorn", "gunicorn", "hypercorn"})  # fmt: skip
MCP = frozenset({"mcp", "fastmcp"})
LLM = frozenset({"anthropic", "openai", "langchain", "langchain-core", "litellm", "llama-index", "google-genai", "cohere", "mistralai"})  # fmt: skip
ML = frozenset({"torch", "tensorflow", "scikit-learn", "sklearn", "jax", "xgboost", "lightgbm", "catboost", "keras", "transformers"})  # fmt: skip
DATA = frozenset({"apache-airflow", "airflow", "dagster", "prefect", "dbt-core", "pyspark", "luigi", "kedro", "duckdb", "great-expectations", "apache-beam"})  # fmt: skip
SCRAPER = frozenset({"playwright", "scrapy", "beautifulsoup4", "selenium", "mechanicalsoup"})
CLI_LIBRARIES = frozenset({"typer", "click", "rich-click", "textual", "cyclopts", "fire", "cleo"})
NOTEBOOK = frozenset({"jupyter", "jupyterlab", "notebook", "ipykernel", "nbformat"})
EXTENSION_BUILD = frozenset({"maturin", "scikit-build-core", "meson-python", "setuptools-rust", "cython", "pybind11", "nanobind"})  # fmt: skip
SKIP_DIRS = frozenset({"node_modules", "__pycache__", "build", "dist", "target", "site-packages"})


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


def _files(root: Path, depth: int = 3) -> list[Path]:
    """List files up to `depth` folders down, skipping hidden, build and dependency folders."""
    found: list[Path] = []
    stack = [(root, 0)]
    while stack:
        folder, level = stack.pop()
        try:
            entries = sorted(folder.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.is_symlink():
                continue
            if entry.is_dir():
                if level < depth and not entry.name.startswith(".") and entry.name not in SKIP_DIRS:
                    stack.append((entry, level + 1))
            else:
                found.append(entry)
    return found


def _text(path: Path) -> str:
    try:
        return path.read_text(errors="ignore")
    except OSError:
        return ""


def _extension_signal(root: Path, pyproject: Mapping[str, object], files: list[Path]) -> str | None:
    requires = _get(pyproject, "build-system", "requires")
    if isinstance(requires, list):
        names = {_requirement_name(item) for item in requires if isinstance(item, str)}
        if hit := sorted(names & EXTENSION_BUILD):
            return f"build-system requires {hit[0]}"
    if "pyo3" in _text(root / "Cargo.toml"):
        return "Cargo.toml with pyo3"
    if pyx := next((f for f in files if f.suffix == ".pyx"), None):
        return pyx.relative_to(root).as_posix()
    cmake = _text(root / "CMakeLists.txt")
    for name in ("nanobind", "pybind11"):
        if name in cmake:
            return f"CMakeLists.txt with {name}"
    if "extension_module" in _text(root / "meson.build"):
        return "meson.build extension_module"
    if "ext_modules" in _text(root / "setup.py"):
        return "setup.py ext_modules"
    return None


def _script_signal(root: Path) -> str | None:
    scripts = [f for f in sorted(root.glob("*.py"))]
    for script in scripts:
        if "# /// script" in _text(script)[:2000]:
            return f"{script.name} has a PEP 723 header"
    return scripts[0].name if scripts else None


def _kinds(root: Path, pyproject: Mapping[str, object], dependencies: set[str]) -> list[Fact]:
    """Every kind of project that matches, most specific first; the first is the primary kind."""
    files = _files(root)
    found: list[Fact] = []

    def dependency(kind: str, names: frozenset[str]) -> None:
        if hit := sorted(names & dependencies):
            found.append(Fact(kind, f"dependency {hit[0]}"))

    if signal := _extension_signal(root, pyproject, files):
        found.append(Fact("extension", signal))
    dependency("mcp-server", MCP)
    if web := sorted(WEB & dependencies):
        found.append(Fact("application", f"dependency {web[0]}"))
    elif (root / "manage.py").is_file():
        found.append(Fact("application", "manage.py"))
    dependency("llm-app", LLM)
    dependency("ml", ML)
    dependency("data-pipeline", DATA)
    dependency("scraper", SCRAPER)
    entry_points = _get(pyproject, "project", "scripts") or _get(pyproject, "project", "gui-scripts")
    if entry_points and (cli := sorted(CLI_LIBRARIES & dependencies)):
        found.append(Fact("cli", f"[project.scripts] with {cli[0]}"))
    has_project = isinstance(_get(pyproject, "project"), Mapping)
    has_build = _get(pyproject, "build-system") is not None
    notebook = next((f for f in files if f.suffix == ".ipynb"), None)
    if not has_build and (jupyter := sorted(NOTEBOOK & dependencies)):
        found.append(Fact("notebook", f"dependency {jupyter[0]}"))
    elif not has_build and notebook:
        found.append(Fact("notebook", notebook.relative_to(root).as_posix()))
    is_application = any(fact.value == "application" for fact in found)
    if has_project and has_build and not is_application:
        found.append(Fact("library", "[project] with a build backend"))
    if not found and has_project:
        found.append(Fact("application", "[project] without a build backend"))
    if not found and (signal := _script_signal(root)):
        found.append(Fact("script", signal))
    return found or [Fact("unknown", "no project files found")]


def _bundles(kinds: Sequence[str]) -> list[str]:
    bundles = ["core"]
    for kind in kinds:
        bundles.extend(b for b in KIND_BUNDLES.get(kind, ()) if b not in bundles)
    return bundles


def _missing_skills(bundles: Sequence[str], installed: Collection[str] | None) -> Fact:
    if installed is None:
        return Fact("unknown", "not run from an installed skill")
    parts = [
        f"{bundle}[{','.join(missing)}]"
        for bundle in bundles
        if (missing := [skill for skill in BUNDLES.get(bundle, ()) if skill not in installed])
    ]
    return Fact(";".join(parts) or "none", "recommended skills that are not installed" if parts else "")


def installed_skills(script: Path) -> frozenset[str] | None:
    """Skill folders next to this script's skill, flat or under <bundle>/skills; None outside a skill."""
    skill = script.resolve().parent.parent
    if script.resolve().parent.name != "scripts" or not (skill / "SKILL.md").is_file():
        return None
    names = {p.name for p in skill.parent.iterdir() if (p / "SKILL.md").is_file()}
    for bundle in skill.parent.iterdir():
        skills = bundle / "skills"
        if skills.is_dir():
            names.update(p.name for p in skills.iterdir() if (p / "SKILL.md").is_file())
    return frozenset(names)


def detect(
    root: Path,
    *,
    available: Collection[str],
    interpreter: str,
    installed: Collection[str] | None = None,
    kind: str | None = None,
) -> dict[str, Fact]:
    """Collect project facts; `available` names the tools found on PATH or in .venv.

    `installed` names the skills next to this one (None when unknown); `kind` overrides detection.
    """
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
    kinds = [Fact(kind, "kind= argument")] if kind else _kinds(root, pyproject, dependencies)
    bundles = _bundles([fact.value for fact in kinds])
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
        "kind": kinds[0],
        "kinds": Fact(",".join(fact.value for fact in kinds), ""),
        "bundles": Fact(",".join(bundles), ""),
        "bundles.missing": _missing_skills(bundles, installed),
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
    override = next((arg.partition("=")[2] for arg in args if arg.startswith("kind=")), None)
    args = [arg for arg in args if not arg.startswith("kind=")]
    if override is not None and override not in KIND_BUNDLES:
        sys.stderr.write(f"error: kind={override} is not one of {', '.join(KIND_BUNDLES)}\n")
        return 2
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
            installed=installed_skills(Path(__file__)),
            kind=override,
        )
    except tomllib.TOMLDecodeError as error:
        sys.stderr.write(f"error: pyproject.toml is not valid TOML: {' '.join(str(error).split())}\n")
        return 1
    sys.stdout.write(render(facts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
