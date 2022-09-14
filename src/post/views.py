
import json
import random
import re
import sys
from datetime import datetime
from re import match, search

from authentication.models import User, interactions, profile
from authentication.utils import getInteractionDetails, getS3FileUrl
from bson import ObjectId
from core.settings.base import (mongo_host, mongo_port, mongo_proddbname,
                                mongo_srv, mongodb_databaseName, password,
                                username)
from django.core.paginator import Paginator
from django.db import connection
from drf_spectacular.utils import extend_schema
from notificationService.models import notifications
from rest_framework.decorators import (api_view, parser_classes,
                                       permission_classes)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from zipchoAdmin.models import category

from .constants import *
from .models import *
from .postResponse import *
from .utils import *

#from .utils import get_collection_handle, get_db_handle, getLikesDetails

POST_COLLECTIONS = 'posts'


db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)

'''
db_handle, mongo_client = get_db_handle(mongodb_databaseName,mongo_host,
                                        int(mongo_port),
                                      username, password) '''
 
collection_handle = get_collection_handle(db_handle, POST_COLLECTIONS)


@extend_schema(methods=['post'], request = getAllUserPostsRequest,
                responses={200: getAllUserPostResponse, 400 : ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getAllUserPosts(request):
    try :
        print("at getAllUserPosts")
        data = request.data 
        viewerId = data['viewerId']

        loginUser = User.objects.get(id = request.user.id)
        user = User.objects.get(id=int(viewerId))

        isConnected = len(list(db_handle.follow.find({"userId": str(loginUser.id),
                                                   "followingId": str(user.id),
                                                   "status" : 1})))
        if isConnected == 1 or user.isPrivate == 0 or loginUser.id == user.id:
            profileData = profile.objects.get(user_id = user.id)
            userPostData = userPost.objects.filter(user=user)\
                            .values_list("post_id", flat=True)\
                            .order_by('-id')
            print(f"userPostData : {userPostData}")
            print(type(userPostData))
            print(len(userPostData))

            '''p = collection_handle.find({"_id":ObjectId("62bc21352f0a5f71036be556")})
            print("iss")
            print(p)
            print(type(p))'''

            posts = map(lambda x : collection_handle.find({"_id":ObjectId(x)}), userPostData)
            print("iss")
            print(posts)
            print(type(posts))
            finalPostData = []

            for post in posts :
                
                for i in post :
                    try : 
                        temp = {}
                        temp['_id'] = str(i['_id'])
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
                        #temp['likes'] = i['likes']
                        #temp['comment'] = i['comment']               
                        temp['visibility'] = i['visibility']


                        #toList = list(map(int, i['visibility'].split(",")))
                        #print(f"size of list : {toList}")
                        #print(sys.getsizeof(toList))
                        
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
                                                                'userId': loginUser.id}))
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

                        print(f"interactionData : {interactionData}")

                        finalPostData.append(temp)
                        print("--------------------------------------------------")

                    except Exception as e:
                        print(f"Some posts had key value issues : {e}")
        
            return Response({"status": 200,"message": "Success", "data": finalPostData}) 
        
        else : 
            message = "This account is private"
            return Response({"status": 403,"message": message, "data": None})     
    
    except Exception as e: 
        print("Failed at getAllPosts: " ,e)
        message= "Failed while Fetching Posts"
        return Response({"status": 400,"message": message, "data": None}) 

