# Intro
## Problem
- Milfoil is an invasive species of algae in many freshwater lakes and rivers in North America. This project seeks to help identify the spread of this species of weed using new technology. The stretch goal would be an autonomous vehicle which could navigate a body of water autonomousls, mapping the areas on the body of water where milfoil is present using computer vision. This could be adapted to other invasive species.
# Pre-requisites
## Current
Raspi
- Currently this works on a Model 3B. You need a model with Bluetooth and Wifi.
GoPro
- Currently this works on a Hero 8 Black.
Adafruit Ultimate GPS
- The GoPro has GPS capabilites. However, these chew up the battery even more. This module from Adafruit is quite low power. Use of an external antenna recommended. 
- Follow the tutorials to install blinka and other dependencies for this
Power
- A usb power bank is enough to power the raspi and the gps board. *HOWEVER*, make sure the Raspi gets the voltage it needs, otherwise something weird happens with the NMEA sentences and they look semi garbled making parsing impossible. 
## Anticipated needs
### Propulsion
A childhood RC toy could be re-purposed for these needs
If anything bigger is needed, maybe an old SeaDoo hull?
### Communications
LORA could provide a power efficient way to transmit small amounts of data over relatively long distances. Would probably be limited to relaying positions, commands.
### Power
The USB power bank is not going to be powerful enough to run the boat (servos and motor) and the raspi + accessories...

# Thanks
https://github.com/KonradIT seems to have figured out the tough parts
# Short term goal
-Test current setup:
-   Using a kayak, can the raspi tell the GoPro to take a picture, get the filename, get the current GPS coordinates, save the data as a csv
-   Batch export the data with pictures into something that can 
# Long term goal
- Make web app for model
- Make web app for results w/ map and sample pics
- Automate running the model
- Putting all this stuff on a boat
  - Making the boat autonomous
  - Running the model on the raspi (external TPU?)
- More AI:
  - Can we predict where the weed will be?
  - Add features to current model to factor in variables such as the current weather conditions, etc.
- Propulsion
- Automated navigation
# Done
-Train AI model using MS Lobe
-Long range command and control

# TODO
- clean up this mess 
