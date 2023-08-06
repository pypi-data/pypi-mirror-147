# Created by Sunkyeong Lee
# Inquiry : sunkyeong.lee@concentrix.com / sunkyong9768@gmail.com


from copy import deepcopy
import pdb
import aanalytics2 as api2
import json
from itertools import *
from sqlalchemy import create_engine
import pandas as pd
import time
import os
from ast import literal_eval


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

def updateSegment(segmentID, jsonFile):
    dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header

    createSeg = ags.updateSegment(segmentID, jsonFile)
    
    return createSeg

def readJson(jsonFile):
    with open(jsonFile, 'r', encoding='UTF8') as bla:
        jsonFile = json.loads(bla.read())

    return jsonFile


def dumpJson(seg_location, seg_id, target):
    string = seg_location + '\\' + str(seg_id) + '-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '.json'
    with open(str(string), 'w', encoding='UTF8') as fileName:
        json.dump(target, fileName, indent="\t")


def idToList(segmentId):
    db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/segment'
    db_connection = create_engine(db_connection_str, encoding='utf-8')
    conn = db_connection.connect()

    query = """
    SELECT id FROM segment.tb_segment_list as seg
    left join segment.tb_segment_contains as cont
    on seg.name = cont.segment_name
    where segment_contains like '%%{0}%%'
    """.format(segmentId)
    
    result = pd.read_sql_query(query, conn)
    result_to_list = result['id'].values.tolist()
    conn.close()

    return result_to_list

# return 변경한 세그먼트 id 리스트로 반환
def segmentUpdate(component_seg, current_segment, segment_archive):
    # component segment의 이름을 seg_list 테이블에서 검색하여 id를 반환
    component_seg_str = ''.join(idToList_segList(component_seg))    
    # 반환된 id를 seg_contains의 테이블에서 조회하여 해당 세그먼트가 포함된 세그 id 반환
    seg_contains = idToList(component_seg_str)

    checkerList = []
    for i in range(len(seg_contains)):
        # 변경할 세그먼트의 old 버전 archive에 현재 날짜 붙여서 저장
        
        # 1. 파일 읽기
        seg_loc = current_segment + "\\" + seg_contains[i] + '.json'
        base_segment = readJson(seg_loc)
        segment_copy = deepcopy(base_segment)

        # 세그먼트 긁어 모으기
        if 'stream' in str(base_segment):
            base_seg = str(base_segment['definition']['container']['pred']['stream'])
            old_seg_json = str(readJson(fileFinder(component_seg_str, segment_archive, False))['definition']['container']['pred'])
            new_seg_json = str(readJson(fileFinder(component_seg_str, current_segment, True))['definition']['container']['pred'])

            # 변환 필요한 세그먼트가 base 세그먼트에 있는지 확인
            if old_seg_json in base_seg:
                checkerList.append(True)
            else:
                checkerList.append(False)

            base_seg_replaced = base_seg.replace(old_seg_json, new_seg_json)
            segment_copy['definition']['container']['pred']['stream'] = list(literal_eval(base_seg_replaced))
        
        else :
            base_seg = str(base_segment['definition']['container']['pred'])
            old_seg_json = str(readJson(fileFinder(component_seg_str, segment_archive, False))['definition']['container']['pred'])
            new_seg_json = str(readJson(fileFinder(component_seg_str, current_segment, True))['definition']['container']['pred'])

            if old_seg_json in base_seg:
                checkerList.append(True)
            else:
                checkerList.append(False)

        # 저장된 세그먼트에 옛날 세그먼트를 새로운 세그먼트로 변경 후
            base_seg_replaced = base_seg.replace(old_seg_json, new_seg_json)
            # json 형식에 변경한 부분 엎어치기
            segment_copy['definition']['container']['pred'] = literal_eval(base_seg_replaced)

        # 원 파일에 저장
        with open(str(seg_loc), 'w', encoding='utf-8') as fileName:
            json.dump(segment_copy, fileName, indent="\t")

        # archive old seg
        dumpJson(segment_archive, seg_contains[i], segment_copy)

    return seg_contains, checkerList

# Fianl Function
# UI에서 사용하지 않음
def updateSeg(component_seg, current_segment, segment_archive):

    seg_list = segmentUpdate(component_seg, current_segment, segment_archive)

    for i in range(len(seg_list)):
        seg_loc = current_segment + "\\" + seg_list[i] + '.json'

        print(updateSegment(seg_list[i], readJson(seg_loc)))

def idToList_segList(segmentId):
    db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/segment'
    db_connection = create_engine(db_connection_str, encoding='utf-8')
    conn = db_connection.connect()

    query = """
    SELECT id FROM segment.tb_segment_list
    where name = "{0}"
    """.format(segmentId)
    
    result = pd.read_sql_query(query, conn)
    result_to_list = result['id'].values.tolist()
    conn.close()
    
    return result_to_list

def fileFinder(component_segment, segment_folder, ifNew):
    if ifNew == True:
        newSeg = segment_folder + "\\" + component_segment + '.json'
        return newSeg
    
    else:
        segment_id_list = os.listdir(segment_folder)
        seg_cleaned = []
        for word in segment_id_list:
            if str(component_segment) in word:
                seg_cleaned.append(word)
        
        seg_cleaned.sort(reverse=True)
        right_before_seg_arc = seg_cleaned[1]

        oldSeg = segment_folder + "\\" + right_before_seg_arc
        return oldSeg

# if __name__ == "__main__":
#     component_seg = "[API Test] MX S22 Ultra Total Visit"
#     current_segment = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/segment List/current_segment"
#     segment_archive = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/segment List/segment_archive"

#     updateSeg(component_seg, current_segment, segment_archive)