#!/usr/bin/env python

import subprocess
import os
import exifread
import time
from datetime import datetime, timedelta

PATH_TO_EXIF_TOOL = '~/Downloads/Image-ExifTool-10.02/exiftool '

def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

for dirpath,_dirnames,filenames in os.walk('.'):
    for filename in filenames:
        if filename.lower().endswith('.mts') :
            fullfilename = os.path.join(dirpath,filename)
            print('processing ' + fullfilename)
            timestamp = filename[:-6] + '.' + filename[-6:-4]
            output = subprocess.check_output([PATH_TO_EXIF_TOOL + fullfilename], shell = True)
            for line in output.splitlines():
                if line.startswith('Date/Time Original'):
                    original = line.split(': ')[1]
                    break
            originaltimezoneoffsethours = int(original[-6:][:-3])
            dt = datetime.strptime(original[:-6], "%Y:%m:%d %H:%M:%S")  + timedelta(hours=-originaltimezoneoffsethours)
            settime = unix_time(dt)
            os.utime(fullfilename, (settime,settime))
