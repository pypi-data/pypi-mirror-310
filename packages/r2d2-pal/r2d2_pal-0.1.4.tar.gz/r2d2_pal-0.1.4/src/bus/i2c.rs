//! # I2C Bus
//! I2C bus implementation.

use embedded_hal::i2c::{I2c, Operation};
use linux_embedded_hal::I2cdev;
use pyo3::{exceptions::PyValueError, prelude::*};

/// I2CBus(address=0x00, path="/dev/i2c-1")
///
/// I2C bus definition.
#[pyclass]
pub struct I2CBus {
    /// The device address
    pub address: u8,
    /// The device path
    pub path: String,
    /// The I2C bus
    bus: Option<I2cdev>,
}

#[pymethods]
impl I2CBus {
    /// Creates a new I2C bus.
    #[new]
    #[pyo3(signature = (address, path))]
    fn new(address: u8, path: String) -> PyResult<Self> {
        Ok(I2CBus {
            address,
            path,
            bus: None,
        })
    }

    /// Opens the I2C bus.
    #[pyo3(signature = ())]
    fn open(&mut self) -> PyResult<()> {
        let bus = match I2cdev::new(&self.path) {
            Ok(bus) => bus,
            Err(_) => {
                return Err(PyValueError::new_err(format!(
                    "Failed to open I2C bus at {}",
                    self.path
                )))
            }
        };

        self.bus = Some(bus);
        Ok(())
    }

    /// Closes the serial bus.
    #[pyo3(signature = ())]
    fn close(&mut self) -> PyResult<()> {
        self.bus = None;
        Ok(())
    }

    /// Reads data from the I2C bus.
    #[pyo3(signature = (length))]
    fn read(&mut self, length: u16) -> PyResult<Vec<u8>> {
        let bus = match self.bus {
            Some(ref mut bus) => bus,
            None => return Err(PyValueError::new_err(format!("I2C bus is not open"))),
        };

        let mut read_buffer = vec![0u8; length as usize];
        let mut ops = [Operation::Read(&mut read_buffer)];

        match bus.transaction(self.address, &mut ops) {
            Ok(_) => return Ok(read_buffer.as_mut_slice().to_vec()),
            Err(_) => {
                return Err(PyValueError::new_err(format!(
                    "Failed to read from I2C bus"
                )))
            }
        }
    }

    /// Writes data to the I2C bus.
    #[pyo3(signature = (data))]
    fn write(&mut self, mut data: Vec<u8>) -> PyResult<()> {
        let bus = match self.bus {
            Some(ref mut bus) => bus,
            None => return Err(PyValueError::new_err(format!("I2C bus is not open"))),
        };

        let mut ops = [Operation::Write(data.as_mut_slice())];

        match bus.transaction(self.address, &mut ops) {
            Ok(_) => Ok(()),
            Err(_) => return Err(PyValueError::new_err(format!("Failed to write to I2C bus"))),
        }
    }
}
