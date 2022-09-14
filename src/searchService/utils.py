from authentication.models import User, profile
from bson import ObjectId
from core.settings.base import (mongo_host, mongo_port, mongo_proddbname,
                                mongo_srv, mongodb_databaseName, password,
                                username)
from django.db import connection
from pymongo import MongoClient

from zipchoAdmin.models import category, interest
from .models import *

def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]

def get_db_handle(db_name, mongo_srv):
    try :
        client = MongoClient(mongo_srv)
        db_handle = client[db_name]
        return db_handle, client
    except Exception as e : 
        print("Failed while connecting to mongoDB srv : ",e)

db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)

def getHash_Post():
    try:
        finalData = []
        c=0

        hashtags = list(map(lambda x : {"post_id":x['_id'],
                                        "hashtags":x['hashtags'].replace(' ',''),
                                        "categoryId":x['categoryId']},
                         db_handle.posts.find({"hashtags":{'$ne':None}} ,#, "categoryId":{'$ne': None}}, 
                                            {"_id":0, "hashtags": 1, "_id": 1,
                                            "categoryId":1})))
        
        for i in range(len(hashtags)):
        
            if hashtags[i]['hashtags'] is not None :
                data = hashtags[i]['hashtags'].split("#")
                for j in range(len(data)):
                    temp = {}
                    if data[j] != '' and data[j] != 'string':
                        temp['id'] = c 
                        temp['hashtag'] = data[j]
                        temp['post_id'] = hashtags[i]['post_id']
                        temp['categoryId'] = hashtags[i]['categoryId']
                        finalData.append(temp)
                        c=c+1 
        return finalData

    except Exception as e : 
        print("Failed while getHash_Post : ",e)

def dictFetchAll(cursor):
    columns = [col[0] for col in cursor.description]
    
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getUserCategoryDetails(data):
    try :
        print("at selecting getUserCategoryDetails ")
        
        user = User.objects.get(id = data['userId'])
        
        with connection.cursor() as cursor : 
            categoryQuery = f"SELECT \
                                  zc.id,\
                                  zc.category,\
                                  IF(COALESCE(ui.interest_id AND c.category_id) IS NULL,\
                                      0,\
                                      1) AS isSelected\
                              FROM\
                                  zipchoAdmin_category zc\
                                      JOIN\
                                  authentication_userinterest ui ON ui.interest_id = zc.interest_id\
                                      AND ui.user_id = %s\
                                      LEFT JOIN\
                                  authentication_usercategory c ON zc.id = c.category_id AND c.user_id = %s; "

            cursor.execute(categoryQuery, [user.id, user.id])
            interestData = dictFetchAll(cursor)
           
            finalData = [] 
            #data = map(lambda n : n if interestData[index]['isSelected'] == 0 else 0, enumerate(interestData))
            temp = {}
         
            for i in range(len(interestData)) :
                if interestData[i]['isSelected'] == 1: 
                    '''temp = {}
                    temp['id'] = interestData[i]['id']
                    temp['category'] = interestData[i]['category']'''
                    #finalData.append(interestData[i]['category'])
                    finalData.append(interestData[i]['id'])
            
        return finalData

    except Exception as e: 
        print("Failed at getUserCategoryDetails ", e)

        return 0