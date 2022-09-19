from rest_framework import serializers
from post.postResponse import usersData,fetchCommentData,userData


class searchPhotoRequest(serializers.Serializer):
    keyword=serializers.CharField(max_length=200)

class searchVideoRequest(serializers.Serializer):
    keyword=serializers.CharField(max_length=200)    

class searchPeopleRequest(serializers.Serializer):
    keyword=serializers.CharField(max_length=200)
    
class searchAllRequest(serializers.Serializer):
    keyword=serializers.CharField(max_length=200)

class getSearchPhotoData(serializers.Serializer):
    _id = serializers.CharField(max_length=50)
    createdById=serializers.IntegerField()
    createdByUsername=serializers.CharField(max_length=50)
    profileImage= serializers.CharField(max_length=300)
    loginUser = serializers.IntegerField()
    type = serializers.IntegerField()
    likedBy = serializers.ListField(child=usersData())
    likes = serializers.IntegerField()
    isLiked = serializers.IntegerField()
    comments = serializers.ListField(child = fetchCommentData())
    totalComments = serializers.IntegerField()
    caption = serializers.CharField(max_length=300)
    visibility = serializers.CharField(max_length=30)
    taggedUser = serializers.ListField(child=userData())
    hashtags =  serializers.CharField(max_length=300)
    mediaUrl = serializers.CharField(max_length=500)
    key =  serializers.CharField(max_length=500)
    latitude = serializers.CharField(max_length=100)
    longitude = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200)
    date = serializers.DateTimeField()
    isBoomarked = serializers.IntegerField() 
    categoryId = serializers.CharField(max_length=30)
    categoryName = serializers.CharField(max_length=200)
    mediaType = serializers.CharField(max_length=30)
    aspectRatio = serializers.CharField(max_length=30)
    canComment = serializers.IntegerField()
    canSharePost = serializers.IntegerField() 

class getSearchVideoData(serializers.Serializer):
    _id = serializers.CharField(max_length=50)
    createdById=serializers.IntegerField()
    createdByUsername=serializers.CharField(max_length=50)
    profileImage= serializers.CharField(max_length=300)
    loginUser = serializers.IntegerField()
    type = serializers.IntegerField()
    likedBy = serializers.ListField(child=usersData())
    likes = serializers.IntegerField()
    isLiked = serializers.IntegerField()
    comments = serializers.ListField(child = fetchCommentData())
    totalComments = serializers.IntegerField()
    caption = serializers.CharField(max_length=300)
    visibility = serializers.CharField(max_length=30)
    taggedUser = serializers.ListField(child=userData())
    hashtags =  serializers.CharField(max_length=300)
    mediaUrl = serializers.CharField(max_length=500)
    key =  serializers.CharField(max_length=500)
    latitude = serializers.CharField(max_length=100)
    longitude = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200)
    date = serializers.DateTimeField()
    isBoomarked = serializers.IntegerField() 
    categoryId = serializers.CharField(max_length=30)
    categoryName = serializers.CharField(max_length=200)
    mediaType = serializers.CharField(max_length=30)
    aspectRatio = serializers.CharField(max_length=30)
    canComment = serializers.IntegerField()
    canSharePost = serializers.IntegerField() 

class getSearchAllData(serializers.Serializer):
    _id = serializers.CharField(max_length=50)
    createdById=serializers.IntegerField()
    createdByUsername=serializers.CharField(max_length=50)
    profileImage= serializers.CharField(max_length=300)
    loginUser = serializers.IntegerField()
    type = serializers.IntegerField()
    likedBy = serializers.ListField(child=usersData())
    likes = serializers.IntegerField()
    isLiked = serializers.IntegerField()
    comments = serializers.ListField(child = fetchCommentData())
    totalComments = serializers.IntegerField()
    caption = serializers.CharField(max_length=300)
    visibility = serializers.CharField(max_length=30)
    taggedUser = serializers.ListField(child=userData())
    hashtags =  serializers.CharField(max_length=300)
    mediaUrl = serializers.CharField(max_length=500)
    key =  serializers.CharField(max_length=500)
    latitude = serializers.CharField(max_length=100)
    longitude = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200)
    date = serializers.DateTimeField()
    isBoomarked = serializers.IntegerField() 
    categoryId = serializers.CharField(max_length=30)
    categoryName = serializers.CharField(max_length=200)
    mediaType = serializers.CharField(max_length=30)
    aspectRatio = serializers.CharField(max_length=30)
    canComment = serializers.IntegerField()
    canSharePost = serializers.IntegerField()
     

class searchPhotoResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.ListField(child = getSearchPhotoData())

class searchVideoResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.ListField(child = getSearchVideoData())

class searchAllResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.ListField(child = getSearchAllData())

class getSearchPeopleData(serializers.Serializer):
    id = serializers.CharField(max_length=50)
    username=serializers.CharField(max_length=100)
    fullname=serializers.CharField(max_length=100)
    profileImage= serializers.CharField(max_length=300)
    isConnected=serializers.IntegerField()
    canTag = serializers.IntegerField()
    canMessage = serializers.IntegerField()
    isPrivate = serializers.IntegerField()

class searchPeopleResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = getSearchPeopleData()

class searchHashtagRequest(serializers.Serializer):
    keyword=serializers.CharField(max_length=200)

class getHashtagData(serializers.Serializer):
    id = serializers.CharField(max_length=50)
    hashtag=serializers.CharField(max_length=100)

class searchHashtagResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = getHashtagData()