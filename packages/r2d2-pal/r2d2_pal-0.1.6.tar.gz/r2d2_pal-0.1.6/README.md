# R2D2

> "Rust Reliable Device Drivers"

r2d2-pal (R2D2 Protocol Abstraction Layer) is a module to define Rust bindings for Python of the [linux_embedded_hal](https://docs.rs/linux-embedded-hal/latest/linux_embedded_hal/) crate.

## Installation

```shell
pip install -U r2d2-pal
```

## Usage

Serial example:

```python
import r2d2

bus = r2d2.SerialBus(
    port_name=port_name,
    baud_rate=baud_rate,
    byte_size=byte_size,
    parity=str(parity),
    stop_bits=stop_bits,
)

bus.write(b"Hello, World!")
data = bus.read(13, 10.0)
```
