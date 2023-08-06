# Created by  Sunkyeong Lee
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


def getSegmentInfo(segmentId):
    dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header

    createSeg = ags.getSegment(segmentId, False, "definition")
    
    return createSeg

def readCSV(csvFile):
    lines = open(csvFile).readlines()
    listCsv = []
    for line in lines[1:]:
        listCsv.append(line.split('\n')[0])

    return listCsv


#segment 이름이 있는 csv > segment id return
def idToList(segmentId):
    db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/segment'
    db_connection = create_engine(db_connection_str, encoding='utf-8')
    conn = db_connection.connect()

    query = """
    SELECT id FROM segment.tb_segment_list
    where name in ("{0}")
    """.format(listToStr(segmentId))
    
    result = pd.read_sql_query(query, conn)
    result_to_list = result['id'].values.tolist()
    conn.close()
    
    return result_to_list


def listToStr(segList):
    return '", "'.join(segList)


def createCSV(fileLoc, seg_id, seg_def):
    string = fileLoc + '\\' + str(seg_id) + '.json'
    with open(str(string), 'w', encoding='utf-8') as fileName:
        json.dump(seg_def, fileName, indent="\t")


def getSegmentDefinition(seg_id, current_seg, segment_archive):
    seg_def = getSegmentInfo(seg_id)
    createCSV(current_seg, seg_id, seg_def)
    createCSV(segment_archive, seg_id + '-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()), seg_def)


# if __name__ == '__main__':
#     seg_id = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/세그먼트 ID/seg_list.csv"
#     current_seg = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/segment List/current_segment"
#     segment_archive = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/segment List/segment_archive"
    
#     segmentName = readCSV(seg_id)
#     segment_id_list = idToList(segmentName)

#     for i in range(len(segment_id_list)):
#         seg_def = getSegmentInfo(segment_id_list[i])
#         createCSV(current_seg, segment_id_list[i], seg_def)
#         createCSV(segment_archive, segment_id_list[i] + '-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()), seg_def)
#         print("'{segment}' is saved.".format(segment = segmentName[i]))


