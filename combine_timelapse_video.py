# combine_timelapse_video.py
# This file turns the Hourly Timelapse Videos into a single larger video
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

# How many days should it advance to get to the stoping point
days_combine = 1 # edit this if combining videos only from a single day, or across many days
delta_day = datetime.timedelta(days=1)

# What date should it start at
default_start = datetime.date.today() - datetime.timedelta(days=days_combine)
year = default_start.year #2021 # change this to set a specific date to start at
month = default_start.month # 5
day = default_start.day #21

# The begining and ending hour of the timelapse to run
start_hour = 22 # Edit this to change what hour is the starting hour
end_hour = 6 # Edit this to change what hour is the ending hour

# Repeat the process for every Timelapse Level
for j in range(timelapse_levels):
    level_folder = 'level_'+str(j)        
        
    # Create the date object and start generating the list of files that need to be merged
    working_date = datetime.datetime(year, month, day)
    working_hour = start_hour
        
    # build a list of all the timelapses to merge together.
    list_of_timelapses = []
    i = 0 # count as we process days until it's processed the correct number of days
    while( i <= days_combine):
        
        while((working_hour < 24 and i < days_combine) or (working_hour <= end_hour and i == days_combine)):
            # Find the folder and file file name of the Timelaps to include 
            video_folder = '/home/pi/Videos/' + str(working_date.date()) + '/' + str(working_hour) + '/' + level_folder
            full_file_path = video_folder + '/TimeLapse_Level_{}_{}_hour_{}.mp4'.format(str(j), str(working_date.date()), str(working_hour))
            list_of_timelapses.append(full_file_path)
            
            # Increment the hour by 1
            working_hour += 1
            
        # reset the Hour to 0 and increment the day
        working_hour = 0
        working_date += delta_day # increment the day by 1
        i+=1 # incrment i to eventually exit the loop

    # debugging
    print('List of timelapses: ', list_of_timelapses)
    
    # use a temp file to hold the hourly timelapse files paths
    temp_file = 'timelapses_temp.txt'
    # Clean up if there is another temp file sitting there
    if(path.exists(temp_file)):
        command = 'rm ' + temp_file 
        print('Removing File with command: ', command)
        system(command)
        
    # write to a temp file of the timelapse file names
    write_file = open(temp_file, 'w')
    for hour_path in list_of_timelapses:
        write_txt = 'file \''+hour_path+'\' \n'
        write_file.write(write_txt)
    write_file.close()
    
    # create the Output folder for the timelapses
    output_folder =  '/home/pi/timelapses/' + str(working_date.date()) + '/' + level_folder
    if(False == path.exists(output_folder)):
        os.makedirs(output_folder)
    
    output_file = output_folder + '/Combined_TimeLapse_Level_{}_{}.mp4'.format(str(j), str(working_date.date()))
    
    # finally, join them all together into one video and save that one
    # One option is to write a file that has all the file locations and then pass that to 
    join_command = 'ffmpeg -f concat -safe 0 -nostats -loglevel 0 -i {} -c copy {}'.format(temp_file, output_file)

    print('Running Join Command: ', join_command)
    
    perf_time = time.perf_counter()
    #
    system(join_command)
    #
    print('Joining Timelapse video is complete. Video saved in ', output_file)    
    print('Joining Timelapse of videos took: ', str(time.perf_counter() - perf_time))
    perf_time = time.perf_counter()

    # Clean up the temp file
    if(path.exists(temp_file)):
        command = 'rm ' + temp_file 
        print('Removing File with command: ', command)
        system(command)

print('Done!')
