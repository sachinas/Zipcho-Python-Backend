
import json
import os
import random
import sys
from datetime import datetime
from re import match, search

from authentication.models import User, profile
from authentication.utils import dictFetchAll, getS3FileUrl
from bson import ObjectId
from core.settings.base import (mongo_host, mongo_port, mongo_proddbname,
                                mongo_srv, mongodb_databaseName, password,
                                username)
from django.core.paginator import Paginator
from django.db import connection
from drf_spectacular.utils import extend_schema
from post.postResponse import *
from post.utils import *
from post.utils import get_db_handle, getHastags
from rest_framework.decorators import (api_view, parser_classes,
                                       permission_classes)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from zipchoAdmin.models import category

from .constants import *
from .models import *
from .searchResponse import *
from .utils import *

db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)

@extend_schema(methods=['post'], request = searchPeopleRequest,
                    responses={200: searchPeopleResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def people(request):
    try :
        print("at searching People ")
        loginUser = User.objects.get(id = request.user.id)
        data = request.data
        query2 = ""
        found = False
        finalData = []

        searchKeyword = data['keyword']
        
        if searchKeyword != None and searchKeyword != '':
            searchKeyword = searchKeyword.lower()
            print(f"searchKeyword : {searchKeyword}")
            # category
            allCategory = list(map(lambda x : x.lower(), category.objects.all().values_list("category",flat=True)))
            print(allCategory)
            
            if searchKeyword in allCategory:
                print("Search by category")
                #ind = (*allCategory,).index(searchKeyword) + 1
                ind = (allCategory).index(searchKeyword) + 1
                query2 = "byCategory"
                found = True
                
            
            if query2 == '' or query2 == None : 
                # first_name
                firstNameData = User.objects.filter(first_name__icontains=searchKeyword).values_list('first_name', flat=True)
                d = map(lambda x: match(searchKeyword.lower(), x.lower()), firstNameData)

                print("--")
                for i in d : 
                    if i != None : 
                        query2 = " WHERE first_name LIKE '" + str(searchKeyword) + "%%' "
                        found = True
                        break
            
            print("query2 - ",query2)
            # last_name
            if query2 == '' or query2 == None : 
                print(f"search by last_name")
                lastNameData = User.objects.filter(last_name__icontains=searchKeyword).values_list('last_name', flat=True)
                d = map(lambda x: match(searchKeyword.lower(), x.lower()), lastNameData)
              
                for i in d : 
                    if i != None : 
                        query2 = " WHERE last_name LIKE '" + str(searchKeyword) + "%%' "
                        found = True
                        break
            # username
            if query2 == '' or query2 == None : 
                print(f"search by username")
                userNameData = User.objects.filter(username__icontains=searchKeyword).values_list('username', flat=True)
                d = map(lambda x: match(searchKeyword.lower(), x.lower()), userNameData)
                print("--")
                for i in d : 
                    if i != None : 
                        query2 = " WHERE username LIKE '" + str(searchKeyword) + "%%' "
                        found = True
                        break
        
       
        if searchKeyword == None or searchKeyword == '': 
            print("Search Keyword is empty")
            query2 = " LIMIT 20"
        
            
        if query2 != '': 
            print(f"QUERY 2 - {query2}")
            if query2 == 'byCategory':
                print(f"ind : {ind}")
                #1. Get all post that belong to certain category 
                categoryPostCursor = list(map(lambda x : str(x['_id']), (db_handle.posts.find({'categoryId':str(ind)},
                                                        {"_id":1}))))

                #2. Find  who created the post
                print("ID of post")
                print(categoryPostCursor)
                with connection.cursor() as cursor : 
                    query1 = "SELECT \
                                    distinct usr.id,\
                                    usr.username,\
                                    usr.first_name,\
                                    usr.last_name,\
                                    p.profileImage\
                                FROM\
                                    authentication_user usr\
                                        JOIN\
                                    authentication_profile p ON p.user_id = usr.id\
                                		JOIN \
                                	post_userpost post ON usr.id = post.user_id\
                                    where post.post_id in %s;"

                    getBasicDataQuery = query1 
                    cursor.execute(getBasicDataQuery, [categoryPostCursor,])
                    basicData = dictFetchAll(cursor)

            if query2 != "byCategory" :
                with connection.cursor() as cursor : 
                    query1 = "SELECT  \
                                distinct usr.id,  \
                                usr.username, \
                                usr.first_name, \
                                usr.last_name, \
                                p.profileImage \
                            FROM \
                                authentication_user usr \
                                    JOIN \
                                authentication_profile p ON p.user_id = usr.id "

                    getBasicDataQuery = query1 + query2 
                    cursor.execute(getBasicDataQuery)
                    basicData = dictFetchAll(cursor)
                    #print(f"Basic Data : {basicData}")

            for i in range(len(basicData)):
                try : 
                    print(basicData[i]['username']) 
                    temp = {}
                    temp['id'] = basicData[i]['id']
                    temp['username'] = basicData[i]['username']
                    temp['fullname'] = basicData[i]['first_name'] + ' ' + basicData[i]['last_name']
                    temp['profileImage'] = getS3FileUrl(basicData[i]['profileImage'])
                    
                    '''followingCursor = list(db_handle.follow.find({"userId": str(loginUser.id), 
                                                             "followingId": str(basicData[i]['id'])
                                                           }))
                    print(followingCursor)                                                       
                    if len(followingCursor) == 0 : 
                        temp['isConnected'] = 0
                    else :                     
                        temp['isConnected'] = followingCursor[0]['status']'''

                    print(f"str(loginUser.id) : {str(loginUser.id)}")
                    print(f"str(basicData[i]['id'] : {str(basicData[i]['id'])}")
                    

                    isConnectedCursor = db_handle.follow.find({"userId": str(loginUser.id), 
                                                             "followingId": str(basicData[i]['id'])
                                                           })
                    d = 0
                    isClone = len(list(isConnectedCursor.clone()))

                    print(f"isClone : {isClone}")
                    if isClone == 0 : 
                        temp['isConnected'] = 2
                        d = 1

                    if isClone != 0: 
                        print("hereeee ")
                        for i in isConnectedCursor :
                            temp['isConnected'] = i['status']
                            d = 1

                    if d == 0 : 
                        temp['isConnected'] = 0  

                    interactionData = getInteractionDetails({'userId': int(temp['id'])})
                    temp['canTag'] = int(interactionData[0]['mentions'])
                    temp['canMessage'] = int(interactionData[0]['messages'])

                    finalData.append(temp)
                    print("======================") 
                except Exception as e :
                    print(f"Something went wrong while Searching people : {e}")
            return Response({"status": 200, "message":"Success", "data":finalData})
        
        if found == False : 
            return Response({"status": 200, "message":"Success", "data":finalData})
        
    except Exception as e: 
        message = "Failed while searching People "
        if e.args[0] != None : 
            message = e.args[0]
        
        print("Failed while searching People : ",e)
        return Response({"status": 400,"message":message, "data": None})

@extend_schema(methods=['post'], request = searchHashtagRequest,
                    responses={200: searchHashtagResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def hashtagsDetails(request):
    try :
        print("at search hashtags")
        loginUser = User.objects.get(id = request.user.id)
        data = request.data
        query2 = ""
        finalData = []

        searchKeyword = data['keyword']
        c=0

        hashtagsData = getHastags()
        
        if searchKeyword == None or searchKeyword == '': 
            return Response({"status": 200, "message":"Success", "data":hashtagsData})
        
        for i in range(len(hashtagsData)):
            print(hashtagsData[i]['hashtag'])
            if search(searchKeyword.lower(), hashtagsData[i]['hashtag'].lower()): 
                finalData.append(hashtagsData[i])
                print("FOUND")
        
        return Response({"status": 200, "message":"Success", "data":finalData})

    except Exception as e: 
        message = "Failed while searching hashtag "
        if e.args[0] != None : 
            message = e.args[0]
        
        print("Failed while searching hashtag : ",e)
        return Response({"status": 400,"message":message, "data": None})


@extend_schema(methods=['post'], request = searchPhotoRequest,
                    responses={200: searchPhotoResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def photo(request):
    try :
        print("at searching Photos ")
        loginUser = User.objects.get(id = request.user.id)
        data = request.data
        query2 = ""
        found = False
        finalData = []
        finalPostData = []
        ind = 0

        searchKeyword = data['keyword']

        print("Hashtags  :")

        hp = getHash_Post()
        userCat = getUserCategoryDetails({"userId": loginUser.id})

        tempPosts = []
        
        if searchKeyword != None and searchKeyword != '':
            searchKeyword = searchKeyword.lower()
            print(f"searchKeyword : {searchKeyword}")
           
            # hastags
            if query2 == '' or query2 == None : 
                print(f"search by hastags in posts ")

                # Category 
                allCategory = list(map(lambda x : x.lower(), category.objects.all().values_list("category",flat=True)))
                print(f"search by category in posts ")
            
                if searchKeyword in allCategory:
                    print("Search by category")
                    #ind = (*allCategory,).index(searchKeyword) + 1
                    ind = (allCategory).index(searchKeyword) + 1
                    query2 = "byCategory"
                    found = True

                print("here")
                print(hp)
                if not hp is None :
                    for i in range(len(hp)):
                        if ( hp[i]['hashtag'].lower() == searchKeyword and \
                            hp[i]['post_id'] not in tempPosts ) or \
                            hp[i]['categoryId'] == str(ind): 
                            tempPosts.append(hp[i]['post_id'])
                            found = True
                            query2 = "byHashtag"
            

        if searchKeyword == None or searchKeyword == '': 
            print("Search Keyword is empty so fetching category based photos ")
            #allCategory = list(map(lambda x : x.lower(), category.objects.all().values_list("category",flat=True)))
            
            indexes = []
            for i in range(len(userCat)):
                print("Search by category")
                #indexes.append(str(i + 1))
                indexes.append(str(userCat[i]))
                query2 = "byCategory"
                found = True

            print(f"Indexes : {indexes}")
            if not hp is None :
                for i in range(len(hp)):
                    if hp[i]['categoryId'] in indexes: 
                    
                        tempPosts.append(hp[i]['post_id'])
                        found = True
                        query2 = "byCategory"
        

        print(tempPosts)
                        
        print(f"ind : {ind}")
            
        if query2 != '': 
            print(f"QUERY 2 - {query2}")
            
            POST_COLLECTIONS = 'posts'
            db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)
            collection_handle = get_collection_handle(db_handle, POST_COLLECTIONS)
            loginUser = User.objects.get(id = request.user.id)
            

            # {_id:{$in:[ObjectId('62ea004973ce3e3467cccc15')]}}
            posts = db_handle.posts.find({
                "_id" :{
                    "$in" : tempPosts
                    }
                }).sort("_id", -1)

            #print(posts)        
            #print(type(posts))
            for i in posts : 
                try :      
                   
                   
                    print(f"POST ----------------------------------------------- {str(i['_id'])}")
                    file_name, file_format = os.path.splitext(i['mediaUrl'])
                    print(f"format : {file_format}")


                    if file_format in IMAGE_FILE_FORMATS : 
                        temp = {}
                        #temp['type'] = 1
                        temp['_id'] = str(i['_id'])
                        #temp['loginUser'] = loginUser.id

                        userPostData = userPost.objects.get(post_id =  str(i['_id']))
                        user = User.objects.get(id = userPostData.user_id)
                        profileData = profile.objects.get(user_id = user.id)
       
                        print(user.id)
                        
                        temp['createdById'] = user.id
                        temp['createdByUsername'] = user.username
                        temp['profileImage'] = profileData.profileImage.url
                        temp['loginUser'] = loginUser.id

                        likes = getLikesDetails(temp, db_handle)
                      
                        if likes[1] == 0 :
                            temp['likedBy'] = []
                            temp['likes'] = 0
                            temp['isLiked'] = likes[2]

                        else :
                            temp['likedBy'] = likes[0]
                            temp['likes'] = likes[1]
                            temp['isLiked'] = likes[2]

                        com = fetchCommentsDetails(temp)
                        temp['comments'] = com
                        temp['totalComments'] = len(com)

                        temp['caption'] = i['caption']
                        temp['visibility'] = i['visibility']
                        
                        if i['taggedUser'] is not None : 
                            temp['taggedUser'] = getBasicDetails(i['taggedUser'])    
                        else : 
                            temp['taggedUser'] = i['taggedUser']
                       

                        temp['hashtags'] = i['hashtags']
                        temp['mediaUrl'] = i['mediaUrl']
                        temp['key'] = i['key']

                        temp['latitude'] = i['latitude']
                        temp['longitude'] = i['longitude']
                        temp['address'] = i['address']
                        temp['date'] = i['date']
                        

                        bmCursor = list(db_handle.bookmarks.find({'post_id': str(i['_id']),
                                                                'userId': request.user.id}))
                        if len(bmCursor) >= 1 : 
                            temp['isBoomarked'] = 1
                        else : 
                            temp['isBoomarked'] = 0

                        if i['categoryId'] is not None : 
                            temp['categoryId'] = i['categoryId']
                            temp['categoryName'] = category.objects.get(id=i['categoryId']).category
                       
                        else:  
                            temp['categoryId'] = None 
                            temp['categoryName'] = None 
                        
                        temp['mediaType'] = i['mediaType']
                        temp['aspectRatio'] = i['aspectRatio']

                        interactionData = getInteractionDetails({'userId': user.id})
                        temp['canSharePost'] = int(interactionData[0]['posts'])
                        temp['canComment'] = int(interactionData[0]['comments'])

                        finalPostData.append(temp)
                            
                except Exception as e:
                    print("Some myWorks posts had key value issues")

           

            return Response({"status": 200, "message":"Success", "data":finalPostData})
        
        if found == False : 
            print("Nothing Found ")
            return Response({"status": 200, "message":"Success", "data":finalPostData})
        
    except Exception as e: 
        message = "Failed while searching Photos "
        if e.args[0] != None : 
            message = e.args[0]
        
        print("Failed while searching Photos : ",e)
        return Response({"status": 400,"message":message, "data": None})

@extend_schema(methods=['post'], request = searchVideoRequest,
                    responses={200: searchVideoResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def video(request):
    try :
        print("at searching video ")
        loginUser = User.objects.get(id = request.user.id)
        data = request.data
        query2 = ""
        found = False
        finalData = []
        finalPostData = []
        ind = 0

        searchKeyword = data['keyword']

        print("Hashtags  :")

        hp = getHash_Post()
        userCat = getUserCategoryDetails({"userId": loginUser.id})

        tempPosts = []
        
        if searchKeyword != None and searchKeyword != '':
            searchKeyword = searchKeyword.lower()
            print(f"searchKeyword : {searchKeyword}")
           
            # hastags
            if query2 == '' or query2 == None : 
                print(f"search by hastags in posts ")

                # Category 
                allCategory = list(map(lambda x : x.lower(), category.objects.all().values_list("category",flat=True)))
                print(f"search by category in posts ")
            
                if searchKeyword in allCategory:
                    print("Search by category")
                    #ind = (*allCategory,).index(searchKeyword) + 1
                    ind = (allCategory).index(searchKeyword) + 1
                    query2 = "byCategory"
                    found = True

                print("here")
                print(hp)
                if not hp is None :
                    for i in range(len(hp)):
                        if ( hp[i]['hashtag'].lower() == searchKeyword and \
                            hp[i]['post_id'] not in tempPosts ) or \
                            hp[i]['categoryId'] == str(ind): 
                            tempPosts.append(hp[i]['post_id'])
                            found = True
                            query2 = "byHashtag"
            

        if searchKeyword == None or searchKeyword == '': 
            print("Search Keyword is empty so fetching category based photos ")
            #allCategory = list(map(lambda x : x.lower(), category.objects.all().values_list("category",flat=True)))
            
            indexes = []
            for i in range(len(userCat)):
                print("Search by category")
                #indexes.append(str(i + 1))
                indexes.append(str(userCat[i]))
                query2 = "byCategory"
                found = True

            print(f"Indexes : {indexes}")
            if not hp is None : 
                for i in range(len(hp)):
                    if hp[i]['categoryId'] in indexes: 
                    
                        tempPosts.append(hp[i]['post_id'])
                        found = True
                        query2 = "byCategory"
            

        print(tempPosts)
                        
        print(f"ind : {ind}")
            
        if query2 != '': 
            print(f"QUERY 2 - {query2}")
            
            POST_COLLECTIONS = 'posts'
            db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)
            collection_handle = get_collection_handle(db_handle, POST_COLLECTIONS)
            loginUser = User.objects.get(id = request.user.id)
            

            # {_id:{$in:[ObjectId('62ea004973ce3e3467cccc15')]}}
            posts = db_handle.posts.find({
                "_id" :{
                    "$in" : tempPosts
                    }
                }).sort("_id", -1)

            #print(posts)        
            #print(type(posts))
            for i in posts : 
                try :      
                    temp = {}
                   
                    print(f"POST ----------------------------------------------- {str(i['_id'])}")
                    file_name, file_format = os.path.splitext(i['mediaUrl'])
                    print(f"format : {file_format}")


                    if file_format in VIDEO_FILE_FORMATS : 
                        temp = {}
                        #temp['type'] = 1
                        temp['_id'] = str(i['_id'])
                        #temp['loginUser'] = loginUser.id

                        userPostData = userPost.objects.get(post_id =  str(i['_id']))
                        user = User.objects.get(id = userPostData.user_id)
                        profileData = profile.objects.get(user_id = user.id)
       
                        print(user.id)
                        
                        temp['createdById'] = user.id
                        temp['createdByUsername'] = user.username
                        temp['profileImage'] = profileData.profileImage.url
                        temp['loginUser'] = loginUser.id

                        likes = getLikesDetails(temp, db_handle)
                      
                        if likes[1] == 0 :
                            temp['likedBy'] = []
                            temp['likes'] = 0
                            temp['isLiked'] = likes[2]

                        else :
                            temp['likedBy'] = likes[0]
                            temp['likes'] = likes[1]
                            temp['isLiked'] = likes[2]

                        com = fetchCommentsDetails(temp)
                        temp['comments'] = com
                        temp['totalComments'] = len(com)

                        temp['caption'] = i['caption']
                        temp['visibility'] = i['visibility']
                        
                        if i['taggedUser'] is not None : 
                            temp['taggedUser'] = getBasicDetails(i['taggedUser'])    
                        else : 
                            temp['taggedUser'] = i['taggedUser']
                       

                        temp['hashtags'] = i['hashtags']
                        temp['mediaUrl'] = i['mediaUrl']
                        temp['key'] = i['key']

                        temp['latitude'] = i['latitude']
                        temp['longitude'] = i['longitude']
                        temp['address'] = i['address']
                        temp['date'] = i['date']
                        

                        bmCursor = list(db_handle.bookmarks.find({'post_id': str(i['_id']),
                                                                'userId': request.user.id}))
                        if len(bmCursor) >= 1 : 
                            temp['isBoomarked'] = 1
                        else : 
                            temp['isBoomarked'] = 0

                        if i['categoryId'] is not None : 
                            temp['categoryId'] = i['categoryId']
                            temp['categoryName'] = category.objects.get(id=i['categoryId']).category
                       
                        else:  
                            temp['categoryId'] = None 
                            temp['categoryName'] = None 
                        
                        temp['mediaType'] = i['mediaType']
                        temp['aspectRatio'] = i['aspectRatio']

                        interactionData = getInteractionDetails({'userId': user.id})
                        temp['canSharePost'] = int(interactionData[0]['posts'])
                        temp['canComment'] = int(interactionData[0]['comments'])

                        finalPostData.append(temp)
                            
                except Exception as e:
                    print("Some myWorks posts had key value issues")

            return Response({"status": 200, "message":"Success", "data":finalPostData})
        
        if found == False : 
            print("Nothing Found ")
            return Response({"status": 200, "message":"Success", "data":finalPostData})
        
    except Exception as e: 
        message = "Failed while searching Video "
        if e.args[0] != None : 
            message = e.args[0]
        
        print("Failed while searching Video : ",e)
        return Response({"status": 400,"message":message, "data": None})


@extend_schema(methods=['post'], request = searchAllRequest,
                    responses={200: searchAllResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def allSearch(request):
    try :
        print("at allSearch ")
        loginUser = User.objects.get(id = request.user.id)
        data = request.data
        query2 = ""
        found = False
        finalData = []
        finalPostData = []
        ind = 0

        searchKeyword = data['keyword']

        print("Hashtags  :")

        hp = getHash_Post()
        userCat = getUserCategoryDetails({"userId": loginUser.id})

        tempPosts = []
        
        if searchKeyword != None and searchKeyword != '':
            searchKeyword = searchKeyword.lower()
            print(f"searchKeyword : {searchKeyword}")
           
            # hastags
            if query2 == '' or query2 == None : 
                print(f"search by hastags in posts ")

                # Category 
                allCategory = list(map(lambda x : x.lower(), category.objects.all().values_list("category",flat=True)))
                print(f"search by category in posts ")
            
                if searchKeyword in allCategory:
                    print("Search by category")
                    #ind = (*allCategory,).index(searchKeyword) + 1
                    ind = (allCategory).index(searchKeyword) + 1
                    query2 = "byCategory"
                    found = True

                print("here")
                print(hp)
                if not hp is None :
                    for i in range(len(hp)):
                        if ( hp[i]['hashtag'].lower() == searchKeyword and \
                            hp[i]['post_id'] not in tempPosts ) or \
                            hp[i]['categoryId'] == str(ind): 
                            tempPosts.append(hp[i]['post_id'])
                            found = True
                            query2 = "byHashtag"
            

        if searchKeyword == None or searchKeyword == '': 
            print("Search Keyword is empty so fetching category based photos ")
            #allCategory = list(map(lambda x : x.lower(), category.objects.all().values_list("category",flat=True)))
            
            indexes = []
            for i in range(len(userCat)):
                print("Search by category")
                #indexes.append(str(i + 1))
                indexes.append(str(userCat[i]))
                query2 = "byCategory"
                found = True

            print(f"Indexes : {indexes}")
            if not hp is None :
                for i in range(len(hp)):
                    if hp[i]['categoryId'] in indexes: 
                    
                        tempPosts.append(hp[i]['post_id'])
                        found = True
                        query2 = "byCategory"
            

        print(tempPosts)
                        
        print(f"ind : {ind}")
            
        if query2 != '': 
            print(f"QUERY 2 - {query2}")
            
            POST_COLLECTIONS = 'posts'
            db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)
            collection_handle = get_collection_handle(db_handle, POST_COLLECTIONS)
            loginUser = User.objects.get(id = request.user.id)
            

            # {_id:{$in:[ObjectId('62ea004973ce3e3467cccc15')]}}
            posts = db_handle.posts.find({
                "_id" :{
                    "$in" : tempPosts
                    }
                }).sort("_id", -1)

            print(posts)        
            print(type(posts))
            for i in posts : 
                try :      
                   
                    print(f"POST ----------------------------------------------- {str(i['_id'])}")
                    file_name, file_format = os.path.splitext(i['mediaUrl'])
                    print(f"format : {file_format}")


                    if file_format in IMAGE_FILE_FORMATS or file_format in VIDEO_FILE_FORMATS : 
                        temp = {}
                        #temp['type'] = 1
                        temp['_id'] = str(i['_id'])
                        #temp['loginUser'] = loginUser.id

                        userPostData = userPost.objects.get(post_id =  str(i['_id']))
                        user = User.objects.get(id = userPostData.user_id)
                        profileData = profile.objects.get(user_id = user.id)
       
                        print(user.id)
                        
                        temp['createdById'] = user.id
                        temp['createdByUsername'] = user.username
                        temp['profileImage'] = profileData.profileImage.url
                        temp['loginUser'] = loginUser.id

                        likes = getLikesDetails(temp, db_handle)
                      
                        if likes[1] == 0 :
                            temp['likedBy'] = []
                            temp['likes'] = 0
                            temp['isLiked'] = likes[2]

                        else :
                            temp['likedBy'] = likes[0]
                            temp['likes'] = likes[1]
                            temp['isLiked'] = likes[2]

                        com = fetchCommentsDetails(temp)
                        temp['comments'] = com
                        temp['totalComments'] = len(com)

                        temp['caption'] = i['caption']
                        temp['visibility'] = i['visibility']
                        
                        if i['taggedUser'] is not None : 
                            temp['taggedUser'] = getBasicDetails(i['taggedUser'])    
                        else : 
                            temp['taggedUser'] = i['taggedUser']
                       

                        temp['hashtags'] = i['hashtags']
                        temp['mediaUrl'] = i['mediaUrl']
                        temp['key'] = i['key']

                        temp['latitude'] = i['latitude']
                        temp['longitude'] = i['longitude']
                        temp['address'] = i['address']
                        temp['date'] = i['date']
                        

                        bmCursor = list(db_handle.bookmarks.find({'post_id': str(i['_id']),
                                                                'userId': request.user.id}))
                        if len(bmCursor) >= 1 : 
                            temp['isBoomarked'] = 1
                        else : 
                            temp['isBoomarked'] = 0

                        if i['categoryId'] is not None : 
                            temp['categoryId'] = i['categoryId']
                            temp['categoryName'] = category.objects.get(id=i['categoryId']).category
                       
                        else:  
                            temp['categoryId'] = None 
                            temp['categoryName'] = None 
                        
                        temp['mediaType'] = i['mediaType']
                        temp['aspectRatio'] = i['aspectRatio']

                        interactionData = getInteractionDetails({'userId': user.id})
                        temp['canSharePost'] = int(interactionData[0]['posts'])
                        temp['canComment'] = int(interactionData[0]['comments'])

                        finalPostData.append(temp)
                            
                except Exception as e:
                    print("Some myWorks posts had key value issues")

           

            return Response({"status": 200, "message":"Success", "data":finalPostData})
        
        if found == False : 
            print("Nothing Found ")
            return Response({"status": 200, "message":"Success", "data":finalPostData})
        
    except Exception as e: 
        message = "Failed while searching allSearch "
        if e.args[0] != None : 
            message = e.args[0]
        
        print("Failed while searching allSearch : ",e)
        return Response({"status": 400,"message":message, "data": None})
