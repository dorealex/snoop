from goprocam import GoProCamera, constants
import board
import digitalio
from adafruit_debouncer import Debouncer
import os
from datetime import datetime
import time
import threading
import csv
import busio
import serial
import adafruit_gps
import subprocess

import startup
###Wake Up GoPro
code = startup.main()

### GoPro settings
gopro = GoProCamera.GoPro()


###GPS Settings
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")

### Button settings
def make_pin_reader(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP
    return lambda: io.value
pin5 = Debouncer(make_pin_reader(board.D12))
pin6 = Debouncer(make_pin_reader(board.D13))

### Button settings
def make_pin_reader(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP
    return lambda: io.value
pin5 = Debouncer(make_pin_reader(board.D12))
pin6 = Debouncer(make_pin_reader(board.D13))

pin = digitalio.DigitalInOut(board.D12)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
switch = Debouncer(pin, interval=0.1)

### Second button setting
pin2 = digitalio.DigitalInOut(board.D13)
pin2.direction = digitalio.Direction.INPUT
pin2.pull = digitalio.Pull.UP
switch2 = Debouncer(pin2, interval=0.1)

### Picture save location
dir_path = os.path.dirname(os.path.realpath(__file__))
new_path = dir_path+"/pictures/"

data_path = dir_path+'/data/'

save = False

### Functions
def getGPSdata():
   
    lat = 0 
    lon = 0
    sats = 0
    alt = 0
    speed = 0
    angle = 0
    horiz_d = 0
    height = 0
    
    lat = gps.latitude
    lon = gps.longitude
    if gps.satellites is not None:
        sats = gps.satellites
    if gps.altitude_m is not None:
        alt = gps.altitude_m
    if gps.speed_knots is not None:
        speed=gps.speed_knots
    if gps.track_angle_deg is not None:
        angle=gps.track_angle_deg
    if gps.horizontal_dilution is not None:
        horiz_d=gps.horizontal_dilution
    if gps.height_geoid is not None:
        height = gps.height_geoid
    return lat, lon, sats, alt, speed, angle, horiz_d, height

def writeData(row):
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)

            
def takePhoto(e):
    while e.isSet():
        row = []
        gopro.take_photo()
        #gopro.downloadLastMedia()
        fullname = gopro.getMedia()
        fname = '100GOPRO-' + fullname.split("/")[-1]
        lat, lon, sats, alt, speed, angle, horiz_d, height = getGPSdata()
        date = datetime.now().strftime('%D')
        time = datetime.now().strftime('%T')
        row = [date,time,lat,lon, sats, alt, speed, angle, horiz_d, height, fullname, fname]
        writeData(row)
        print('Taking picture',date,time)
        #current_file = dir_path+'/'+fname
        #if os.path.isfile(current_file):
        #    os.replace(current_file, new_path+fname) #move file, would be cleaner to download the file directly to the right folder, but the API doesn't work the way I thought it did
        e.wait(5)
def setup_folder():
    base_path = dir_path+'/data/'
    fname = base_path+datetime.now().strftime('%Y-%b-%d-%R')+'.csv'      
    fname = fname.replace(":","_")
    with open(fname, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
    return fname
### Initial settings
total_rows = []       
e = threading.Event()
t1 = threading.Thread(target=takePhoto, args=([e]))
headers =  ["date","time","lat","lon", "sats", "alt", "speed", "angle", "horiz_d", "heigh", "fullname", "fname"]
run = True
data_file = setup_folder()
print(data_file)
print("Starting script")

### Main loop
while(run):
    gps.update()
    switch.update()
    if switch.fell:
        #toggle value
        save = not save
        print('Toggle switch, new val:',save)
    switch2.update()
    if switch2.fell:
        print('pressing the 2nd button')
        save = False
        e.clear()
        
        run=False
    if save:
        e.set() #should be taking pictures
    else:
        e.clear() #not taking pictures
        
    if not t1.is_alive(): #start the thread if it hasn't been yet
        if e.is_set():
            try:
                t1.start()
            except :
                pass
startup.turn_off_wifi()    
print('Script Ended. Disconnecting from GoPro')