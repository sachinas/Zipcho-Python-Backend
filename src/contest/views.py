import os

import boto3
from botocore.exceptions import ClientError
from bson import ObjectId
from core.settings.base import (AWS_STORAGE_BUCKET_NAME, mongo_host,
                                mongo_port, mongo_proddbname, mongo_srv,
                                mongodb_databaseName, password, username)
from drf_spectacular.utils import extend_schema
from post.utils import get_collection_handle, get_db_handle
from rest_framework.decorators import (api_view, parser_classes,
                                       permission_classes)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .contestResponse import *
from .models import contest_type

CONTEST_COLLECTION = 'contest'
db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)
collection_handle = get_collection_handle(db_handle, CONTEST_COLLECTION)
'''
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


      
        newContest = collection_handle.insert_one(data)

        return Response({"status": 200,
                        "message": "Success",
                        "data": "data"}) 

    except ClientError as e:
        print("Client Error : ",e)

    except Exception as e :
        message = "Failed at createContest "
        print("Failed at createContest ", e)
        return Response({"status": 400,
                        "message": message,
                        "data": None}) '''
