import subprocess
import os
import time

MAC='D2:C5:26:66:6C:7D'

def turn_off_wifi():
    os.system('sudo /home/pi/Documents/Snoop/wifi_disconnect.sh')

def turn_on_wifi():
    os.system('sudo /home/pi/Documents/Snoop/wifi_connect.sh')


def get_wifi_list():
    return subprocess.check_output("check_wifi_list.sh")

def get_current_wifi():
    return subprocess.check_output("iwgetid").decode("utf-8")


def main():
    for x in range(0,5):
        print("Try #", x)
        turn_on_wifi()
        #wifi_list = get_wifi_list()
        # if "HERO8B" in wifi_list:
        #     print ("GoPro Wifi On")
        # else:
        #     print("GoPro Wifi Off...")
        curr_wifi = get_current_wifi()
        if "HERO8B" in curr_wifi:
            print("Connected")
            return 1
            break
        else:
            print("Cannot connect")
        time.sleep(5)
    return 0
if __name__ =='__main__': 
    main()


