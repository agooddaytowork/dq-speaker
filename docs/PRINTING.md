# Printing guide

The fit-tested prototype was printed in Bambu Lab PETG. Do not globally scale
the STL files: the mounting geometry and heat-set insert pockets are already
dimensioned for the tested design.

## Suggested starting profile

- 0.4 mm nozzle
- 0.20 mm layer height
- 4 walls
- 5 top and 5 bottom layers
- 25–35% gyroid infill for caps and handle
- 35–45% gyroid infill for both frame halves
- 3–4 walls for the sleeve; infill has little effect on its thin shell
- PETG temperature and cooling per the filament manufacturer

These are starting points, not a locked profile. Increase walls before adding
heavy infill when more stiffness is needed.

## Orientation

| File | Recommended orientation |
| --- | --- |
| `01-rear-frame.stl` | Largest flat rail face on the bed; bosses upward |
| `02-front-frame.stl` | Largest flat rail face on the bed; columns upward |
| `03-outer-sleeve.stl` | Upright on one end, 133 × 97 mm footprint |
| `04-top-cap.stl` | Exterior face on the bed, service pocket upward |
| `05-bottom-cap.stl` | Broad exterior/base face on the bed |
| `06-v-handle.stl` | Mounting pads on the bed; inspect bridges in preview |
| `07`–`10` screw plugs | Flat face on the bed |

Use support only where the slicer preview shows an unsupported critical face.
Keep support away from the sleeve grooves, insert pockets and mounting columns
where possible.

## First print sequence

Print the two frame halves before the cosmetic parts. Confirm:

1. the speaker module can be inserted between the halves;
2. all six front columns and four rear bosses line up;
3. the four horizontal frame screws do not touch the driver assembly;
4. top and bottom frame interfaces remain square after tightening.

Only then print the sleeve and caps. PETG strings around the ventilation slots;
remove loose material before installing electronics.

## Heat-set inserts

Use a temperature-controlled insert tip. Start near the low end of the PETG
working range and increase slowly. Press the insert straight, stop at the
designed shoulder, and let it cool before testing a screw. Excess heat can
soften the nearby rail and move a mounting point.

