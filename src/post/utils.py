import gc

from authentication.models import User, profile
from authentication.utils import getInteractionDetails
from bson import ObjectId
from core.settings.base import (mongo_host, mongo_port, mongo_proddbname,
                                mongo_srv, mongodb_databaseName, password,
                                username)
from django.db import connection
from pymongo import MongoClient
from zipchoAdmin.models import category

from .models import *

'''def get_db_handle(db_name, host, port, username, password):
    client = MongoClient(host=host,
                         port=port,
                         username=username,
                         password=password)

    db_handle = client[db_name]
    return db_handle, client 
'''

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


def getLikesDetails(data, db_handle):
    try :
        print("getLikesDetails ------------")
        finalData = []
        temp = {}
        data['type'] = 1
        isLiked = 0
        #print("at get Like Details")
        #print(data)
        if data['type'] == 1 :

            before = len(gc.get_objects())
         
            #print("Fetching Likes of POST")
            #{'_id': ObjectId('62e3638c8bbfff59d4f4eb75'), 'post_id': '62e2174d174e0e3d6dff3dd9',
            #  'userId': '3', 'username': 'angadiumakant'}
            
            likedByIds = list(db_handle.likes.find({'post_id': data['_id']}))
            
            #print(type(likedByIds))
            #print(likedByIds.__dict__)
            for like in likedByIds:
                temp = {}
                if like['userId']  == str(data['loginUser']) : 
                    isLiked = 1
                
                temp['userId']= like['userId']
                temp['username']= like['username']

            
            finalData.append(temp)            
        return finalData, len(likedByIds), isLiked
 
    except Exception as e : 
        print("Failed while fetching Likes Details ",e)

def dictFetchAll(cursor):
    columns = [col[0] for col in cursor.description]
    
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getUserInterests(userId, catId):
    try :
        print("at  getUserInterests ")
        
        with connection.cursor() as cursor : 
            interestQuery = f"SELECT \
                                i.id,\
                                i.interest,\
                                zc.category, \
                                IF(ui.interest_id IS NULL, 0, 1) AS isSelected\
                            FROM\
                                zipchoAdmin_interest i\
                                    LEFT JOIN\
                                authentication_userinterest ui ON i.id = ui.interest_id\
                                    JOIN\
                                zipchoAdmin_category zc ON zc.interest_id = ui.interest_id\
                            WHERE\
                                ui.user_id = %s AND zc.id = %s; "

            cursor.execute(interestQuery, [userId,catId])
            interestData = dictFetchAll(cursor)
            data = interestData

        return data

    except Exception as e: 
        print(e)
        return 0

def getPosts(loginUserId, userId, catId):
    try :
        print("At get Posts")
        POST_COLLECTIONS = 'posts'
        db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)
        collection_handle = get_collection_handle(db_handle, POST_COLLECTIONS)

      
        user = User.objects.get(id=userId)
        profileData = profile.objects.get(user_id = user.id)
        
        userPostData = userPost.objects.filter(user=user).values_list("post_id", flat=True)
        print(f"At mongo catid :{catId}")
        posts = map(lambda x : collection_handle.find({"_id":ObjectId(x), 'categoryId':str(catId)}), userPostData)
        
        nn = posts
        print(nn)
        
        finalPostData = []

        
        for post in posts :
            myInterest=""
           
            print(f"POST : {post}")
            for i in post :
                if catId == int(i['categoryId']) :
                    print(f"CAT ID :{catId}")

                    try :      
                        temp = {}
                        temp['type'] = 1
                        temp['_id'] = str(i['_id'])
                        print(f"HERE ----------------------------------------------- {str(i['_id'])}")
                        temp['createdById'] = user.id
                        temp['createdByUsername'] = user.username
                        temp['profileImage'] = profileData.profileImage.url
                        temp['loginUser'] = loginUserId

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
                                                                'userId': loginUserId}))
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
       
        #print(f"FINAL POST DATA : {finalPostData}")
        '''print(f"FINAL POST DATA for {catId}")
        print(len(finalPostData))
        print(finalPostData)'''
        return finalPostData

    except Exception as e: 
        print(e)
        return 0

