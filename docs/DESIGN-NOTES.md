# Design notes

## Mechanical architecture

The enclosure is divided into four functional groups:

1. a two-piece internal frame that holds the donor speaker and links top to
   bottom;
2. a ventilated outer sleeve keyed into grooves in both caps;
3. removable top and bottom caps;
4. an optional V handle sharing the four top fasteners.

The frame had to remain split. A one-piece frame looked cleaner in CAD but left
no practical path to install the speaker module. Earlier frame joints also
crossed the driver volume, so the final connection keeps the fastening mass at
the perimeter.

## Tested revisions worth preserving

- Front mounting columns: six at 4.2 mm diameter.
- Rear mounting bosses: four at 6 mm diameter.
- The corrected pair of front columns is offset toward the intended side; the
  centre pair remains at the original fit-tested location.
- Native Fusion fillet features replace hand-drawn corner approximations on
  load-bearing 90-degree transitions.
- The rectangular shell reduces wasted volume while preserving the fitted
  mounting geometry.
- The top cap is pocketed 8 mm from the inside for USB-C/power tool access,
  while retaining the sleeve groove wall and local M3 islands.
- The V handle moves its grip to the centre and avoids the power control. All
  exposed handle edges are filleted.

The detailed working specifications are retained under `cad/source/`. Some of
those notes are in Vietnamese because they record the actual iteration history.

