#!/usr/bin/env bash
# Builds the fixture project for the `cpp-binding-return-policy` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["scikit-build-core>=0.10", "nanobind>=2.4"]
build-backend = "scikit_build_core.build"

[project]
name = "gridlib"
version = "0.2.0"
requires-python = ">=3.12"
__FIXTURE_EOF__
mkdir -p "$(dirname CMakeLists.txt)"
cat > CMakeLists.txt <<'__FIXTURE_EOF__'
cmake_minimum_required(VERSION 3.18)
project(gridlib LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
find_package(Python 3.12 COMPONENTS Interpreter Development.Module REQUIRED)
find_package(nanobind CONFIG REQUIRED)
nanobind_add_module(_core src/grid.cpp)
install(TARGETS _core LIBRARY DESTINATION gridlib)
__FIXTURE_EOF__
mkdir -p "$(dirname src/grid.cpp)"
cat > src/grid.cpp <<'__FIXTURE_EOF__'
#include <cstddef>
#include <vector>

#include <nanobind/nanobind.h>

namespace nb = nanobind;

struct Cell {
    double value = 0.0;
};

class Grid {
public:
    explicit Grid(std::size_t n) : cells_(n) {}

    Cell *cell(std::size_t i) { return &cells_[i]; }

    std::size_t size() const { return cells_.size(); }

private:
    std::vector<Cell> cells_;
};

NB_MODULE(_core, m) {
    nb::class_<Cell>(m, "Cell")
        .def_rw("value", &Cell::value);

    nb::class_<Grid>(m, "Grid")
        .def(nb::init<std::size_t>())
        .def("cell", &Grid::cell)
        .def("size", &Grid::size);
}
__FIXTURE_EOF__
mkdir -p "$(dirname src/gridlib/__init__.py)"
cat > src/gridlib/__init__.py <<'__FIXTURE_EOF__'
from gridlib._core import Cell, Grid

__all__ = ["Cell", "Grid"]
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_grid.py)"
cat > tests/test_grid.py <<'__FIXTURE_EOF__'
from gridlib import Grid


def test_size():
    assert Grid(4).size() == 4
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
