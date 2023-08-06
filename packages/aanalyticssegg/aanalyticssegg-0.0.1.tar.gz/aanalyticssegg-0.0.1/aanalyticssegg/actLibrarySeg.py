# Created by Sunkyeong Lee
# Inquiry : sunkyeong.lee@concentrix.com / sunkyong9768@gmail.com

import aanalytics2 as api2
import json
from copy import deepcopy
from itertools import *
import csv
import os
from ast import literal_eval
from sqlalchemy import create_engine
import pandas as pd
import time

def dataInitiator():
    api2.configure()
    logger = api2.Login() 
    logger.connector.config

def createSegment(jsonFile):
    dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header

    createSeg = ags.createSegment(jsonFile)
    
    return createSeg

def readJson(jsonFile):
    with open(jsonFile, 'r', encoding='UTF8') as bla:
        jsonFile = json.loads(bla.read())

    return jsonFile

def pullFromLib(ownerId, segment):
    segJson = readJson(segment)
    segJson_temp = deepcopy(segJson)
    newName = segJson_temp['name'] + ' (Pulled from Lib)'

    segJson['name'] = newName
    segJson["owner"]["id"] = ownerId

    return segJson

# if __name__ == "__main__":
#     owner_id = 200121276
#     segmentArchive = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/segment List/segment_archive/s200001591_61daebb793dba82b8dc8b6bf-20220305-165903.json"
#     # segJson = readJson(segmentArchive)
    # segJson_temp = deepcopy(segJson)
    # newName = segJson_temp['name'] + ' (Pulled from Lib)'

    # segJson['name'] = newName
    # segJson["owner"]["id"] = owner_id

    # print(createSegment(segJson))

    