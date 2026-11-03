from collections.abc import Mapping
from pathlib import Path

import pytest
from detect_project import Fact, detect, main, render

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
    ],
    ids=["mypy-table", "mypy-ini", "pyright-json", "pyright-table", "both", "dependency-only"],
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
