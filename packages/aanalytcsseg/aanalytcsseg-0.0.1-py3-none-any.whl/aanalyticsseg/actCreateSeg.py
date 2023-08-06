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


def exportToCSV(dataSet, fileName):
    dataSet.to_csv(fileName, sep=',', index=False)


def readJson(jsonFile):
    with open(jsonFile, 'r', encoding='UTF8') as bla:
        jsonFile = json.loads(bla.read())

    return jsonFile

### New
def readCSV(csvFile):
    lines = open(csvFile).readlines()
    
    listCsv = []
    for line in lines[1:]:
        listCsv.append(line.split('\n')[0])

    return listCsv


def createSegment(jsonFile):
    dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header

    createSeg = ags.createSegment(jsonFile)
    
    return createSeg

# 리스트 형식으로 return
def getJsonList(path):
    file_lst = os.listdir(path)

    jsonList = []
    for file in file_lst:
        filepath = path + '/' + file
        jsonList.append(readJson(filepath))
        
    return jsonList

### New
def getJsonListCsv(path, fileLists):

    jsonList = []
    for file in fileLists:
        filepath = path + '/' + file + '.json'
        jsonList.append(readJson(filepath))
        
    return jsonList


# 220227
def getjsonDict(component, jsonList):
    jsonDict = {}
    for i in range(len(jsonList)):
        jsonDict[component[i]] = str(jsonList[i]['definition']['container'])

    return jsonDict

# 220227
def getSegmentId(component, jsonList):
    jsonDict = {}
    for i in range(len(jsonList)):
        jsonDict[component[i]] = str(jsonList[i]['id'])

    return jsonDict


# input : list
# pull all possible options
def getAllCases_original(dataset):
    
    dataset_list = []
    for i in range(1, len(dataset)):
        #permutations
        printList = list(combinations(dataset, i+1))
        dataset_list.append(printList)

    # 중첩 리스트 제거
    dataset_list_raw = []
    for i in range(len(dataset_list)):
        for j in range(len(dataset_list[i])):
            dataset_list_raw.append(dataset_list[i][j])

    return dataset_list_raw


# List로 out
def setSegment(dataset, ifKey, head):
    segmentList = []
    for i in range(len(dataset)):
        if ifKey == True:
            name = head + " " + ' > '.join(dataset[i])
            segmentList.append(name)
        else:
            value = ','.join(dataset[i])
            segmentList.append(value)

    return segmentList

def stackTodb(dataFrame, dbTableName):
    print(dataFrame)
    db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/segment'
    db_connection = create_engine(db_connection_str, encoding='utf-8')
    conn = db_connection.connect()

    dataFrame.to_sql(name=dbTableName, con=db_connection, if_exists='append', index=False)
    print("finished")

# input대로 중첩 리스트 만들기
def createIndex(seg_index):
    # seg_index = "segmentApi\gmc_input_segment\cnx_seg_index.csv"
    index = readCSV(seg_index)

    lst = []
    for i in range(len(index)):
        temp = list(index[i])
        lst.append(temp)

    # 리스트 내 중복 값 제거
    for i in range(len(lst)):
        while ',' in lst[i]:
            lst[i].remove(',')
    
    for i in range(len(lst)):
        while '"' in lst[i]:
            lst[i].remove('"')
        
    return lst


def getAllCases(base_seg, input_index):
    index = createIndex(input_index)
    index_temp = deepcopy(index)
    
    for i in range(len(index)):
        for j in range(len(index[i])):
            index_temp[i][j] = base_seg[int(index[i][j])-1]

    return index_temp


### NEW
def getSegment(seg_list_csv, segment_archive, current_segment, input_index, head, ownerId):

    seg_list = splitSegList(seg_list_csv)[1]
    
    seg_def_json = getJsonListCsv(current_segment, idToList(seg_list))
    seg_component = splitSegList(seg_list_csv)[0]
    
    # getFileName
    jsonDict = getjsonDict(seg_component, seg_def_json)
    jsonSeg = getSegmentId(seg_component, seg_def_json)

    # Description : 딕셔너리를 key, value로 분리
    jsonKey = []
    jsonValue = []
    for key, value in jsonDict.items():
        jsonKey.append(key)
        jsonValue.append(value)

    # Segment ID : 딕셔너리를 key, value로 분리
    jsonSegKey = []
    jsonSegValue = []
    for key, value in jsonSeg.items():
        jsonSegKey.append(key)
        jsonSegValue.append(value)

    # 경우의 수로 만들기
    segmentName = setSegment(getAllCases(jsonKey, input_index), True, head)
    segmentValue = setSegment(getAllCases(jsonValue, input_index), False, head)

    # Segment
    segmentIdList = { 'segment_name': setSegment(getAllCases(jsonSegKey, input_index), True, head),
                    'segment_contains' : setSegment(getAllCases(jsonSegValue, input_index), False, head)}

    stackTodb(pd.DataFrame(segmentIdList), 'tb_segment_contains')

    # template
    targetFile = ownerIdChange(ownerId)
    # targetFile = readJson('SegmentCreate/userflow_template.json')
    target = deepcopy(targetFile)  
    
    # 변경 후 호출
    segmentInfo = []
    for i in range(len(segmentName)):
        target['name'] = segmentName[i]
        target['definition']['container']['pred']['stream'] = list(literal_eval(segmentValue[i]))

        callSegment = createSegment(target)
        print(callSegment)
        
        # string = 'C:\\Users\Administrator\OneDrive - Concentrix Corporation\Documents\★Segment\segment_list\\' + str(callSegment["id"]) + '.json'
        current_seg_def = current_segment + '\\' + str(callSegment["id"]) + '.json'
        seg_arc_def = segment_archive + '\\' + str(callSegment["id"]) + '-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '.json'
        jsonMaker(current_seg_def, target)
        jsonMaker(seg_arc_def, target)

        segmentInfo.append(callSegment)


    segmentList = pd.DataFrame(segmentInfo).drop(["description", "owner", "isPostShardId", "rsid"], axis=1)
    stackTodb(segmentList, 'tb_segment_list')


