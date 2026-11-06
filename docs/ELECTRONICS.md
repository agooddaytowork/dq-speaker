# Electronics notes

## Signal and power path

The prototype uses one reclaimed Google Nest Audio two-way speaker assembly
without its original electronics, one LF03S 2 × 25 W DSP
amplifier and one 7.4 V lithium battery pack. The board provides the amplifier,
DSP controls and USB-C charging interface used in the build.

The exact LF03S board revision can vary by seller. Confirm every connector and
pin label against the board in your hand; do not use marketplace photos as a
wiring diagram.

## Mechanical interfaces

- top power opening: 13 mm diameter
- top USB-C opening: 11 mm diameter
- top-cap internal service pocket: 8 mm deep, leaving a 4 mm top skin
- optional electronics screws: M2 × 10 mm with matching inserts

Wire the board outside the enclosure and test both drivers at low level first.
Verify channel assignment and DSP crossover settings before increasing volume.

## DSP used during the prototype

The vendor mobile application was used for crossover, channel gain and output
EQ. The REW graph in `media/frequency-response.jpg` shows the raw mid/bass and
treble measurements alongside the purple response after crossover tuning.
Screenshots in
`media/` are development records, not universal presets: driver modules,
placement and rooms differ, so measure your own build.

## Battery safety

- use a protected pack with an appropriate BMS;
- verify charger voltage, polarity and current rating;
- add insulation and strain relief around every metal edge;
- keep the pack away from heat-set insert work;
- never enclose, charge or reuse a swollen, punctured or damaged cell;
- stop immediately if the pack or board becomes unusually hot.

This project has not been safety certified. Build and operate it at your own
risk.

