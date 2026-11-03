from pathlib import Path

import detect_project as dp
import pytest

BUNDLE = """\
bundle:
  name: demo

targets:
  dev:
    mode: development
    default: true
    variables:
      catalog: dev
  prod:
    mode: production
"""


def write(root: Path, name: str, text: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_bundle_targets_and_default_target_are_read(tmp_path: Path) -> None:
    write(tmp_path, "databricks.yml", BUNDLE)

    facts = dp.bundle_facts(tmp_path)

    assert facts["bundle.targets"].value == "dev,prod"
    assert facts["bundle.default_target"].value == "dev"


def test_missing_bundle_reports_none_with_default_comment(tmp_path: Path) -> None:
    facts = dp.bundle_facts(tmp_path)

    assert facts["bundle"] == dp.Fact("none", "# default: no databricks.yml in this folder")


def test_targets_block_ignores_nested_keys_and_comments(tmp_path: Path) -> None:
    write(tmp_path, "databricks.yml", "targets:\n  # staging soon\n  dev:\n    workspace:\n      host: x\ninclude:\n  - a\n")

    assert dp.bundle_facts(tmp_path)["bundle.targets"].value == "dev"


@pytest.mark.parametrize(
    ("yaml_text", "expected"),
    [
        ("resources:\n  jobs:\n    j:\n      environments:\n        - environment_key: default\n", "serverless"),
        ("new_cluster:\n  spark_version: 17.3.x-scala2.13\n", "classic"),
        ("spark_version: 17.3.x-scala2.13\nenvironment_key: default\n", "mixed"),
        ("pipelines:\n  p:\n    serverless: true\n", "serverless"),
    ],
    ids=["environment-key", "spark-version", "both", "serverless-pipeline"],
)
def test_compute_kind_is_detected_from_resource_yaml(tmp_path: Path, yaml_text: str, expected: str) -> None:
    write(tmp_path, "resources/job.yml", yaml_text)

    assert dp.compute_facts(tmp_path)["compute"].value == expected


def test_runtime_and_environment_versions_are_collected(tmp_path: Path) -> None:
    write(tmp_path, "resources/a.yml", "spark_version: '17.3.x-scala2.13'\n")
    write(tmp_path, "resources/b.yml", 'environment_version: "4"\n')

    facts = dp.compute_facts(tmp_path)

    assert facts["runtime"].value == "17.3.x-scala2.13"
    assert facts["serverless.environment_version"].value == "4"


def test_both_spark_clients_declared_is_a_conflict(tmp_path: Path) -> None:
    write(
        tmp_path,
        "pyproject.toml",
        '[project]\nname = "x"\ndependencies = []\n'
        '[dependency-groups]\ndev = ["databricks-connect~=17.3.0", "pyspark>=4"]\n',
    )

    assert dp.spark_client_facts(tmp_path)["spark.client"].value == "conflict"


def test_spark_in_runtime_dependencies_is_flagged(tmp_path: Path) -> None:
    write(tmp_path, "pyproject.toml", '[project]\nname = "x"\ndependencies = ["pyspark==4.1.0", "pydantic"]\n')

    facts = dp.spark_client_facts(tmp_path)

    assert facts["spark.client"].value == "pyspark"
    assert facts["spark.in_runtime_deps"].value == "pyspark"


def test_legacy_dlt_import_is_reported(tmp_path: Path) -> None:
    write(tmp_path, "src/p/bronze.py", "import dlt\n\n@dlt.table\ndef t():\n    return None\n")
    write(tmp_path, "src/p/silver.py", "from pyspark import pipelines as dp\n")

    facts = dp.code_facts(tmp_path)

    assert facts["pipelines.files"].value == "2"
    assert facts["pipelines.api"].value == "dlt"


def test_notebooks_counts_ipynb_and_source_format(tmp_path: Path) -> None:
    write(tmp_path, "a.ipynb", "{}")
    write(tmp_path, "b.py", "# Databricks notebook source\nprint(1)\n")
    write(tmp_path, "c.py", "x = 1\n")
    write(tmp_path, ".venv/lib/d.ipynb", "{}")

    assert dp.code_facts(tmp_path)["notebooks"].value == "2"


def test_sql_pipeline_definitions_are_counted(tmp_path: Path) -> None:
    write(tmp_path, "t.sql", "CREATE OR REFRESH STREAMING TABLE bronze AS SELECT * FROM STREAM read_files('/x')")

    assert dp.code_facts(tmp_path)["pipelines.files"].value == "1"


def test_python_target_comes_from_requires_python(tmp_path: Path) -> None:
    write(tmp_path, "pyproject.toml", '[project]\nname = "x"\nrequires-python = ">=3.11,<3.13"\n')

    assert dp.python_facts(tmp_path)["python.target"].value == "3.11"


def test_render_appends_source_comment() -> None:
    rendered = dp.render({"a": dp.Fact("1", ""), "b": dp.Fact("2", "# default")})

    assert rendered == "a=1\nb=2  # default\n"


def test_main_rejects_missing_directory(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code = dp.main([str(tmp_path / "missing")])

    assert code == 2
    assert "is not a directory" in capsys.readouterr().err
