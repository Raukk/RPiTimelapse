# manual_hourly_timelapse_video.py
# This file turns the Hourly Images to a Timelapse Video and cleans up the Images folders.
from os import system, path
import os
import datetime
from time import sleep
import time

# Basic timelapse Video settings 
fps = 30
x_res = 1280
y_res = 720
timelapse_levels = 4 # each time lapse level doubles the speed of the timelapse from the default ~15x, to 30x, 60x, 120x etc.

# using the point at which it is called to assume that we need to process this hours images into a video. 
today = datetime.date.today()
hour = 14   # datetime.datetime.now().hour - 1
folder_name = '/home/pi/Pictures/' + str(today)
hour_folder_name = folder_name + '/' + str(hour)
# simply waiting an hour means that we don't have to worry about subtracting an hour and getting a previous day, etc.
sleep_time = 60 * 60 + 100 # sleep for 60 minutes of 60 seconds plus 100 extra seconds to give some buffer for slow processes and inaccurate timers
numphotos = 2 * sleep_time # the maximum number of images that could be, calc since it's two images per second

# make sure the output folders exist
video_folder = '/home/pi/Videos/' + str(today) + '/' + str(hour) + '/'
if(False == path.exists(video_folder)):
    os.makedirs(video_folder)
    
# make the folders for the different levels of timelapse exist
for j in range(timelapse_levels):
    level_folder = 'level_'+str(j)
    level_folder = video_folder + level_folder
    if(False == path.exists(level_folder)):
        os.makedirs(level_folder)

# Create the Time lapse videos for the hours
print("Please standby as your timelapse video is created.")
for j in range(timelapse_levels):
    sleep(5) # sleep 5 seconds just to be sure that everything is ready.         
    level_folder = video_folder + 'level_'+str(j)  
    
    command = 'ffmpeg -r {} -f image2 -s {}x{} -nostats -loglevel 0 -pattern_type glob -i "{}/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p {}/TimeLapse_Level_{}_{}_hour_{}.mp4'.format(fps, x_res, y_res, hour_folder_name, level_folder, str(j), str(today), str(hour))
    print('Running Command: ', command)       
    
    perf_time = time.perf_counter()

    system(command)
    print('Timelapse video is complete. Video saved in ', level_folder)
    
    print('Timelapse of video took: ', str(time.perf_counter() - perf_time))
    perf_time = time.perf_counter()

    for i in range(numphotos):
        every = 2 ** (j+1)
        if(i%every != 0):
            file_name = hour_folder_name + '/image{0:06d}.jpg'.format(i)
            if(path.exists(file_name)):
                command = 'rm ' + file_name 
                #print('Removing File with command: ', command)
                system(command)
    
    print('Clean out files for next level took: ', str(time.perf_counter() - perf_time))

clear_folder = 'rm -r ' + hour_folder_name
print('Clearing folder using command: ', clear_folder)      
    
perf_time = time.perf_counter()     

system(clear_folder)    
print('Finished Removing Images Folder: ', hour_folder_name)
print('Cleaning up folder took: ', str(time.perf_counter() - perf_time))
