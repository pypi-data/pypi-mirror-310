mod bus;

use pyo3::prelude::*;

/// An I/O device communication module written in Rust.
#[pymodule]
fn r2d2(m: &Bound<'_, PyModule>) -> PyResult<()> {
    bus::init_pymodule(m)?;
    Ok(())
}
