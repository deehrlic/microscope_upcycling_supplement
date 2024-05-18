import numpy as np
import subprocess
import yaml, os, cv2, time
import boto3, botocore
import logging
import os
from datetime import datetime
import json

experimentname = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
return_value, image = camera.read()
#print(return_value)

if return_value:
    writepath = "C:/Users/somet/OneDrive/Documents/zstacks/stills/" + experimentname + ".png"
    windowspath = "C:\\Users\\somet\\OneDrive\\Documents\\zstacks\\stills\\" + experimentname + ".png"
    cv2.imwrite(writepath, image)
    print("IMAGE SAVED TO: " + writepath)
    s3 = boto3.client('s3', endpoint_url="https://s3.braingeneers.gi.ucsc.edu")
    try:
        response = s3.upload_file(writepath,"streamscope","stills/" + experimentname + ".png")
        print(response)
    except botocore.exceptions.ClientError as e:
        logging.error(e)
        print(e)
del(camera)