@extend_schema(methods=['post'], request = userPostRequest,
                    responses={200: userPostResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
#@parser_classes((MultiPartParser,))
def userPosts(request):
    try :
        print("at Entering userPosts ")
        user = User.objects.get(id = request.user.id)
        data = request.data
        now = datetime.now()
        data['date'] = now

        if data['visibility'] is None or \
            data['visibility'] == '' or \
            not re.search(str(visibilityPattern), data['visibility']):
            raise Exception("Invalid visibility format")
        
        if data['categoryId'] is not None and \
            data['categoryId'] != '' and \
            not re.search(idPattern, data['categoryId']):
            raise Exception("Invalid categoryId format")

        # mediaUrl Validation
        if data['mediaUrl'] is None or \
            data['mediaUrl'] == '' or \
            data['key'] is None or \
            data['key'] == '' :
            raise Exception("Invalid mediaUrl or key format")
        
        else : 
            mediaUrls = data['mediaUrl'].split(",")
            keys = data['key'].split(",")

            if len(mediaUrls) != len(keys):
                raise Exception("Invalid mediaUrl or key format")

            for i in range(len(mediaUrls)):
                if not re.search(mediaUrlPattern, mediaUrls[i]) or \
                    not re.search(keyPattern, keys[i]):
                    raise Exception("Invalid mediaUrl or key format")
        
        

        # latitude validation
        if data['latitude'] is None:
            pass
        elif len(data['latitude']) == 0 :
            pass
        else :
            if not re.search(latlongPattern, str(data['latitude'])):
                raise Exception("invalid latitude format")

        # longitude validation
        if data['longitude'] is None:
            pass
        elif len(data['longitude']) == 0 :
            pass
        else :
            if not re.search(latlongPattern, str(data['longitude'])):
                raise Exception("invalid longitude format")
           
        taggedUser = data['taggedUser']
        if len(taggedUser) != 0: 
            for i in range(len(taggedUser)):
                if taggedUser[i]['userId'] is None or \
                    taggedUser[i]['userId'] == "" or \
                    not re.search(userIdPattern, taggedUser[i]['userId']):
                    raise Exception("Invalid UserId Format")
        
        #hashtags validation
        if data['hashtags'] is None :
            pass
        elif len(data['hashtags']) == 0 : 
            pass
        else :
            hashtags = data['hashtags'].split(" ")
           
            if len(hashtags) != 0:
                for i in range(len(hashtags)):
                    if not re.search(hashtagPattern, hashtags[i]):
                        raise Exception("Invalid hashtag format ") 
                    
        nP = collection_handle.insert_one(data)

        msg = f"{user.username} has tagged you in a post"

        for i in range(len(taggedUser)):
            notifications.objects.create(userId_id = int(taggedUser[i]['userId']),
                                    fromId_id = user.id,
                                    notification = msg,
                                    date = datetime.now())

        '''nP = collection_handle.insert_one({
            "caption" : data['caption'], 
            "visibility" : data['visibility'],
            "taggerUser" : data['taggedUser'],
        })'''

        #"taggerUser" : data['taggedUser'],
            #"location" : data['location'],
            #"hashtags" : data['hashtags']
        print(f"Created in Mongodb :{nP.inserted_id}")
        # <class 'bson.objectid.ObjectId'>
        print(type(nP.inserted_id))
        
        # 2 : Create a row in mysql db with the _id generated above 
        newUserPost, created = userPost.objects.get_or_create(
                                user = user,
                                post_id = nP.inserted_id)
        
        return Response({"status": 200,"message":"Success"})

    except Exception as e: 
        message = "Failed while creating user post "
        if e.args[0] != None : 
            message = e.args[0]
        
        print("Failed while creating user post : ",e)
        return Response({"status": 400,"message":message, "data": None})

@extend_schema(methods=['delete'], request = deletePostRequest,
                    responses={200: deletePostResponse, 400: ErrorResponsePortfolio})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePost(request,post_id):
    try :
        print("at Deleting userPosts ")
        user = User.objects.get(id = request.user.id)
        #data = request.data
        data = {}
        data['post_id'] = str(post_id)

        print(f"post_id : {post_id}")

        now = datetime.now()

        userPosts = userPost.objects.get(post_id = data['post_id'])
        
        if userPosts.user_id != user.id : 
            raise Exception("Permission Denied")
        else : 
            print("Deleting Post, Comments, Likes, Bookmarks ")
            userPosts.delete()
            db_handle.posts.delete_one({"_id":ObjectId(str(data['post_id']))})
            db_handle.comments.delete_many({"post_id":str(data['post_id'])})
            db_handle.likes.delete_many({"post_id":str(data['post_id'])})
            db_handle.bookmarks.delete_many({"post_id":str(data['post_id'])})
        
        return Response({"status": 200,"message":"Success"})

    except Exception as e: 
        message = "Failed while deleting user post "
        if e.args[0] != None : 
            message = e.args[0]
        if e.args[0] == 'Permission Denied':
            message = e.args[0]
            return Response({"status": 400,"message":message, "data": None})
        
        print("Failed while deleting user post : ",e)
        return Response({"status": 400,"message":message, "data": None})

@extend_schema(methods=['post'], request = updatePostRequest,
                    responses={200: updatePostResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatePost(request):
    try :
        print("at Updating userPosts ")
        user = User.objects.get(id = request.user.id)
        data = request.data
        now = datetime.now()

        userPosts = userPost.objects.get(post_id = data['post_id'])
        
        if userPosts.user_id != user.id : 
            raise Exception("Permission Denied")
        else : 
            print("Updating Post")
            post_id = userPosts.post_id
            print(f"post_id : {post_id}")
            
            filter = { "_id": ObjectId(post_id) }
            # {'_id': ObjectId('62f255735b11e8bd1f1ab0a4'), 'caption': 'Dream Team', 'visibility': '1', 'taggedUser': [{'userId': '3'}],
            # 'hashtags': '#dance', 'mediaUrl': 'https://zipchodev.s3.ap-south-1.amazonaws.com/zipchodev%2FportfolioImages%2F1660048103teamPic44.jpg', 
            # 'key': 'zipchodev/portfolioImages/1660048103teamPic44.jpg',
            #  'latitude': '10.2321', 'longitude': '11.231', 'address': 'Kerala', 'categoryId': '7', 
            # 'date': datetime.datetime(2022, 8, 9, 12, 39, 15, 952000)}
           
            updatedValues = {}
            
            postCursor= db_handle.posts.find(filter)
            for i in postCursor:
                print(i)
                if data['caption'] != None:
                    updatedValues['caption'] = data['caption']

                if data['visibility'] != None:
                    updatedValues['visibility'] = data['visibility']

                if data['taggedUser'] != None:
                    updatedValues['taggedUser'] = data['taggedUser']

                if data['hashtags'] != None:
                    updatedValues['hashtags'] = data['hashtags']
                
                if data['latitude'] != None:
                    updatedValues['latitude'] = data['latitude']

                if data['longitude'] != None:
                    updatedValues['longitude'] = data['longitude']

                if data['address'] != None:
                    updatedValues['address'] = data['address']
                
                if data['categoryId'] != None:
                    updatedValues['categoryId'] = data['categoryId']

                newvalues = { "$set" : updatedValues }
                db_handle.posts.update_one(filter, newvalues)

            
        return Response({"status": 200,"message":"Success","data":[]})

    except Exception as e: 
        message = "Failed while updating user post "
        if e.args[0] != None : 
            message = e.args[0]
        if e.args[0] == 'Permission Denied':
            message = e.args[0]
            return Response({"status": 400,"message":message, "data": None})
        
        print("Failed while updating user post : ",e)
        return Response({"status": 400,"message":message, "data": None})

@extend_schema(methods=['post'], request = fetchCommentsRequest,
                    responses={200: fetchCommentsResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fetchComments(request):
    try :
        finalPostData = []
        print("at getComments")
        data = request.data
        postId = data['postId']
        print(f"POST ID :{postId}")
        user = User.objects.get(id=request.user.id)
        userPostData = userPost.objects.filter(user=user).values_list("post_id", flat=True)
        print(f"userPostData : {userPostData}")
        
        comments = db_handle.comments.find({"post_id":postId})
        
        l = len(list(comments.clone()))
        print(f"details of commenst  : {l}")

        for comment in comments : 
          
            temp = {}
            temp['comment'] = comment['comment']
            temp['likes'] = comment['likes']
            temp['date'] = comment['date']
            temp['post_id'] = comment['post_id']
            temp['comment_id'] = str(comment['_id'])
            temp['userId'] = comment['userId']
            temp['username'] = comment['username']
            profileData = profile.objects.get(user_id = comment['userId'])
            temp['profileImage'] = profileData.profileImage.url
          
            replyComments = db_handle.replyComments.find({"comment_id":str(comment['_id'])})
            replyData = []
            for replyComment in replyComments : 
              
                temp2 = {}
                temp2['comment'] = replyComment['comment']
                temp2['likes'] = replyComment['likes']
                temp2['date'] = replyComment['date']
                temp2['userId'] = replyComment['userId']
                temp2['userName'] = replyComment['username']
                profileData = profile.objects.get(user_id = replyComment['userId'])
                temp2['profileImage'] = profileData.profileImage.url
          
                replyData.append(temp2)
            
            temp['replies'] = replyData
      
            finalPostData.append(temp)
        return Response({"status": 200,"message": "Success", "data": finalPostData}) 
        
    except Exception as e: 
        print("Failed at getComments: " ,e)
        message= "Failed while Fetching getComments"
        return Response({"status": 400,"message": message, "data": None}) 


@extend_schema(methods=['post'], request = commentsRequest,
                    responses={200: commentsResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])    
def comment(request):
    try :
        finalPostData = []
        print("at posting a comment")
        
        data = request.data
        user = User.objects.get(id = request.user.id)
        print( data['type'])
        print(type( data['type']))
        now = datetime.now()
        print(f"NOW - {now}")
        if int(data['type']) == 1 : # HardCoded replace with Static
            print("newComment -->")
            newComment = db_handle.comments.insert_one({
                'userId' : user.id,
                'username' : user.username,
                'comment' : data['comment'],
                'post_id': data['post_id'],
                'likes': None,
                "date": now
            })

            # Notify other user for comment
            postOwner = userPost.objects.get(post_id = str(data['post_id']))
            
            if user.id != postOwner.user_id:
                print(f"Notify for comment")
                msg = f"{user.username} has commented on your post"
                notifications.objects.create(userId_id = postOwner.user_id,
                                            fromId_id = user.id,
                                            notification = msg,
                                            date = datetime.now())

            comments = db_handle.comments.find({"_id":ObjectId(newComment.inserted_id)})

            for comment in comments : 
             
                temp = {}
                temp['comment'] = comment['comment']
                temp['likes'] = comment['likes']
                temp['date'] = comment['date']
                temp['post_id'] = comment['post_id']
                temp['comment_id'] = str(comment['_id'])
                temp['userId'] = comment['userId']
                temp['username'] = comment['username']

                finalPostData.append(temp)

        elif int(data['type']) == 2 : # Hardcoded replace with static 
            newReplyComment = db_handle.replyComments.insert_one({
                'userId' : user.id,
                'username' : user.username,
                'comment' : data['comment'],
                'comment_id' : data['comment_id'],
                'likes': None,
                "date": now
            })
            
            comments = db_handle.comments.find({"_id":ObjectId(newReplyComment.inserted_id)})

            for comment in comments : 
          
                temp = {}
                temp['comment'] = comment['comment']
                temp['likes'] = comment['likes']
                temp['date'] = comment['date']
                temp['post_id'] = comment['post_id']
                temp['comment_id'] = str(comment['_id'])
                temp['userId'] = comment['userId']
                temp['username'] = comment['username']

                finalPostData.append(temp)

        
        else:
            
            raise Exception("Unkown Comment Type")

        return Response({"status": 200,"message": "Success", "data": finalPostData}) 
        
    except Exception as e: 
        message= "Failed while Posting a Comment"
        if e.args[0] == 'Unkown Comment Type':
            message = "Unkown Comment Type"
        print("Failed at getComments: " ,e)
       
        return Response({"status": 400,"message": message, "data": None}) 


@extend_schema(methods=['post'],request = getMyWorksRequest,
                responses={200: getAllMyWorksResponse, 400 : ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getMyWorks(request):
    try :
        print("at getMyWorks")
        data = request.data 
        viewerId = data['viewerId']

        user = User.objects.get(id=int(viewerId))
        loginUser = User.objects.get(id = request.user.id)
        
        profileData = profile.objects.get(user_id = user.id)
        userPostData = userPost.objects.filter(user=user)\
                        .values_list("post_id", flat=True)\
                        .order_by('-id')

        isConnected = len(list(db_handle.follow.find({"userId": str(loginUser.id),
                                                   "followingId": str(user.id),
                                                   "status" : 1})))
        if isConnected == 1 or user.isPrivate == 0 or loginUser.id == user.id:

            print(f"userPostData : {userPostData}")
            print(type(userPostData))
            print(len(userPostData))

            '''p = collection_handle.find({"_id":ObjectId("62bc21352f0a5f71036be556")})
            print("iss")
            print(p)
            print(type(p))'''

            posts = map(lambda x : collection_handle.find({"_id":ObjectId(x)}), userPostData)
            print("iss")
            print(posts)
            print(type(posts))
            finalPostData = []
            myWorks = []
    
            userInterests = []
            userCategories = []
            existingPosts = posts

            for post in posts :
                temp = {}
                myInterest=""
                temp2 = {}
                
                for i in post :
                
                    temp2 = {}
                    userPosts = []
                    try :
                        print(f"Finding Category : {i['categoryId']}")
                        interests = getUserInterests(user.id, i['categoryId'])
                        myInterest = interests[0]['interest']
                        print("------------------------")
                        print("interests[0]['interest']")
                        print(interests[0]['interest'])

                        print("userInterests")
                        print(userInterests)

                        print("i['categoryId']")
                        print(i['categoryId'])
                        print("------------------------")

                        #if  interests[0]['categoryId'] not in userCategories :
                        if i['categoryId'] not in userCategories:
                            print("Interst : ")
                            print("ENTERED !!!!")
                            print(interests[0]['interest'])
                            temp2['interestId'] = interests[0]['id']
                            temp2['interestName'] = interests[0]['interest']
                            temp2['categoryId'] = int(i['categoryId'])
                            temp2['categoryName'] = interests[0]['category']
                            userCategories.append(i['categoryId'])
                            print(f"Before get Post Category id : {int(i['categoryId'])}")
                            p = getPosts(loginUser.id, user.id, int(i['categoryId']))
                            temp2['posts'] = p

                            print(f"POST FOR  INTEREST :{interests[0]['id']} and CATEGORY : {int(i['categoryId'])}")
                            #print(p)
                            print("-----------------------------------------------------------------------------------------")

                            finalPostData.append(temp2)

                    except Exception as e : 
                        print("No Interest found ")
      
            return Response({"status": 200,"message": "Success", "data": finalPostData}) 

        else : 
            message = "This account is private"
            return Response({"status": 403,"message": message, "data": None})     


    except Exception as e: 
        print("Failed at getMyWorks: " ,e)
        message= "Failed while Fetching My Works"
        return Response({"status": 400,"message": message, "data": None}) 


@extend_schema(methods=['post'], request = likeRequest,
                    responses={200: likeResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])    
def userLike(request):
    try :
        finalPostData = []
        print("at liking and unliking a post")
        
        data = request.data
        user = User.objects.get(id = request.user.id)

        post_id = data['post_id']
        
        if post_id is None or post_id == '' or \
            not re.search(postIdPattern, post_id) or \
            len(post_id) != 24:
            raise Exception("invalid post_id format")

        likedCursor = db_handle.likes.find({"post_id": post_id, "userId": str(user.id)})
        d = 0
        
        for i in likedCursor : 
            if i['post_id'] == post_id:
                print("Removing")
                db_handle.likes.delete_one({"post_id": post_id, "userId": str(user.id)})
                d = 1
        
        if d == 0: 
            print("Added one ")
            newLike  = db_handle.likes.insert_one({"post_id": post_id,
                                        "userId": str(user.id), 
                                        "username" : user.username})

            # Notify the other user 
            postOwner = userPost.objects.get(post_id = str(post_id))
            if user.id != postOwner.user_id :
                print("Notify for Like ")
                msg = f"{user.username} has liked your post"
                notifications.objects.create(userId_id = postOwner.user_id,
                                            fromId_id = user.id,
                                            notification = msg,
                                            date=datetime.now())

        return Response({"status": 200,"message": "Success", "data": []}) 
        
    except Exception as e: 
        message= "Failed while Liking a Post"
    
        print(f"{message} : {e}")
        if e.args[0] != message :
            message = str(e.args[0])
       
        return Response({"status": 400,"message": message, "data": None}) 


@extend_schema(methods=['post'], request = followRequest,
                    responses={200: likeResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])    
def userFollow(request):
    try :
        finalPostData = []
        print("at follow and unfollowing a user")
        
        data = request.data
        user = User.objects.get(id = request.user.id) # 6 

        followingId = data['followingId'] # 3 
        
        followerCursor = db_handle.follow.find({"userId": str(user.id),"followingId": str(followingId)})
        d = 0
        
        for i in followerCursor : 
            if i['followingId'] == followingId:
                print("Unfollowed")
                db_handle.follow.delete_one({"userId": str(user.id),"followingId": str(followingId)})
                d = 1
        
        if d == 0: 
            followingUser = User.objects.get(id = int(followingId))

            if followingUser.isPrivate == 0 :
                print("Followed Public Profile ")
                db_handle.follow.insert_one({"userId": str(user.id),"followingId": str(followingId),"status":1})
            else : 
                db_handle.follow.insert_one({"userId": str(user.id),"followingId": str(followingId),"status":0})
        return Response({"status": 200,"message": "Success", "data": []}) 
        
    except Exception as e: 
        message= "Failed while Following / Unfollowing a User"
    
        print(f"{message} : {e}")
       
        return Response({"status": 400,"message": message, "data": None}) 

@extend_schema(methods=['post'],request = fetchFollowersRequest,
                responses={200: fetchFollowersResponse, 400 : ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fetchFollowers(request):
    try :
        print("at fetchFollowers")

        user = User.objects.get(id=request.user.id)
        data = request.data
        followersData = []
        found = False
        matchingUserIds = [] 

        viewerId = data['viewerId']        
        print(f"viewerID {viewerId}")

        if viewerId is None or \
            viewerId == '' or \
            not re.search(idPattern, viewerId) :
            raise Exception("invalid viewerId format")

        searchKeyword = data['keyword']

        if searchKeyword != None and searchKeyword != '':
            searchKeyword = searchKeyword.lower()

            # username
            print(f"search by username")
            userNameData = User.objects.filter(username__icontains=searchKeyword).values_list('id', 'username')
            d = list(map(lambda x: { "id": x[0],"match": match(searchKeyword.lower(), x[1].lower())}, userNameData))
            
            for i in range(len(d)):
                matchingUserIds.append(str(d[i]['id']))
                found = True
            
            # first_name
            firstNameData = User.objects.filter(first_name__icontains=searchKeyword).values_list('id','first_name')
            d = list(map(lambda x: { "id": x[0], "match": match(searchKeyword.lower(), x[1].lower())}, firstNameData))
            
            for i in range(len(d)):
                matchingUserIds.append(str(d[i]['id']))
                found = True        
        
            # last_name
            print(f"search by last_name")
            lastNameData = User.objects.filter(last_name__icontains=searchKeyword).values_list('id', 'last_name')
            d = list(map(lambda x: { "id": x[0],"match": match(searchKeyword.lower(), x[1].lower())}, lastNameData))
            
            for i in range(len(d)):
                matchingUserIds.append(str(d[i]['id']))
                found = True

        #print(f" Query 2 :{query2}")    
        #print(f"matchingUserIds : {matchingUserIds}")                

        if searchKeyword is None or searchKeyword == '' : 
            followersCursor = db_handle.follow.find({"followingId": str(viewerId)})
       
        else :
            followersCursor = db_handle.follow.find({
                                    "followingId": str(viewerId),
                                    "userId": {
                                        "$in" : matchingUserIds
                                    }
                                })

        followerCount = list(followersCursor.clone())
        
        for follower in followersCursor:
            try :
                temp  = {}
                temp['userId'] = follower['userId']
                userData = User.objects.get(id = int(follower['userId']))
                temp['username'] = userData.username
                temp['fullname']  = userData.first_name + " " +userData.last_name
                
                profileData = profile.objects.get(user_id = follower['userId'])
                temp['profileImage'] = profileData.profileImage.url
                temp['status'] = follower['status']
                followersData.append(temp)

            except Exception as e : 
                print("User not found while fetching following")

        #followersData.append({'followerCount' : len(followerCount)})
        
        return Response({"status": 200,"message": "Success", "data": followersData}) 
        
    except Exception as e: 
        print("Failed at fetchFollowers: " ,e)
        message= "Failed while fetchFollowers"

        if e.args[0] != message:
            message = str(e.args[0])

        return Response({"status": 400,"message": message, "data": None}) 

@extend_schema(methods=['post'], request = fetchFollowingRequest,
                responses={200: fetchFollowingResponse, 400 : ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fetchFollowing(request):
    try :
        print("at fetchFollowing")

        user = User.objects.get(id=request.user.id)
        data = request.data
        followingData = []
        
        found = False
        matchingUserIds = [] 

        viewerId = data['viewerId']
        print(f"viewerID {viewerId}")

        searchKeyword = data['keyword']

        if searchKeyword != None and searchKeyword != '':
            searchKeyword = searchKeyword.lower()

            # username
            print(f"search by username")
            userNameData = User.objects.filter(username__icontains=searchKeyword).values_list('id', 'username')
            d = list(map(lambda x: { "id": x[0],"match": match(searchKeyword.lower(), x[1].lower())}, userNameData))
            
            for i in range(len(d)):
                matchingUserIds.append(str(d[i]['id']))
                found = True
         
            # first_name
            firstNameData = User.objects.filter(first_name__icontains=searchKeyword).values_list('id','first_name')
            d = list(map(lambda x: { "id": x[0], "match": match(searchKeyword.lower(), x[1].lower())}, firstNameData))
            
            for i in range(len(d)):
                matchingUserIds.append(str(d[i]['id']))
                found = True        
        
            # last_name
            print(f"search by last_name")
            lastNameData = User.objects.filter(last_name__icontains=searchKeyword).values_list('id', 'last_name')
            d = list(map(lambda x: { "id": x[0],"match": match(searchKeyword.lower(), x[1].lower())}, lastNameData))
            
            for i in range(len(d)):
                matchingUserIds.append(str(d[i]['id']))
                found = True

        followingCursor = db_handle.follow.find({"userId": str(viewerId)})

        if searchKeyword is None or searchKeyword == '' : 
            followingCursor = db_handle.follow.find({"userId": str(viewerId)})
       
        else :
            followingCursor = db_handle.follow.find({
                                    "userId": str(viewerId),
                                    "followingId": {
                                        "$in" : matchingUserIds
                                    }
                                })
        followingCount = list(followingCursor.clone())
        
        for following in followingCursor:
           
            try : 
                temp  = {}
                temp['userId'] = following['followingId']
                userData = User.objects.get(id = int(following['followingId']))
                temp['fullname']  = userData.first_name + " " +userData.last_name
                temp['username'] = userData.username

                profileData = profile.objects.get(user_id = following['followingId'])
                temp['profileImage'] = profileData.profileImage.url
                temp['status'] = following['status']
                followingData.append(temp)
            except Exception as e : 
                print("User not found while fetching following")

        #followingData.append({'followerCount' : len(followingCount)})  
               
        return Response({"status": 200,"message": "Success", "data": followingData}) 
        
    except Exception as e: 
        print("Failed at fetchFollowers: " ,e)
        message= "Failed while fetchFollowers"
        return Response({"status": 400,"message": message, "data": None}) 

@extend_schema(methods=['post'], request = dashboardRequest,
                responses={200: dashboardResponse, 400 : ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):

    try :
        print("at dashboard")
        data = request.data
        viewerId = data['viewerId']
        
        print(f"viewerID {viewerId}")
        


        user = User.objects.get(id=int(viewerId))
        profileData = profile.objects.get(user_id = int(viewerId))
        finalData = []
        temp = {}

        temp['profileImage'] = profileData.profileImage.url
        temp['userId'] = user.id 
        temp['username'] = user.username
        temp['fullname'] = user.first_name + " " +user.last_name
        temp['bio'] = profileData.bio
 
        # Post
        userPostData = userPost.objects.filter(user=user).values_list("post_id", flat=True)
        posts = map(lambda x : collection_handle.find({"_id":ObjectId(x)}), userPostData)
        temp['posts'] = len(list(posts))
      
        # Followers
        t = {}
        t['viewerId'] = viewerId
        t['userId'] = user.id
        followers = fetchFollowersData(t)[0]['followerCount']
        temp['followers'] = followers
        print(f"Followers : {followers}")
      

        # Following
        following = fetchFollowingData(t)[0]['followingCount']
        
        temp['following'] = following
        print(f"Following : {following}")

        # isConnected
        
        isConnectedCursor = db_handle.follow.find({"userId" : str(request.user.id), "followingId" : str(viewerId)})
        d = 0
        isClone = len(list(isConnectedCursor.clone()))

        print(f"isClone : {isClone}")
        if isClone == 0 : 
            temp['isConnected'] = 2
            d = 1

        if isClone != 0: 
            for i in isConnectedCursor :
                temp['isConnected'] = i['status']
                d = 1

        if d == 0 : 
            temp['isConnected'] = 0
            

        
        finalData.append(temp)
               
        return Response({"status": 200,"message": "Success", "data": finalData}) 
        
    except Exception as e: 
        print("Failed at portfolio dashboard: " ,e)
        message= "Failed at  portfolio dashboard"
        return Response({"status": 400,"message": message, "data": None}) 


@extend_schema(methods=['get'],
                responses={200: dashboardResponse, 400 : ErrorResponsePortfolio})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def myDashboard(request):

    try :
        print("at my dashboard")
        
        user = User.objects.get(id = request.user.id)
        profileData = profile.objects.get(user_id = user.id )
        viewerId = user.id 
        
        finalData = []
        temp = {}

        temp['profileImage'] = profileData.profileImage.url
        temp['userId'] = user.id 
        temp['username'] = user.username
        temp['fullname']  = user.first_name + " " +user.last_name
 
        # Post
        userPostData = userPost.objects.filter(user=user).values_list("post_id", flat=True)
        posts = map(lambda x : collection_handle.find({"_id":ObjectId(x)}), userPostData)
        temp['posts'] = len(list(posts))
      
        # Followers
        t = {}
        t['viewerId'] = user.id
        t['userId'] = user.id
        followers = fetchFollowersData(t)[0]['followerCount']
        temp['followers'] = followers
        print(f"Followers : {followers}")
      

        # Following
        following = fetchFollowingData(t)[0]['followingCount']
        
        temp['following'] = following
        print(f"Following : {following}")

        # isConnected
        
        isConnectedCursor = db_handle.follow.find({"userId" : str(request.user.id), "followingId" : str(viewerId)})
        d = len(list(isConnectedCursor.clone()))
        if d >= 1 :
            temp['isConnected'] = 1
        else :
            temp['isConnected'] = 0

        finalData.append(temp)
               
        return Response({"status": 200,"message": "Success", "data": finalData}) 
        
    except Exception as e: 
        print("Failed at portfolio dashboard: " ,e)
        message= "Failed at  portfolio dashboard"
        return Response({"status": 400,"message": message, "data": None}) 


@extend_schema(methods=['post'], request = myFeedsRequest,
                    responses={200: myFeedsResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def myFeeds(request):
    try :
        print("at myFeeds generation ")
        user = User.objects.get(id = request.user.id)
        data = request.data
        page_size = data['page_size']
        page = data['page']

        finalPostData = []

        '''if data['viewerId'] is None or data['viewerId'] == "" or \
            not re.search(idPattern, data['viewerId']) : 
            raise Exception("invalid ViewerId Format")'''
        
        t = {}
        t['userId'] = request.user.id
        t['viewerId'] = request.user.id
        t['status']="myFeeds"
        following = fetchFollowingDetails(t)
        
        if data['page'] is None or data['page'] == '' or \
            not re.search(idPattern, str(data['page'])):
            raise Exception("page invalid format")
       
        if data['page_size'] is None or data['page_size'] == '' or \
            not re.search(idPattern, str(data['page_size'])):
            raise Exception("page_size invalid format")

        for i in range(len(following)):
            
            print(f"Fetching Posts of {following[i]['username']}")
            followingId = int(following[i]['userId'])
            user = User.objects.get(id=followingId)
            
            userPostData = userPost.objects.filter(user_id=followingId )\
                            .values_list("post_id", flat=True) \
                            .order_by('-id')

            profileData = profile.objects.get(user_id = followingId)
       
            posts = map(lambda x : collection_handle.find({"_id":ObjectId(x)}), userPostData)
           

            for post in posts :
                for i in post :
                    try : 
                        temp = {}
                        temp['_id'] = str(i['_id'])
                        print(temp['_id'])

                        temp['createdById'] = user.id
                        temp['createdByUsername'] = user.username
                        temp['profileImage'] = profileData.profileImage.url
                        temp['loginUser'] = user.id

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
                        print("Some myFeeds Posts had key value issues")

            print("**********************************************")
            #random.shuffle(finalPostData)
        
        dataToSend = []

        try : 
            p = Paginator(finalPostData, page_size)
            dataToSend = p.page(page).object_list

            tempIsNext = {
                "totalPost":len(finalPostData),
                "page_size" : page_size,
                "page" : page
                }
            nextPage = isNextPage(tempIsNext)

        except Exception as e : 
            print(e)
            dataToSend = p.page(1).object_list
            
            tempIsNext = {
                "totalPost":len(finalPostData),
                "page_size" : 1,
                "page" : 1
                }

            nextPage = isNextPage(tempIsNext)

        return Response({"status": 200,"message":"Success",
                        "data": {"totalPost":len(finalPostData),
                                "isNextPageAvailable": nextPage,
                                "finalData":dataToSend}})

    except Exception as e: 
        message = "Failed while fetching myFeeds "
        if e.args[0] != None or e.args[0] != message: 
            message = e.args[0]
        
        print("Failed while fetching myFeeds : ",e)
        return Response({"status": 400,"message":message, "data": None})

@extend_schema(methods=['post'], request = myBookmarksRequest,
                    responses={200: myBookmarksResponse, 400: ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userBookmark(request):
    try :
        print("at userBookmark ")

        user = User.objects.get(id = request.user.id)
        data = request.data
        post_id = data['post_id']

        if post_id is None or post_id == '' or \
            not re.search(postIdPattern, post_id) or \
            len(post_id) != 24:
            raise Exception("invalid post_id format")
       
        exisitingCursor = db_handle.bookmarks.find({
            'userId' : user.id,
            'post_id' : data['post_id'] 
        })

        l = len(list(exisitingCursor))
      
        if l == 0:
            newBookmark = db_handle.bookmarks.insert_one({
                'userId' : user.id,
                'post_id' : data['post_id']
            })

        else:
            print("Removing Bookmark")
            db_handle.bookmarks.delete_one({
                'userId' : user.id,
                'post_id' : data['post_id']
            })

        return Response({"status": 200,"message":"Success","data":[]})

    except Exception as e: 
        message = "Failed while userBookmark "
        if e.args[0] != None : 
            message = e.args[0]
        
        print("Failed while userBookmark : ",e)
        return Response({"status": 400,"message":message, "data": None})

@extend_schema(methods=['get'],
                responses={200: fetchBookmarkResponse, 400 : ErrorResponsePortfolio})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchBookmarks(request):
    try :
        print("at fetchBookmarks ")
        loginUser = User.objects.get(id = request.user.id)
        finalBookmarkData = []
        
        #'post_id' : data['post_id'] 
        exisitingCursor = db_handle.bookmarks.find({
            'userId' : loginUser.id,
        }).sort('_id', -1)

        for j in exisitingCursor:
            print(j['post_id'])
            postOwner = userPost.objects.get(post_id = str(j['post_id']))
            user = User.objects.get(id = postOwner.user_id)
            profileData = profile.objects.get(user_id = user.id)
            
            filter = { "_id": ObjectId(j['post_id']) }
            postData = db_handle.posts.find(filter)
            
            for i in postData:
                temp = {}
                temp['type'] = 1
                temp['_id'] = str(i['_id'])
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
                                                        'userId': loginUser.id}))
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

                finalBookmarkData.append(temp)
    
        return Response({"status": 200,"message":"Success","data":finalBookmarkData})

    except Exception as e: 
        message = "Failed while fetchBookmarks "
        if e.args[0] != None : 
            message = e.args[0]
        
        print("Failed while fetchBookmarks : ",e)
        return Response({"status": 400,"message":message, "data": None})

@extend_schema(methods=['post'], request = updateFollowRequest,
                responses={200: updateFollowResponse, 400 : ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateFollowRequestStatus(request):
    try :
        print("at acceptFollowRequest")

        user = User.objects.get(id=request.user.id)
        data = request.data

        if data['userId'] is None or data['userId'] == "" or \
            not re.search(idPattern, data['userId']):
            raise Exception("invalid UserId Format")

        if data['status'] is None or data['status'] == "" or \
            not re.search(idPattern, data['status']):
            raise Exception("invalid status format")

        status = int(data['status'])
        if status == 1 : # Accept
            filter = {  "userId" : str(data['userId']), "followingId" : str(request.user.id) }
            updateStatus = { "$set" : { 'status' : status } }
            updateCursor = db_handle.follow.update_one(filter, updateStatus)
        
        elif status == 2 : # Delete 
            filter = {  "userId" : str(data['userId']), "followingId" : str(request.user.id) }
            deleteCurosr = db_handle.follow.delete_one(filter)
        else : 
            raise Exception("Unknown status type")

        return Response({"status": 200,"message": "Success", "data": []}) 
        
    except Exception as e: 
        print("Failed at acceptFollowRequest: " ,e)
        message= "Failed while acceptFollowRequest"
        if e.args[0] == 'Unknown status type' or e.args[0] != message:
            message = str(e.args[0])
        return Response({"status": 400,"message": message, "data": None}) 

@extend_schema(methods=['get'],responses={200: fetchReportResponse, 
                                400 : ErrorResponsePortfolio})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchReport(request):
    try :
        print("at fetchReport")

        reportData = list(report.objects.all().values())
        return Response({"status": 200,"message": "Success", "data": reportData}) 
    except Exception as e: 
        print("Failed at fetchReport: " ,e)
        message= "Failed while fetchReport"
        return Response({"status": 400,"message": message, "data": None}) 

@extend_schema(methods=['post'], request = reportRequest,
                responses={200: reportResponse, 400 : ErrorResponsePortfolio})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userReport(request):
    try :
        print("at userReport")

        loginUser = User.objects.get(id=request.user.id)
        data = request.data
        reportId = int(data['reportId'])

        newReport = reportPost.objects.create(post_id = data['post_id'],
                                               reason_id = reportId,
                                               user = loginUser )

        return Response({"status": 200,"message": "Success", "data": []}) 
        
    except Exception as e: 
        print("Failed at report: " ,e)
        message= "Failed while reporting"
        return Response({"status": 400,"message": message, "data": None}) 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulkDelete(request):
    try :
        print("at bulkDelete")

        deletePostsBulk()

        return Response({"status": 200,"message": "Success", "data": []}) 
        
    except Exception as e: 
        print("Failed at bulkDelete: " ,e)
        message= "Failed while bulkDelete"
        return Response({"status": 400,"message": message, "data": None}) 