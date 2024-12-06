use std::io::{Read, Write};

use super::serial::SerialBus;

#[test]
fn test_serial_read() {
    let (mut master, _slave, name) =
        openpty::openpty(None, None, None).expect("Creating pty failed");
    let mut bus = SerialBus::new(name, 9600, Some(8), Some("None".to_string()), Some(1)).unwrap();

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
    let mut bus = SerialBus::new(name, 9600, Some(8), Some("None".to_string()), Some(1)).unwrap();

    bus.open().expect("Opening bus failed");

    let data = "Hello, world!".as_bytes().to_vec();
    bus.write(data).expect("Writing to bus failed");

    let mut buffer = [0u8; 13];
    master
        .read(buffer.as_mut())
        .expect("Reading from bus failed");

    assert_eq!("Hello, world!".as_bytes(), buffer);
}
