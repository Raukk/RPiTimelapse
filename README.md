# RPiTimelapse
Simple Python scripts for a robust Raspberry Pi based Timelapse Camera

## Why?

I wrote this code because I wanted to record a timelapse of my sleep.

I decided to use a RasPi because I could reuse it for other projects once I am done with the timelapses, and it already has a simple NoIR camera that comes with IR LEDs to iluminate the room.  

I wans't satisfied with any of the timelapse scripts I saw when googling, so I started throwing together my own.

## Hardware

![Hardware](./Time_Lapse_Cam_V1.png)

The hardware is a Raspi 4 (8GB), 64GB SD card, a NoIR cammera module, and some 3M wall tabs.

https://www.amazon.com/dp/B0759GYR51/ref=cm_sw_r_cp_apa_glt_fabc_EAY2AARVAEMHM364CBNP?_encoding=UTF8&psc=1

https://www.amazon.com/dp/B08DJ9MLHV/ref=cm_sw_r_cp_apa_glt_fabc_990RNZQ3B3P95Z7BYDF4?_encoding=UTF8&psc=1

https://www.amazon.com/dp/B08879MG33/ref=cm_sw_r_cp_apa_glt_fabc_4KMAKR15VKDWTX67D9Z2?_encoding=UTF8&psc=1

On my hardware, with the settings and code as is, the capture rate is 2 images per second.
Creating Timelapse Video for 1 hours worth of images takes about 15 minutes. 
Note: the timelapse images and videos can take a lot of space, so, small SD cards may have issues.

Note: 
If you run this on other hardware, you will probably have to tweak things.

## Setup

It is assumed that the OS & SD card are set up, that the camera is installed & enabled, and the timezone is set.

The `.py` files are expected to be writen into the directory `/home/pi/`

For it to run on boot, use the command `sudo crontab -e` and paste the contents of the file [Crontab](./Crontab) into it.

## Use

At this point, it should be simple plug and play to record timelapses.

It is also assumed that you will have a way to interact with it when you desire to retrieve the Timelapse video(s).
Mine is connected to wifi, and has `ssh` set up to access the console, I retrieve the timelapse files using `scp` 


### Combining Hours into one Video

The file [combine_timelapse_video.py](./combine_timelapse_video.py) is used to combine many hour timelapse videos into a single video for download or viewing.

The default values in the file are from 10 pm the night before to 6:59 am today, but this can be changed by changing the variables `start_hour` `end_hour` `days_combine` 

If you want it to not end on today's date, then you need to adjust the variable `default_start` to be the desired start date.



### Manual running hours that failed

If the Pi is powered off when the hour switches to the next (or during the timelapse video creation) then that hour will not be processed.

The code does not yet go back to 'fix' hours that were not processed, but the images can be processed by manually running the script [manual_hourly_timelapse_video.py](./manual_hourly_timelapse_video.py)

You will need to edit it to give it the correct Date and Hour to run the process for (will eventually take command line args).
I do this with `sudo nano manual_hourly_timelapse_video.py` and then alter the value of the variable `hour` and if needed, the value of `today` to the desired day. 



### Other Uses

If you wish to use this for other things like night sky timelapses, you will probably want to tweak it quite a bit.
Feel free to submit pull requests or bug reports if the changes don't impact other uses. 

## Misc

Note: Python and Linux are not my daily drivers, so, if I made a dumb mistake, let me know.


