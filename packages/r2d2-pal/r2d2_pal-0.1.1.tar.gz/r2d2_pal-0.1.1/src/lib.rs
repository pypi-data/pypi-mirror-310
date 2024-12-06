pub mod bus;

use bus::{i2c::I2CBus, serial::SerialBus};
use pyo3::prelude::*;

/// An I/O device communication module written in Rust.
#[pymodule]
fn r2d2(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<SerialBus>()?;
    m.add_class::<I2CBus>()?;
    Ok(())
}