def jsonMaker(seg_def, target):
    with open(str(seg_def), 'w', encoding='utf-8') as fileName:
        json.dump(target, fileName, indent="\t")


def createSegList(segListCsv):
    seg_list = readCSV(segListCsv)
    
    doubleSegList = []
    for i in range(len(seg_list)):
        doubleSegList.append(seg_list[i].split(','))
    
    return doubleSegList

def idToList(segmentId):
    db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/segment'
    db_connection = create_engine(db_connection_str, encoding='utf-8')
    conn = db_connection.connect()

    result_list = []
    for i in range(len(segmentId)):
        query = """
        SELECT id FROM segment.tb_segment_list
        where name = "{0}"
        """.format(segmentId[i])
    
        result = pd.read_sql_query(query, conn)
        result_to_list = ''.join(result['id'].values.tolist())
        result_list.append(result_to_list)

    conn.close()
    
    return result_list

def listToStr(segList):
    return '", "'.join(segList)

def splitSegList(seg_list_csv):
    segmentList_double = createSegList(seg_list_csv)
    component = []
    segName = []
    for i in range(len(segmentList_double)):
        component.append(segmentList_double[i][0])
        segName.append(segmentList_double[i][1])

    return component, segName

def ownerIdChange(ownerId):
    template = """
    {
    "name": "[Test] Home > PFS",
    "description": "Created by API",
    "rsid": "sssamsung4mstglobal",
    "reportSuiteName": "P6 WEB - MST Global",
    "owner": {
      "id": 200150002,
      "name": "string",
      "login": "string"
    },
    "definition": {
        "func":"segment",
        "version":[ 1, 0, 0 ],
        "container": {
            "func": "container",
            "context": "visits",
            "pred": {
                "func": "sequence",
                "stream": [
                    {
                        "func":"container",
                        "context":"hits",
                        "pred": {
                            "func": "streq",
                            "str": "home",
                            "val": {
                                "func":"attr", "name":"variables/prop6"
                            }
                        }
                    },
                    {
                        "func":"container",
                        "context":"hits",
                        "pred": {
                            "func": "streq",
                            "str": "product family showcase",
                            "val": {
                                "func":"attr", "name":"variables/prop6"
                            }
                        }
                    }
                ]
            }
        }
    },
    "compatibility": {
      "valid": true,
      "message": "string",
      "validator_version": "string",
      "supported_products": [
        "string"
      ],
      "supported_schema": [
        "string"
      ],
      "supported_features": [
        "string"
      ]
    },
    "definitionLastModified": "2021-08-22T06:19:00.458Z",
    "categories": [
      "string"
    ],
    "siteTitle": "string",
    "tags": [
      {
        "id": 0,
        "name": "string",
        "description": "string",
        "components": [
          {
            "componentType": "string",
            "componentId": "string",
            "tags": [
              "Unknown Type: Tag"
            ]
          }
        ]
      }
    ],
    "modified": "2021-08-22T06:19:00.458Z",
    "created": "2021-08-22T06:19:00.458Z"
  }"""
    targetFile = json.loads(template)
    targetFile["owner"]["id"] = ownerId

    return targetFile 

# if __name__ == "__main__":
#     seg_list_csv = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/세그먼트 생성/세그먼트 리스트.csv"
#     current_segment = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/segment List/current_segment"
#     segmen_archive = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/segment List/segment_archive"
#     input_index = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/세그먼트 생성/세그먼트 순서.csv"
#     header = "[API Test] S20 FE"
#     ownerID = 200121276

#     getSegment(seg_list_csv, segmen_archive, current_segment, input_index, header, ownerID)

#     # seg_list = splitSegList(seg_list_csv)[1]


    # db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/segment'
    # db_connection = create_engine(db_connection_str, encoding='utf-8')
    # conn = db_connection.connect()
    
    # result_list = []
    # for i in range(len(seg_list)):
    #     query = """
    #     SELECT id FROM segment.tb_segment_list
    #     where name = "{0}"
    #     """.format(seg_list[i])
    
    #     result = pd.read_sql_query(query, conn)
    #     result_to_list = ''.join(result['id'].values.tolist())
    #     result_list.append(result_to_list)
    
    # conn.close()
    # print(result_list)
    # # print(idToList(seg_list))