def fetchFollowersData(data):
    try :
        print("at fetchFollowers")
        db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)

        user = User.objects.get(id=data['userId'])
        
        followersData = []

        viewerId = data['viewerId']
        print(f"viewerID {viewerId}")

        followersCursor = db_handle.follow.find({"followingId": str(viewerId)})
        followerCount = list(followersCursor.clone())
        
        '''for follower in followersCursor:
            try :
                temp  = {}
                temp['userId'] = follower['userId']
                temp['username'] = User.objects.filter(id = int(follower['userId'])).values_list('username',flat=True)[0]
                followersData.append(temp)

            except Exception as e : 
                print("User not found while fetching following")
        '''
        
        followersData.append({'followerCount' : len(followerCount)})
        
        return followersData
        
    except Exception as e: 
        print("Failed at fetchFollowers: " ,e)
        message= "Failed while fetchFollowers"
        return 0


def fetchFollowingDetails(data):
    try :
        print("at fetchFollowingDetails")
        db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)


        user = User.objects.get(id=data['userId'])
        followingData = []

        viewerId = data['viewerId']
        print(f"viewerID {viewerId}")

        followingCursor = db_handle.follow.find({"userId": str(viewerId)})
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
                followingData.append(temp)
            except Exception as e : 
                print("User not found while fetching following")

        #followingData.append({'followingCount' : len(followingCount)})  
               
        return followingData
        
    except Exception as e: 
        print("Failed at fetchFollowingDetails: " ,e)
        message = "Failed while fetchFollowingDetails"
        return 0

def fetchFollowingData(data):
    try :
        print("at fetchFollowing")
        db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)


        user = User.objects.get(id=data['userId'])
        followingData = []

        viewerId = data['viewerId']
        print(f"viewerID {viewerId}")

        followingCursor = db_handle.follow.find({"userId": str(viewerId)})
        followingCount = list(followingCursor.clone())
        
        '''for following in followingCursor:
           
            try : 
                temp  = {}
                temp['userId'] = following['followingId']
                temp['username'] = User.objects.filter(id = int(following['followingId'])).values_list('username',flat=True)[0]
                followingData.append(temp)
            except Exception as e : 
                print("User not found while fetching following")
        '''
        followingData.append({'followingCount' : len(followingCount)})  
               
        return followingData
        
    except Exception as e: 
        print("Failed at fetchFollowers: " ,e)
        message = "Failed while fetchFollowers"
        return 0

def fetchFollowingDetails(data):
    try :
        print("at fetchFollowingDetails")
        db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)
        #rint("heree")
        #print(data)
        user = User.objects.get(id=data['userId'])

        temp2 = {}

        followersData = []

        #viewerId = data['viewerId']
        #print(f"viewerID {viewerId}")
        if data['status'] == 'myFeeds' : 
            #print(f"str(user.id) : {str(user.id)}")
            followersCursor = db_handle.follow.find({"userId": str(user.id),"status":1})
            
            # Adding own user id to show own posts in feeds
            temp2['userId'] = user.id
            temp2['username'] = user.username
            temp2['fullname']  = user.first_name + " " +user.last_name
                
            profileData = profile.objects.get(user_id = user.id)
            temp2['profileImage'] = profileData.profileImage.url
            temp2['status'] = 0
            followersData.append(temp2)

        else :
            followersCursor = db_handle.follow.find({"followingId": str(user.id),
                                                "status": int(data['status'])})
                                                
        followerCount = list(followersCursor.clone())
        
        for follower in followersCursor:
            try :
                temp  = {}
                #print("here")
                #print(follower['userId'])
                
                if data['status'] == 'myFeeds':
                    temp['userId'] = follower['followingId']
                else :
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
        
        return followersData
        
    except Exception as e: 
        print("Failed at fetchFollowingDetails: " ,e)
        message = "Failed while fetchFollowingDetails"
        return 0


def fetchCommentsDetails(data):
    try :
        finalPostData = []
        print("at fetch Comments Details")
        
        postId = data['_id'] # post_id
        print(f"POST ID :{postId}")

        #user = User.objects.get(id=data['userId'])
        #userPostData = userPost.objects.filter(user=user).values_list("post_id", flat=True)
        
        #print(f"userPostData : {userPostData}")
        
        comments = db_handle.comments.find({"post_id":postId})
        
        l = len(list(comments.clone()))
        #print(f"details of comments  : {l}")

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
        return finalPostData
        
    except Exception as e: 
        print("Failed at fetchCommentsDetails: " ,e)
        message= "Failed while fetchCommentsDetails"
        return 0

