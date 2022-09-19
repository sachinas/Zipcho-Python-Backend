import calendar
import os
import re
import time
from re import match, search

import boto3
from botocore.exceptions import ClientError
from bson import ObjectId
from core.settings.base import (AWS_ACCESS_KEY_ID, AWS_S3_REGION_NAME,
                                AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME,
                                mongo_host, mongo_port, mongo_proddbname,
                                mongo_srv, mongodb_databaseName, password,
                                username)
from drf_spectacular.utils import extend_schema
from post.utils import get_collection_handle, get_db_handle
from rest_framework.decorators import (api_view, parser_classes,
                                       permission_classes)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .constants import *
from .contestResponse import *
from .models import contest_type

CONTEST_COLLECTION = 'contest'
db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)
collection_handle = get_collection_handle(db_handle, CONTEST_COLLECTION)

def upload_to_s3(request,name, image):
    try :
        session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3 = boto3.resource('s3')
        gmt = time.gmtime()
        ts = calendar.timegm((gmt))

        filename = COVER_PIC_FOLDER + str(ts) + '_' + request.FILES['cover_pic'].name
        cover_pic = request.FILES['cover_pic']
        obj = s3.Object(AWS_STORAGE_BUCKET_NAME, filename)
        r = obj.put(Body=cover_pic)
        
    except Exception as e : 
        print("Failed while uploading to s3 ",e)

@extend_schema(methods=['get'],
                responses={200: fetchContestTypeResponse, 400: ErrorResponseContest})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchContestType(request):
    try :
        print("at fetchContestType")
        contestData = list(contest_type.objects.all().values())
      
        finalData = []

        for i in range(len(contestData)):
            temp = {}
            temp['id'] = contestData[i]['id']
            temp['contest_type'] = contestData[i]['contest_type']
            temp['is_active'] = int(contestData[i]['is_active'])
            finalData.append(temp)


        return Response({"status": 200,
                        "message": "Success",
                        "data": finalData}) 
       
    except Exception as e :
        message = "Failed at contestType "
        print("Failed at contestType ", e)
        return Response({"status": 400,
                        "message": message,
                        "data": None}) 

@extend_schema(methods=['POST'],request = createContestRequest, 
                responses={200: createContestResponse, 400: ErrorResponseContest})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createContest(request):
    try :
        print("at create Contest")
        data = request.data
        
        # cover_pic
        assert data['cover_pic'] != None , \
            'Cover pic cannot be null'
        assert len(data['cover_pic']) != 0 , \
            'Cover pic cannot be empty'

        '''# display_pic
        assert data['display_pic'] != None , \
            'display pic cannot be null'
        assert len(data['display_pic']) != 0 , \
            'display pic cannot be empty'''


        

        '''
        
                {
            "cover_pic": "https://zipchodev.s3.ap-south-1.amazonaws.com/contest/cover_pic/eventCoverPic.jpg",
            "display_pic": "https://zipchodev.s3.ap-south-1.amazonaws.com/contest/cover_pic/eventCoverPic.jpg",
            "contest_title": "S ar ga ",
            "start_date_time":  "2022-09-15T00:00:00.000+00:00",
            "category_id": "1",
            "contestType_id" : "1",
            "isPaid":  1
        }

        # contest_title        
        assert data['contest_title'] != None , \
            'contest Title cannot be null'
        assert len(data['contest_title']) != 0 , \
            'contest Title cannot be empty'
        if re.search(isSpace, data['contest_title']):
            raise Exception('contest Tile format cannot contain spaces alone')
        if not re.search(contestNamePattern, data['contest_title']) :
            raise Exception('invalid contest Tile format')
         
        # start_date_time
        assert data['start_date_time'] != None , \
            'start_date_time cannot be null'
        assert len(data['start_date_time']) != 0 , \
            'start_date_time cannot be empty'
        if re.search(isSpace, data['start_date_time']):
            raise Exception('start_date_time format cannot contain spaces alone')

        # category_id
        assert data['category_id'] != None , \
            'category_id cannot be null'
        assert len(data['category_id']) != 0 , \
            'category_id cannot be empty'
        if re.search(isSpace, data['category_id']):
            raise Exception('category_id format cannot contain spaces alone')
        if not re.search(idPattern, data['category_id']) :
            raise Exception('invalid category_id format')
        
        # contestType_id 
        assert data['contestType_id'] != None , \
            'contestType_id cannot be null'
        assert len(data['contestType_id']) != 0 , \
            'contestType_id cannot be empty'
        if re.search(isSpace, data['contestType_id']):
            raise Exception('contestType_id format cannot contain spaces alone')
        if not re.search(idPattern, data['contestType_id']) :
            raise Exception('invalid contestType_id format')

        # isPaid 
        assert data['isPaid'] != None , \
            'isPaid cannot be null'
        if not re.search(booleanPattern, str(data['isPaid'])) :
            raise Exception('invalid isPaid format')

        # fee
        if not re.search(feePattern, str(data['isPaid'])) :
            raise Exception('invalid isPaid format')'''



        #newContest = collection_handle.insert_one(data)

        return Response({"status": 200,
                        "message": "Success",
                        "data": url}) 

    except ClientError as e:
        print("Client Error : ",e)

    except Exception as e :
        message = "Failed at createContest "
        if e.args[0] != message : 
            message = str(e.args[0])
        print("Failed at createContest ", e)

        return Response({"status": 400,
                        "message": message,
                        "data": None}) 
