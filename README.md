# Scale Driver for a Sartorius Secura 

This driver gives you the ability to communicate with a Sartorius brand Secura scale through a serial port USB connection.

## Getting Started

### Scale Settings

1. Insure that the device protocol is set to PC-SBI. 
2. The print function should be set to manual without stability. 

### Setup

1. Clone the repository.
2. Turn on scale and manually level.
3. Connect the scale via a USB cable.
4. Open example.py and adapt it to fit your application.


## Features

- Communicate with the scale to get weight measurements
- Process scale responses and raw data
- Configure the scale settings
- Error handling for scale communication

### Tare and Calibration

To tare the scale use `tare()` and to preforma an internal callibration use `isocal()`.

### Measuring

To get a simple weight measurement use the `getWeight()`. If you would like to take a longer measurement over a given time period use the `collectWeightTillTime()`. If you would like to take a meaurement till a given weight is reached then use the `collectWeightTillMix()`.

## Example

```python

from scale_driver import Scale

my_scale = Scale('COM7',9600,timeout=3)
my_scale.tare()
my_scale.getWeight()

```

## Contact

Danika Heaney - danika.heaney@tum.de or 
Helge Stein - helge.stein@tum.de

## Acknowledgements

This code was modeled after [sartoriususb](https://github.com/holgi/sartoriusb).



