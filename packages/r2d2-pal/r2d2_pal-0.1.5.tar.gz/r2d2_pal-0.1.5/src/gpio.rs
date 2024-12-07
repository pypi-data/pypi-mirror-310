//! # GPIO
//!
//! GPIO module.

use core::fmt;

use embedded_hal::digital::{InputPin, OutputPin};
use linux_embedded_hal::{
    gpio_cdev::{Chip, LineRequestFlags},
    CdevPin,
};
use pyo3::{exceptions::PyValueError, prelude::*};

/// GPIO direction.
#[derive(PartialEq)]
pub enum Direction {
    /// Input direction.
    Input,
    /// Output direction.
    Output,
}

impl TryFrom<&str> for Direction {
    type Error = String;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        match value {
            "in" => Ok(Direction::Input),
            "out" => Ok(Direction::Output),
            _ => Err(format!("Invalid direction value: {}", value)),
        }
    }
}

/// GPIO state.
pub enum State {
    /// High state.
    High,
    /// Low state.
    Low,
}

impl fmt::Display for State {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            State::High => write!(f, "high"),
            State::Low => write!(f, "low"),
        }
    }
}

impl TryFrom<&str> for State {
    type Error = String;

    fn try_from(value: &str) -> Result<Self, Self::Error> {
        match value {
            "high" => Ok(State::High),
            "low" => Ok(State::Low),
            _ => Err(format!("Invalid state value: {}", value)),
        }
    }
}

/// GPIO(pin_nb=22, direction="in", state="low")
///
/// GPIO definition.
#[pyclass]
pub struct GPIO {
    /// The pin number
    pub pin_nb: u8,
    /// The direction
    pub direction: Direction,
    /// The state
    pub state: State,
    /// The internal GPIO pin
    pin: Option<CdevPin>,
}

#[pymethods]
impl GPIO {
    #[new]
    #[pyo3(signature = (pin_nb, direction, state))]
    fn new(pin_nb: u8, direction: String, state: String) -> PyResult<Self> {
        let gpio_direction = match Direction::try_from(direction.as_str()) {
            Ok(direction) => direction,
            Err(error) => return Err(PyValueError::new_err(error)),
        };
        let gpio_state = match State::try_from(state.as_str()) {
            Ok(state) => state,
            Err(error) => return Err(PyValueError::new_err(error)),
        };

        let mut chip = match Chip::new(direction) {
            Ok(chip) => chip,
            Err(error) => return Err(PyValueError::new_err(error.to_string())),
        };
        let line = match chip.get_line(0) {
            Ok(line) => line,
            Err(error) => return Err(PyValueError::new_err(error.to_string())),
        };
        let line_handle = match line.request(LineRequestFlags::OUTPUT, 0, "gpio") {
            Ok(line_handle) => line_handle,
            Err(error) => return Err(PyValueError::new_err(error.to_string())),
        };
        let pin = match CdevPin::new(line_handle) {
            Ok(pin) => pin,
            Err(error) => return Err(PyValueError::new_err(error.to_string())),
        };

        Ok(GPIO {
            pin_nb,
            direction: gpio_direction,
            state: gpio_state,
            pin: Some(pin),
        })
    }

    /// Sets the GPIO state.
    #[pyo3(signature = (state))]
    fn set_state(&mut self, state: String) -> PyResult<()> {
        let gpio_state = match State::try_from(state.as_str()) {
            Ok(state) => state,
            Err(error) => return Err(PyValueError::new_err(error)),
        };

        let pin = match &mut self.pin {
            Some(pin) => pin,
            None => return Err(PyValueError::new_err("GPIO pin is not initialized")),
        };

        match gpio_state {
            State::High => pin
                .set_high()
                .map_err(|error| PyValueError::new_err(error.to_string())),
            State::Low => pin
                .set_low()
                .map_err(|error| PyValueError::new_err(error.to_string())),
        }
    }

    /// Gets the GPIO state.
    #[pyo3(signature = ())]
    fn get_state(&mut self) -> PyResult<String> {
        let pin = match &mut self.pin {
            Some(pin) => pin,
            None => return Err(PyValueError::new_err("GPIO pin is not initialized")),
        };

        if self.direction != Direction::Input {
            return Err(PyValueError::new_err("Cannot get state of input GPIO"));
        }

        let state = match pin.is_high() {
            Ok(true) => State::High,
            Ok(false) => State::Low,
            Err(error) => return Err(PyValueError::new_err(error.to_string())),
        };

        Ok(state.to_string())
    }
}
