from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account


import os
# import re
import io

import pdf2image
import tempfile
import datetime


# Google API
credentials = service_account.Credentials.from_service_account_file("APIKey.json")
client = vision.ImageAnnotatorClient(credentials=credentials)


def OCRscan(self, imgfile):

    print("Performing OCR Scan on the image ", imgfile)
    with io.open(imgfile, "rb") as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response_with_text = client.document_text_detection(image=image)
    document = response_with_text.full_text_annotation

    return document


def boxes_to_obj(self,bound):
   
    return {'x1': bound.vertices[0].x ,'x2':bound.vertices[1].x  ,
                'y1':bound.vertices[0].y  ,'y2':bound.vertices[2].y  }


def generateTempFolder(self, prifx, src):
    "Creating temp directory.."

    print("Creating temp directory.. with src and prefix .. ", prifx, src)
    # temp_dir = tempfile.mkdtemp(("-"+str(datetime.datetime.now()).replace(":", "-")), "PMR_Claims", self.cwd+os.sep
    #                             + "GENERATED"+os.sep+"CLAIMS")
    temp_dir = tempfile.mkdtemp(
        ("-"+str(datetime.datetime.now()).replace(":", "-")), prifx, src)

    print("Temp directory created", temp_dir)

    return temp_dir

def createSubDir(self, src, subDirNameList):
    print("Creating a subdirectory..")

    for subfolder_name in subDirNameList:
        os.makedirs(os.path.join(src, subfolder_name))


def getFilesindir(self, dire):
    print('Fetching the file in the directory')
    print(dire)
    return os.listdir(dire)
