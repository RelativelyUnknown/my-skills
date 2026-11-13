#!/usr/bin/env bash
# Builds the fixture project for the `review-pyo3-diff` case in the empty workspace. Never compiled.
set -euo pipefail
mkdir -p src python/fastsum
cat > Cargo.toml <<'__F__'
[package]
name = "fastsum"
version = "0.1.0"
edition = "2021"

[lib]
name = "_fastsum"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.22", features = ["extension-module"] }
__F__
cat > python/fastsum/__init__.py <<'__F__'
from fastsum._fastsum import checksum, parse_header

__all__ = ["checksum", "parse_header"]
__F__
cat > src/lib.rs <<'__F__'
use pyo3::prelude::*;

/// Sum of the bytes, modulo 2**32.
#[pyfunction]
fn checksum(data: &[u8]) -> u32 {
    data.iter().fold(0u32, |acc, b| acc.wrapping_add(*b as u32))
}

#[pymodule]
fn _fastsum(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(checksum, m)?)?;
    Ok(())
}
__F__
git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -q -m "checksum"
cat > src/lib.rs <<'__F__'
use pyo3::prelude::*;

/// Sum of the bytes, modulo 2**32.
#[pyfunction]
fn checksum(data: &[u8]) -> u32 {
    data.iter().fold(0u32, |acc, b| acc.wrapping_add(*b as u32))
}

/// Read a header of the form "LEN:PAYLOAD" and return (declared length, payload length).
#[pyfunction]
fn parse_header(header: &str) -> PyResult<(u32, u32)> {
    let (len, payload) = header.split_once(':').ok_or_else(|| {
        pyo3::exceptions::PyValueError::new_err("missing ':'")
    })?;
    let declared: u32 = len.parse().unwrap();
    Ok((declared, payload.len() as u32))
}

#[pymodule]
fn _fastsum(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(checksum, m)?)?;
    m.add_function(wrap_pyfunction!(parse_header, m)?)?;
    Ok(())
}
__F__
