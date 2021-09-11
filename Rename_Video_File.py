
import math
import pandas as pd
import numpy as np
import os
import re

import time
import pytesseract as tess

import cv2 

directory='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Input/Quali/'
ArchiveDir ='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Input/Quali/Archive'


def Rename_Video_File(filename, directory):

    img = cv2.VideoCapture(directory + filename)

    img.set(1, 1)
    success, image = img.read()
    ret, currentFrame = img.read()

    # cv2.imshow("frame", currentFrame)
    # cv2.waitKey()

    try:
        roi_track = currentFrame[16:43, 14:83]

        roi_name1 = currentFrame[128:156, 261:478]

        roi_Q = currentFrame[1249:1275, 1267:1311]
    except:
        pass

    Digit_Config = r'--oem 3 --psm 6 outputbase digits'
    Lap_Config = r'--oem 3 tessedit_char_whitelist=0123456789/ --psm 13'


    roi_name1 = cv2.cvtColor(roi_name1, cv2.COLOR_BGR2GRAY)
    (thresh, roi_name1) = cv2.threshold(roi_name1, 127, 255, cv2.THRESH_BINARY)

    Name1 = tess.image_to_string(roi_name1, lang='eng', config='--psm 6')
    Name1 = re.sub('',"", Name1)
    Name1 = re.sub('\n',"", Name1)
    Name1 = re.sub('2',"Z", Name1)



    roi_track = cv2.blur(roi_track, (2, 2))         
    roi_track = cv2.cvtColor(roi_track, cv2.COLOR_BGR2GRAY)
    (thresh, roi_track) = cv2.threshold(roi_track, 185, 255, cv2.THRESH_BINARY)
    roi_track = cv2.blur(roi_track, (2, 2))

    # cv2.imshow('Track', roi_track)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    # cv2.waitKey(1)


    Track = tess.image_to_string(roi_track, lang='eng', config='--psm 6')
    Track = re.sub('',"", Track)
    Track = re.sub('\n',"", Track)



    ### Q
    roi_Q = cv2.cvtColor(roi_Q, cv2.COLOR_BGR2GRAY)


    Qnum = tess.image_to_string(roi_Q, config='--psm 6')
    Qnum = re.sub('',"", Qnum)
    Qnum = re.sub('\n',"", Qnum)
    Qnum = re.sub('i',"1", Qnum)


    return Track, Name1, Qnum

def LoopThru():
    for filename in os.listdir(directory):
        if filename.endswith(".mov") or filename.endswith(".mp4") or filename.endswith("."):

            cred = Rename_Video_File(filename, directory)

            New_filename = '%s_%s_%s.mov'%(cred)

            if filename != New_filename:
                os.rename((os.path.join(directory, filename)),(os.path.join(directory, New_filename)))
                print(filename, 'renamed as:', New_filename)
                print('\n\n\n')

# LoopThru()
def Infinite():
    while True:
        LoopThru()
        print('Looking for Video to Rename!')
        time.sleep(1)

# Infinite()