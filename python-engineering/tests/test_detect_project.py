from collections.abc import Mapping
from pathlib import Path

import pytest
from detect_project import BUNDLES, KIND_BUNDLES, Fact, detect, main, render

HATCH_PYPROJECT = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "x"
version = "0.1.0"
requires-python = ">=3.12"
"""


def write_files(root: Path, files: Mapping[str, str]) -> Path:
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return root


def detect_in(
    root: Path,
    files: Mapping[str, str],
    *,
    available: frozenset[str] = frozenset(),
) -> dict[str, Fact]:
    write_files(root, files)
    return detect(root, available=available, interpreter="3.13.1")


def test_uv_project_reports_each_fact_with_its_source(tmp_path: Path) -> None:
    facts = detect_in(
        tmp_path,
        {"pyproject.toml": HATCH_PYPROJECT, "uv.lock": "", "src/x/__init__.py": ""},
    )

    assert facts["python.target"] == Fact("3.12", 'requires-python ">=3.12"')
    assert facts["python.interpreter"] == Fact("3.13.1", "running interpreter")
    assert facts["runner"] == Fact("uv", "uv.lock")
    assert facts["layout"] == Fact("src", "src/x/__init__.py")
    assert facts["backend"] == Fact("hatchling", "hatchling.build")


def test_empty_directory_falls_back_to_defaults(tmp_path: Path) -> None:
    facts = detect_in(tmp_path, {})

    defaults = {
        "python.target": "3.12",
        "runner": "uv",
        "layout": "src",
        "backend": "hatchling",
        "test": "pytest",
        "test.import_mode": "prepend",
        "types": "mypy",
        "lint": "ruff",
    }
    assert {key: facts[key] for key in defaults} == {
        key: Fact(value, "default") for key, value in defaults.items()
    }
    assert facts["async"] == Fact("none", "not found")
    assert facts["ci"] == Fact("none", "not found")
    assert facts["tools.missing"].value == "none"


@pytest.mark.parametrize(
    ("spec", "target"),
    [
        (">=3.10", "3.10"),
        (">=3.10,<4", "3.10"),
        ("~=3.11.2", "3.11"),
        (">=3.9.1", "3.9"),
        ("==3.12.*", "3.12"),
        (">3.9", "3.9"),
    ],
)
def test_python_target_is_the_lower_bound_of_requires_python(
    tmp_path: Path, spec: str, target: str
) -> None:
    pyproject = f'[project]\nname = "x"\nversion = "0"\nrequires-python = "{spec}"\n'

    facts = detect_in(tmp_path, {"pyproject.toml": pyproject})

    assert facts["python.target"].value == target


def test_poetry_caret_python_constraint_sets_the_target(tmp_path: Path) -> None:
    pyproject = '[tool.poetry.dependencies]\npython = "^3.10"\n'

    facts = detect_in(tmp_path, {"pyproject.toml": pyproject})

    assert facts["python.target"] == Fact("3.10", 'tool.poetry python "^3.10"')


@pytest.mark.parametrize(
    ("files", "runner", "source"),
    [
        ({"uv.lock": ""}, "uv", "uv.lock"),
        ({"poetry.lock": ""}, "poetry", "poetry.lock"),
        ({"pdm.lock": ""}, "pdm", "pdm.lock"),
        ({"pyproject.toml": "[tool.uv]\npackage = true\n"}, "uv", "[tool.uv]"),
        ({"pyproject.toml": '[tool.poetry]\nname = "x"\n'}, "poetry", "[tool.poetry]"),
        ({"pyproject.toml": "[tool.pdm]\n"}, "pdm", "[tool.pdm]"),
        ({"hatch.toml": ""}, "hatch", "hatch.toml"),
        ({"pyproject.toml": "[tool.hatch.envs.default]\n"}, "hatch", "[tool.hatch.envs]"),
        ({"requirements.txt": "pytest\n"}, "pip", "requirements.txt"),
        (
            {"uv.lock": "", "pyproject.toml": '[tool.poetry]\nname = "x"\n'},
            "uv",
            "uv.lock",
        ),
    ],
    ids=[
        "uv-lock", "poetry-lock", "pdm-lock", "uv-table", "poetry-table",
        "pdm-table", "hatch-toml", "hatch-envs", "requirements", "lockfile-beats-table",
    ],
)
def test_runner_comes_from_lockfile_then_tool_table_then_requirements(
    tmp_path: Path, files: Mapping[str, str], runner: str, source: str
) -> None:
    facts = detect_in(tmp_path, files)

    assert facts["runner"] == Fact(runner, source)


def test_src_layout_needs_a_package_under_src(tmp_path: Path) -> None:
    facts = detect_in(tmp_path, {"src/pkg/__init__.py": ""})

    assert facts["layout"] == Fact("src", "src/pkg/__init__.py")


def test_package_at_the_root_is_flat_layout(tmp_path: Path) -> None:
    facts = detect_in(tmp_path, {"pyproject.toml": "", "pkg/__init__.py": "", "tests/__init__.py": ""})

    assert facts["layout"] == Fact("flat", "pkg/__init__.py at root")


@pytest.mark.parametrize(
    ("build_backend", "name"),
    [
        ("hatchling.build", "hatchling"),
        ("setuptools.build_meta", "setuptools"),
        ("poetry.core.masonry.api", "poetry-core"),
        ("pdm.backend", "pdm-backend"),
        ("flit_core.buildapi", "flit-core"),
        ("uv_build", "uv_build"),
        ("some.other.backend", "some.other.backend"),
    ],
)
def test_backend_name_comes_from_build_backend(
    tmp_path: Path, build_backend: str, name: str
) -> None:
    pyproject = f'[build-system]\nrequires = []\nbuild-backend = "{build_backend}"\n'

    facts = detect_in(tmp_path, {"pyproject.toml": pyproject})

    assert facts["backend"] == Fact(name, build_backend)


def test_pytest_import_mode_is_read_from_pyproject_addopts(tmp_path: Path) -> None:
    pyproject = '[tool.pytest.ini_options]\naddopts = "-ra --import-mode=importlib"\n'

    facts = detect_in(tmp_path, {"pyproject.toml": pyproject})

    assert facts["test"] == Fact("pytest", "[tool.pytest.ini_options]")
    assert facts["test.import_mode"] == Fact("importlib", "addopts")


def test_pytest_import_mode_is_read_from_pytest_ini(tmp_path: Path) -> None:
    ini = "[pytest]\naddopts = --import-mode=importlib\n"

    facts = detect_in(tmp_path, {"pytest.ini": ini})

    assert facts["test"] == Fact("pytest", "pytest.ini")
    assert facts["test.import_mode"] == Fact("importlib", "addopts")


@pytest.mark.parametrize(
    ("files", "types"),
    [
        ({"pyproject.toml": "[tool.mypy]\nstrict = true\n"}, "mypy"),
        ({"mypy.ini": "[mypy]\n"}, "mypy"),
        ({"pyrightconfig.json": "{}"}, "pyright"),
        ({"pyproject.toml": "[tool.pyright]\n"}, "pyright"),
        ({"pyproject.toml": "[tool.pyright]\n[tool.mypy]\n"}, "mypy+pyright"),
        (
            {"pyproject.toml": '[dependency-groups]\ndev = ["pyright>=1.1"]\n'},
            "pyright",
        ),
        ({"pyproject.toml": "[tool.mypy]\n[tool.ty]\n"}, "mypy+ty"),
        ({"pyrefly.toml": ""}, "pyrefly"),
        ({"pyproject.toml": "[tool.basedpyright]\n"}, "basedpyright"),
    ],
    ids=[
        "mypy-table", "mypy-ini", "pyright-json", "pyright-table", "both", "dependency-only",
        "mypy-and-ty", "pyrefly-toml", "basedpyright-table",
    ],
)
def test_type_checker_is_detected_from_config_or_dependencies(
    tmp_path: Path, files: Mapping[str, str], types: str
) -> None:
    facts = detect_in(tmp_path, files)

    assert facts["types"].value == types
    assert facts["types"].source != "default"


@pytest.mark.parametrize(
    ("files", "lint"),
    [
        ({"pyproject.toml": "[tool.ruff]\n"}, "ruff"),
        ({"ruff.toml": ""}, "ruff"),
        ({".flake8": "[flake8]\n", "pyproject.toml": "[tool.black]\n"}, "flake8+black"),
        ({"pyproject.toml": '[tool.poetry.group.dev.dependencies]\npylint = "^3"\n'}, "pylint"),
    ],
    ids=["ruff-table", "ruff-toml", "flake8-black", "poetry-group-dependency"],
)
def test_linters_are_detected_in_a_fixed_order(
    tmp_path: Path, files: Mapping[str, str], lint: str
) -> None:
    facts = detect_in(tmp_path, files)

    assert facts["lint"].value == lint
    assert facts["lint"].source != "default"


def test_async_test_plugins_come_from_dependencies(tmp_path: Path) -> None:
    pyproject = '[dependency-groups]\ndev = ["pytest>=8", "pytest-asyncio>=0.23", "anyio"]\n'

    facts = detect_in(tmp_path, {"pyproject.toml": pyproject})

    assert facts["async"].value == "anyio+pytest-asyncio"


@pytest.mark.parametrize(
    ("path", "ci"),
    [(".github/workflows/ci.yml", "github-actions"), (".gitlab-ci.yml", "gitlab-ci")],
)
def test_ci_system_is_detected_from_its_config_file(tmp_path: Path, path: str, ci: str) -> None:
    facts = detect_in(tmp_path, {path: ""})

    assert facts["ci"] == Fact(ci, path)


def test_declared_tools_missing_from_path_are_listed(tmp_path: Path) -> None:
    pyproject = '[tool.poetry]\nname = "x"\n[tool.mypy]\nstrict = true\n'

    facts = detect_in(tmp_path, {"pyproject.toml": pyproject}, available=frozenset({"poetry"}))

    assert facts["tools.available"].value == "poetry"
    assert facts["tools.missing"].value == "mypy"


def test_default_tools_are_not_reported_missing(tmp_path: Path) -> None:
    facts = detect_in(tmp_path, {}, available=frozenset())

    assert facts["tools.missing"].value == "none"


def test_render_prints_key_value_with_source_comment() -> None:
    facts = {"runner": Fact("uv", "uv.lock"), "tools.available": Fact("pytest,uv", "")}

    assert render(facts) == "runner=uv  # uv.lock\ntools.available=pytest,uv\n"


def test_main_prints_facts_for_the_given_directory(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    write_files(tmp_path, {"uv.lock": "", ".venv/bin/mypy": ""})
    monkeypatch.setattr("detect_project.shutil.which", lambda _name: None)

    assert main([str(tmp_path)]) == 0

    out = capsys.readouterr().out
    assert "runner=uv  # uv.lock\n" in out
    assert "tools.available=mypy\n" in out


def test_main_reports_complexity_tools_found_in_the_venv(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    write_files(tmp_path, {".venv/bin/xenon": "", ".venv/bin/radon": ""})
    monkeypatch.setattr("detect_project.shutil.which", lambda _name: None)

    assert main([str(tmp_path)]) == 0

    assert "tools.available=radon,xenon\n" in capsys.readouterr().out


def test_main_reports_invalid_toml_on_one_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_files(tmp_path, {"pyproject.toml": "[project\n"})

    assert main([str(tmp_path)]) == 1

    err = capsys.readouterr().err
    assert err.startswith("error: pyproject.toml is not valid TOML")
    assert err.count("\n") == 1


def test_main_rejects_a_directory_that_does_not_exist(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "nope"

    assert main([str(missing)]) == 2

    assert f"error: {missing} is not a directory" in capsys.readouterr().err


# ---------------------------------------------------------------------------- kind and bundles
NO_BACKEND = """\
[project]
name = "x"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [{deps}]
"""


def with_deps(*names: str) -> str:
    return NO_BACKEND.format(deps=", ".join(f'"{name}"' for name in names))


def backend(name: str) -> str:
    return f'[build-system]\nrequires = ["{name}"]\nbuild-backend = "{name}"\n\n' + with_deps()


@pytest.mark.parametrize(
    ("files", "kind", "source_part"),
    [
        ({"pyproject.toml": HATCH_PYPROJECT}, "library", "build backend"),
        ({"pyproject.toml": with_deps()}, "application", "without a build backend"),
        ({"pyproject.toml": with_deps("fastapi", "uvicorn")}, "application", "fastapi"),
        ({"manage.py": "", "pyproject.toml": HATCH_PYPROJECT}, "application", "manage.py"),
        ({"pyproject.toml": with_deps("mcp")}, "mcp-server", "mcp"),
        ({"pyproject.toml": with_deps("fastmcp")}, "mcp-server", "fastmcp"),
        ({"pyproject.toml": with_deps("anthropic")}, "llm-app", "anthropic"),
        ({"pyproject.toml": with_deps("torch")}, "ml", "torch"),
        ({"pyproject.toml": with_deps("scikit-learn")}, "ml", "scikit-learn"),
        ({"pyproject.toml": with_deps("apache-airflow")}, "data-pipeline", "apache-airflow"),
        ({"pyproject.toml": with_deps("dagster")}, "data-pipeline", "dagster"),
        ({"pyproject.toml": with_deps("playwright")}, "scraper", "playwright"),
        ({"pyproject.toml": with_deps("scrapy")}, "scraper", "scrapy"),
        ({"pyproject.toml": HATCH_PYPROJECT + '\n[project.scripts]\nx = "x:main"\n'}, "library", "build backend"),
        ({"analysis.ipynb": "{}"}, "notebook", "analysis.ipynb"),
        ({"pyproject.toml": with_deps("jupyterlab")}, "notebook", "jupyterlab"),
        ({"tool.py": "print(1)\n"}, "script", "tool.py"),
        ({"run.py": "# /// script\n# dependencies = []\n# ///\nprint(1)\n"}, "script", "PEP 723"),
        ({}, "unknown", ""),
    ],
)
def test_kind_is_the_first_matching_signal(
    tmp_path: Path, files: dict[str, str], kind: str, source_part: str
) -> None:
    facts = detect_in(tmp_path, files)

    assert facts["kind"].value == kind
    assert source_part in facts["kind"].source


@pytest.mark.parametrize(
    "files",
    [
        {"pyproject.toml": backend("maturin")},
        {"pyproject.toml": HATCH_PYPROJECT, "Cargo.toml": '[dependencies]\npyo3 = "0.30"\n'},
        {"pyproject.toml": HATCH_PYPROJECT, "src/x/fast.pyx": ""},
        {"pyproject.toml": HATCH_PYPROJECT, "CMakeLists.txt": "find_package(nanobind CONFIG REQUIRED)\n"},
        {"pyproject.toml": HATCH_PYPROJECT, "CMakeLists.txt": "find_package(pybind11 CONFIG REQUIRED)\n"},
        {"pyproject.toml": HATCH_PYPROJECT, "meson.build": "py.extension_module('x', 'x.c')\n"},
        {"pyproject.toml": HATCH_PYPROJECT, "setup.py": "setup(ext_modules=[Extension('x', ['x.c'])])\n"},
    ],
)
def test_native_extension_signals_win_over_library(tmp_path: Path, files: dict[str, str]) -> None:
    facts = detect_in(tmp_path, files)

    assert facts["kind"].value == "extension"


def test_cli_needs_scripts_and_a_cli_library(tmp_path: Path) -> None:
    pyproject = HATCH_PYPROJECT + 'dependencies = ["typer"]\n\n[project.scripts]\nx = "x:main"\n'
    facts = detect_in(tmp_path, {"pyproject.toml": pyproject})

    assert facts["kind"].value == "cli"
    assert "typer" in facts["kind"].source


def test_hidden_and_build_directories_are_not_searched_for_extensions(tmp_path: Path) -> None:
    facts = detect_in(
        tmp_path,
        {"pyproject.toml": HATCH_PYPROJECT, ".venv/lib/pkg/fast.pyx": "", "node_modules/p/fast.pyx": ""},
    )

    assert facts["kind"].value == "library"


def test_a_project_can_be_several_kinds_and_bundles_are_the_union(tmp_path: Path) -> None:
    facts = detect_in(tmp_path, {"pyproject.toml": with_deps("fastapi", "torch")})

    assert facts["kind"].value == "application"
    assert facts["kinds"].value == "application,ml"
    assert facts["bundles"].value == "core,application,machine-learning"


@pytest.mark.parametrize(
    ("files", "bundles"),
    [
        ({"tool.py": ""}, "core"),
        ({"pyproject.toml": HATCH_PYPROJECT}, "core,library"),
        ({"pyproject.toml": backend("maturin")}, "core,native-extension,library"),
        ({}, "core"),
    ],
)
def test_bundles_always_start_with_core(tmp_path: Path, files: dict[str, str], bundles: str) -> None:
    assert detect_in(tmp_path, files)["bundles"].value == bundles


def test_every_kind_maps_to_bundles_that_exist() -> None:
    known = set(BUNDLES)
    for kind, bundles in KIND_BUNDLES.items():
        assert set(bundles) <= known, kind


def test_missing_skills_are_listed_per_bundle(tmp_path: Path) -> None:
    write_files(tmp_path, {"pyproject.toml": HATCH_PYPROJECT})
    installed = set(BUNDLES["core"]) | set(BUNDLES["library"][:-1])

    facts = detect(tmp_path, available=frozenset(), interpreter="3.13.1", installed=installed)

    assert facts["bundles.missing"].value == f"library[{BUNDLES['library'][-1]}]"


def test_nothing_is_missing_when_every_recommended_skill_is_installed(tmp_path: Path) -> None:
    write_files(tmp_path, {"pyproject.toml": HATCH_PYPROJECT})
    installed = set(BUNDLES["core"]) | set(BUNDLES["library"])

    facts = detect(tmp_path, available=frozenset(), interpreter="3.13.1", installed=installed)

    assert facts["bundles.missing"].value == "none"


def test_missing_skills_are_unknown_when_not_run_from_a_skills_folder(tmp_path: Path) -> None:
    facts = detect_in(tmp_path, {"pyproject.toml": HATCH_PYPROJECT})

    assert facts["bundles.missing"] == Fact("unknown", "not run from an installed skill")


def test_kind_argument_overrides_detection(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    write_files(tmp_path, {"pyproject.toml": HATCH_PYPROJECT})

    assert main(["kind=ml", str(tmp_path)]) == 0

    out = capsys.readouterr().out
    assert "kind=ml  # kind= argument\n" in out
    assert "bundles=core,machine-learning\n" in out


def test_unknown_kind_argument_is_rejected(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["kind=banana", str(tmp_path)]) == 2

    err = capsys.readouterr().err
    assert err.startswith("error: kind=banana is not one of")
    assert "library" in err
