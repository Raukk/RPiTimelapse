# hourly_timelapse_images.py
# This file creates images for time lapse videos broken up by hour
from picamera import PiCamera
from os import system, path
import os
import datetime
from time import sleep
import time

# Set up all the static variables that don't change
secondsinterval = 0.5 #number of seconds between each photo taken. This was determined experimentally
photos_per_min = int(60//secondsinterval)

# Basic Camera Settings
x_res = 1280
y_res = 720
# The camera hardware can do higher resolution but FHD was filling toom uch space on the drive.

font_size = int(y_res//100) * 10
camera = PiCamera()
camera.resolution = (x_res, y_res)

print("RPi started taking photos for your timelapse at: " + str(datetime.datetime.now()), flush=True)

# infinte loop
while(True):
    # Get the date
    today = datetime.date.today()
    # Create a folder for the date
    folder_name = '/home/pi/Pictures/' + str(today)
    if(False == path.exists(folder_name)):
        os.makedirs(folder_name)
        
    # While it is still the same day
    while(today == datetime.date.today()):
        i = int(((datetime.datetime.now().minute * 60) + datetime.datetime.now().second) / secondsinterval) # reset the counter every hour
        
        # Get the Hour of the day
        hour = datetime.datetime.now().hour    
        # Create a folder for the hour        
        hour_folder_name = folder_name + '/' + str(hour)
        if(False == path.exists(hour_folder_name)):
            os.makedirs(hour_folder_name)
            
        # While it is still the same hour    
        while(hour == datetime.datetime.now().hour):
            # Create the file name for this timelapse image
            file_name = hour_folder_name +'/image{0:06d}.jpg'.format(i)
            
            # Capture the Image and add the Date-Time stamp 
            camera.capture(file_name, quality=15) # Quality 15 was selected because it reduces the size while not looking bad
            
            # This adds the Date and Time to the bottom of the photo
            system('convert -pointsize {} -fill white -draw \"text {},{} \'{}\'\" {} {} &'.format(str(font_size), font_size, str(y_res-font_size), str(today) + ' - ' + datetime.datetime.now().strftime("%H:%M:%S"), file_name, file_name))
            
            # Every 5 minutes log the progress (when running from the console, it helps you know it's still running without spamming the console)
            if(i%(photos_per_min * 5) == 0):
                print('Saving image number: ', file_name, flush=True)
                
            i += 1 # increment i
            
        print("End Of the Hour", flush=True)
        
    print("End Of the Day", flush=True)
    
