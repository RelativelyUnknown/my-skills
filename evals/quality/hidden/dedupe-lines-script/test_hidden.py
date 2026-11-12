import subprocess
import sys
from pathlib import Path

SCRIPT = Path("tools/dedupe.py")


def run(path, *args):
    return subprocess.run([sys.executable, str(SCRIPT), str(path), *args], capture_output=True, text=True)


def test_removes_duplicates_keeping_first(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("b\na\nb\nc\na\n")
    assert run(f).returncode == 0
    assert f.read_text() == "b\na\nc\n"


def test_dry_run_changes_nothing_and_reports(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("x\ny\nx\n")
    r = run(f, "--dry-run")
    assert r.returncode == 0
    assert f.read_text() == "x\ny\nx\n"
    assert "x" in r.stdout


def test_unicode_and_no_trailing_newline(tmp_path):
    f = tmp_path / "u.txt"
    f.write_bytes("é\nz\né".encode())
    assert run(f).returncode == 0
    assert f.read_bytes().decode().split("\n")[:2] == ["é", "z"]
    assert f.read_bytes().decode().count("é") == 1


def test_empty_file_ok(tmp_path):
    f = tmp_path / "e.txt"
    f.write_text("")
    assert run(f).returncode == 0
    assert f.read_text() == ""


def test_missing_file_fails_cleanly(tmp_path):
    r = run(tmp_path / "nope.txt")
    assert r.returncode != 0
    assert "Traceback" not in r.stderr
