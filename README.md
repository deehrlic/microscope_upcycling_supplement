# "Microscope Upcycling" Supplemental Material

This repositoty contains the supplemental material for the paper "Microscope Upcycling: Transforming legacy microscopes into automated cloud-integrated imaging systems" by Yohei Rosen, Drew Ehrlich, David F. Parks, Ryan Fenimore, David Haussler, Sri Kurniawan, and Mircea Teodorescu

To order machined parts (files in /hardware with the extension .dxf or .dwg), use any remote manufacturing service - we recommend SendCutSend. These parts should be manufactured out of the material listed for them in the BOM file at the root of this repository. One part will need a bend, and another will need to have countersunk holes.

Printed parts (files in /hardware with the extension .stl) should be ordered from a 3D printing or CNC milling service if you cannot manufacture them in house - we recommed PCBWay. 

The folder /streamdeckmini contains the scripts to operate the XY stage from a Elgato Stream Deck Mini. Each script can be bound to a button using the "Run" module in the Elgato Stream Deck software - these buttons will move the motors back and forth.

The folder /streamdeckpedal contains the scripts to operate the utilities intended to be used with the Z-stacking tool that are controlled by an Elgato Stream Deck Pedal. These are a script that captures still images and the script that operates the GUI for performing Z-stacking. The last button opens the folder where images are stored, which does not require a script. These buttons can be programmed in the same manner those for the Stream Deck Mini can.

These control mappings can also be seen in the image below. 

![controlscheme](/stills/controlscheme.PNG)

For wiring the motor driver to the motor and the motor power supply, the image below can be used as a reference to make sure the motor is connected properly.

![wiringguide](/stills/wiringguide.png)
