//! # Bus
//! 
//! Bus module.

pub mod i2c;
pub mod serial;

#[path = "tests/mod.rs"]
#[cfg(test)]
pub mod tests;