def getHastags():
    
    finalData = []
    tempHash = []
    c=0

    hashtags = list(map(lambda x : x['hashtags'].replace(' ',''),
                     db_handle.posts.find({"hashtags":{'$ne':None}},
                                        {"_id":0, "hashtags": 1})
                        )
                    )
  
    for i in range(len(hashtags)):
      
        if hashtags[i] is not None :
            data = hashtags[i].split("#")
            for j in range(len(data)):
                temp = {}
                if data[j] not in tempHash and data[j] != '' and data[j] != 'string' :
                    temp['id'] = c 
                    temp['hashtag'] = data[j]
                    finalData.append(temp)
                    tempHash.append(data[j])
                    c=c+1 
    return finalData

def getBasicDetails(data):
    try:
        print("getBasicDetails")
        basicData = [] 
        #[{'userId': '3'}, {'userId': '69'}]

        try :
            for i in range(len(data)):
                userData = User.objects.get(id=int(data[i]['userId']))

                temp  = {}
                temp['userId'] = str(userData.id)
                temp['username'] = userData.username
                temp['fullname']  = userData.first_name + " " +userData.last_name
                
                profileData = profile.objects.get(user_id = userData.id)
                temp['profileImage'] = profileData.profileImage.url

                basicData.append(temp)

        except Exception as e: 
            print("Something went wrong while fetching basic detail: ",e)

        return basicData

    except Exception as e:
        print("Failed at getBasicDetails: ",e )
        return 0



def deletePostsBulk():
    try :
        print("At Delete Posts Bulk")
        POST_COLLECTIONS = 'posts'
        db_handle, mongo_client = get_db_handle(mongo_proddbname,mongo_srv)
        collection_handle = get_collection_handle(db_handle, POST_COLLECTIONS)
        userIds = [111,6,3,11]
        
        up = userPost.objects.filter(user_id__in = userIds).values()
        print(len(up))
        
        acceptedPosts = []

        for i in range(len(up)):
            post_id = up[i]['post_id']
            user = up[i]['user_id']
            acceptedPosts.append(post_id)
        
        print(len(acceptedPosts))

        postsCursor = db_handle.posts.find()

        for i in postsCursor:
            if str(i['_id']) not in acceptedPosts:
                post_id = i['_id']
                print(f"Deleting Post : {post_id} of user : {user}")
                db_handle.posts.delete_one({"_id":ObjectId(str(post_id))})
                db_handle.comments.delete_many({"post_id":str(post_id)})
                db_handle.likes.delete_many({"post_id":str(post_id)})
                db_handle.bookmarks.delete_many({"post_id":str(post_id)})
                try :
                    toDelete = userPost.objects.get(post_id = post_id)
                    toDelete.delete()   
                except Exception as e :
                     print("userPost Metadata not found")
        

        print("Deleting Post, Comments, Likes, Bookmarks ")

        ''' for i in range(len(up)):
            post_id = up[i]['post_id']
            user = up[i]['user_id']
            print(f"Deleting Post : {post_id} of user : {user}")
            db_handle.posts.delete_one({"_id":ObjectId(str(post_id))})
            db_handle.comments.delete_many({"post_id":str(post_id)})
            db_handle.likes.delete_many({"post_id":str(post_id)})
            db_handle.bookmarks.delete_many({"post_id":str(post_id)})
            toDelete = userPost.objects.get(post_id = post_id)
            toDelete.delete()'''


    except Exception as e: 
        print(e)
        return 0


def isNextPage(data):
    try :
        isNext = int(data['totalPost']) / int(int(data['page_size']) * int(data['page']))
        print("at isNextPage ")
        print(isNext)
        
        if int(data['page_size']) == int(data['totalPost']):
            return 0

        if isNext >= 1:
            return 1
        
        return 0
    except Exception as e : 
        print("Failed at isNextPage : ", e)