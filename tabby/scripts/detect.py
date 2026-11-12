#!/usr/bin/env python3
"""detect.py: print the facts a Python task needs from the repo, in about ten lines. Reads files only; runs nothing.

    python3 detect.py [PROJECT_DIR]

Runner, build backend, Python target, tests, formatter and linter, type checker, the project's check command, CI, docs tool,
native extension, and whether AGENTS.md has a `## Tabby` or `## Python defaults` section. A line says `none found` rather than
guessing. Stdlib only; Python 3.11 or later for tomllib (older: the pyproject lines are skipped).
"""
import pathlib, re, sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()


def has(*names):
    return [n for n in names if (root / n).exists()]


def text(name):
    try:
        return (root / name).read_text(errors="ignore")
    except OSError:
        return ""


try:
    import tomllib
    py = tomllib.loads(text("pyproject.toml")) if has("pyproject.toml") else {}
except Exception:
    py = {}
tool = py.get("tool", {})
proj = py.get("project", {})
cfg_text = "\n".join(text(n) for n in ("pyproject.toml", "setup.cfg", "tox.ini", ".pre-commit-config.yaml", "Makefile", "justfile"))
ci_text = "\n".join(p.read_text(errors="ignore") for p in list((root / ".github/workflows").glob("*.y*ml")) + [root / ".gitlab-ci.yml"] if p.exists())
all_text = cfg_text + "\n" + ci_text


def lines():
    runner = []
    for f, n in (("uv.lock", "uv"), ("poetry.lock", "poetry"), ("pdm.lock", "pdm"), ("Pipfile", "pipenv"), ("pixi.toml", "pixi"), ("environment.yml", "conda")):
        if has(f):
            runner.append(n)
    if "poetry" in tool and "poetry" not in runner:
        runner.append("poetry")
    if "hatch" in tool and (tool["hatch"] or {}).get("envs"):
        runner.append("hatch")
    if not runner and (list(root.glob("requirements*.txt")) or has("setup.py")):
        runner.append("pip")
    note = "  (two runners: ask which is current)" if len(runner) > 1 else ""
    yield "runner: " + (", ".join(runner) or "none found") + note
    backend = (py.get("build-system") or {}).get("build-backend", "")
    yield "build backend: " + (backend or ("setup.py" if has("setup.py") else "none found"))
    pyv = proj.get("requires-python") or text(".python-version").strip() or "none found"
    yield f"python: {pyv}"
    if "[tool.pytest" in cfg_text or has("pytest.ini", "conftest.py") or list(root.glob("tests/conftest.py")):
        tests = "pytest"
    elif re.search(r"unittest\.TestCase", "".join(p.read_text(errors="ignore") for p in list(root.glob("tests/**/*.py"))[:30])):
        tests = "unittest"
    else:
        tests = "pytest" if list(root.glob("tests/test_*.py")) else "none found"
    extra = has("tox.ini", "noxfile.py")
    yield "tests: " + tests + (f" via {', '.join(extra)}" if extra else "")
    fmt = [n for n, k in (("ruff format", "[tool.ruff"), ("black", "black"), ("isort", "isort"), ("yapf", "yapf")) if k in cfg_text or (k == "[tool.ruff" and has("ruff.toml", ".ruff.toml"))]
    lint = [n for n, k in (("ruff", "[tool.ruff"), ("flake8", "flake8"), ("pylint", "pylint")) if k in cfg_text or (k == "[tool.ruff" and has("ruff.toml", ".ruff.toml"))]
    yield "format/lint: " + (", ".join(dict.fromkeys(fmt + lint)) or "none found")
    types = [n for n, k in (("mypy", "mypy"), ("pyright", "pyright"), ("pyrefly", "pyrefly"), ("ty", "[tool.ty")) if k in cfg_text or (n == "pyright" and has("pyrightconfig.json"))]
    yield "types: " + (", ".join(types) or "none found")
    check = []
    for mk in ("Makefile", "justfile"):
        for m in re.finditer(r"^(check|test|ci|lint|verify)\s*:", text(mk), re.M):
            check.append(f"{'make' if mk == 'Makefile' else 'just'} {m.group(1)}")
    yield "check command: " + (", ".join(check) or "none found (read the CI steps)")
    ci = [str(p.relative_to(root)) for p in list((root / ".github/workflows").glob("*.y*ml"))] + has(".gitlab-ci.yml")
    yield "ci: " + (", ".join(ci) or "none found")
    docs = has("mkdocs.yml") + (["sphinx (docs/conf.py)"] if has("docs/conf.py") else [])
    native = [n for n in ("Cargo.toml", "CMakeLists.txt", "meson.build", "build.zig") if (root / n).exists()] + (["ext_modules"] if "ext_modules" in all_text else []) + [str(p.name) for p in list(root.glob("**/*.pyx"))[:1]]
    yield "docs: " + (", ".join(docs) or "none found") + "; native: " + (", ".join(native) or "none")
    mem = text("AGENTS.md") + text("CLAUDE.md")
    yield "project memory: " + ("## Tabby section" if "## Tabby" in mem else "no ## Tabby section") + (", ## Python defaults" if "## Python defaults" in mem else "") + (f"; {', '.join(has('AGENTS.md', 'CLAUDE.md'))}" if has("AGENTS.md", "CLAUDE.md") else "; no AGENTS.md or CLAUDE.md")


print("Detected from the repo (files only; nothing was run):")
try:
    for ln in lines():
        print("- " + ln)
except Exception as e:  # never fail the skill that runs this
    print(f"- (detect.py stopped: {type(e).__name__}; read the repo instead)")
