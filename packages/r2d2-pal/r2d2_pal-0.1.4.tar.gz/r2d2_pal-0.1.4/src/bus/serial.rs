//! # Serial Bus
//!
//! Serial bus implementation.

use std::time::{Duration, Instant};

use embedded_hal_nb::serial::{Read, Write};
use linux_embedded_hal::serialport;
use linux_embedded_hal::serialport::DataBits;
use linux_embedded_hal::serialport::Parity;
use linux_embedded_hal::serialport::StopBits;
use linux_embedded_hal::Serial;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

/// SerialBus(port_name="/dev/ttyUSB0", baud_rate=9600, byte_size=8, parity="None", stop_bits=1)
///
/// Serial bus definition.
#[pyclass]
pub struct SerialBus {
    /// The port name
    pub port_name: String,
    /// The baud rate
    pub baud_rate: u32,
    /// The byte size
    pub byte_size: DataBits,
    /// The parity
    pub parity: Parity,
    /// The stop bits
    pub stop_bits: StopBits,
    /// The internal bus
    bus: Option<Serial>,
}

#[pymethods]
impl SerialBus {
    /// Creates a new serial bus.
    #[new]
    #[pyo3(signature = (port_name, baud_rate, byte_size, parity, stop_bits))]
    fn new(
        port_name: String,
        baud_rate: u32,
        byte_size: Option<u8>,
        parity: Option<String>,
        stop_bits: Option<u8>,
    ) -> PyResult<Self> {
        let byte_size = match byte_size {
            Some(byte_size) => DataBits::try_from(byte_size).unwrap(),
            None => DataBits::Eight,
        };

        let parity = match parity {
            Some(parity) => match parity.as_str() {
                "None" => Parity::None,
                "Odd" => Parity::Odd,
                "Even" => Parity::Even,
                _ => {
                    return Err(PyValueError::new_err(format!(
                        "Invalid parity value: {}",
                        parity
                    )))
                }
            },
            None => Parity::None,
        };

        let stop_bits = match stop_bits {
            Some(stop_bits) => StopBits::try_from(stop_bits).unwrap(),
            None => StopBits::One,
        };

        Ok(SerialBus {
            port_name,
            baud_rate,
            byte_size,
            parity,
            stop_bits,
            bus: None,
        })
    }

    /// Opens the serial bus.
    #[pyo3(signature = ())]
    fn open(&mut self) -> PyResult<()> {
        let builder = serialport::new(&self.port_name, self.baud_rate)
            .data_bits(self.byte_size)
            .parity(self.parity)
            .stop_bits(self.stop_bits)
            .flow_control(serialport::FlowControl::None);
        self.bus = match Serial::open_from_builder(builder) {
            Ok(port) => Some(port),
            Err(_) => return Err(PyValueError::new_err(format!("Failed to open serial port"))),
        };
        Ok(())
    }

    /// Closes the serial bus.
    #[pyo3(signature = ())]
    fn close(&mut self) -> PyResult<()> {
        self.bus = None;
        Ok(())
    }

    /// Reads data from the serial bus.
    #[pyo3(signature = (length, timeout))]
    fn read(&mut self, length: u16, timeout: f32) -> PyResult<Vec<u8>> {
        let mut data = Vec::new();
        let start_time = Instant::now();
        let timeout_duration = Duration::from_secs_f32(timeout);

        let port = match self.bus.as_mut() {
            Some(port) => port,
            None => return Err(PyValueError::new_err(format!("Port not open"))),
        };

        for _ in 0..length {
            if start_time.elapsed() > timeout_duration {
                break;
            }

            match port.read() {
                Ok(byte) => data.push(byte),
                Err(_) => return Err(PyValueError::new_err(format!("Failed to read data"))),
            }
        }

        Ok(data)
    }

    /// Writes data to the serial bus.
    #[pyo3(signature = (data))]
    fn write(&mut self, data: Vec<u8>) -> PyResult<()> {
        let port = match self.bus.as_mut() {
            Some(port) => port,
            None => return Err(PyValueError::new_err(format!("Port not open"))),
        };

        for byte in data {
            match port.write(byte) {
                Ok(_) => (),
                Err(_) => return Err(PyValueError::new_err(format!("Failed to write data"))),
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use std::io::{Read, Write};

    use super::SerialBus;

    #[test]
    fn test_serial_read() {
        let (mut master, _slave, name) =
            openpty::openpty(None, None, None).expect("Creating pty failed");
        let mut bus =
            SerialBus::new(name, 9600, Some(8), Some("None".to_string()), Some(1)).unwrap();

        bus.open().expect("Opening bus failed");

        master
            .write_all("Hello, world!".as_bytes())
            .expect("Writing to bus failed");

        let data = bus.read(13, 10.0).expect("Reading from bus failed");
        assert_eq!("Hello, world!".as_bytes(), data.as_slice());
    }

    #[test]
    fn test_serial_write() {
        let (mut master, _slave, name) =
            openpty::openpty(None, None, None).expect("Creating pty failed");
        let mut bus =
            SerialBus::new(name, 9600, Some(8), Some("None".to_string()), Some(1)).unwrap();

        bus.open().expect("Opening bus failed");

        let data = "Hello, world!".as_bytes().to_vec();
        bus.write(data).expect("Writing to bus failed");

        let mut buffer = [0u8; 13];
        master
            .read(buffer.as_mut())
            .expect("Reading from bus failed");

        assert_eq!("Hello, world!".as_bytes(), buffer);
    }
}
