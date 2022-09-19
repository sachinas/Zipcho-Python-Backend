from rest_framework import serializers

class userData(serializers.Serializer):
    userId = serializers.CharField(max_length=50)
    username=serializers.CharField(max_length=100)
    fullname=serializers.CharField(max_length=100)

class usersData(serializers.Serializer):
    userId = serializers.CharField(max_length=50)
    username=serializers.CharField(max_length=100)

class followData(serializers.Serializer):
    userId = serializers.CharField(max_length=50)
    username=serializers.CharField(max_length=100)
    fullname=serializers.CharField(max_length=100)
    profileImage=serializers.CharField(max_length=300)
    status = serializers.IntegerField()

class fetchCommentsRequest(serializers.Serializer):
    postId = serializers.CharField(max_length=200)

class repliesData(serializers.Serializer):
    comment = serializers.CharField(max_length=150)
    likes = serializers.IntegerField()
    date = serializers.DateTimeField()
    userId =  serializers.IntegerField()
    userName = serializers.CharField(max_length=200)
    profileImage=serializers.CharField(max_length=300)

class fetchCommentData(serializers.Serializer):
    comment = serializers.CharField(max_length=150)
    likes = serializers.IntegerField()
    date = serializers.DateTimeField()
    post_id = serializers.CharField(max_length=200)
    comment_id= serializers.CharField(max_length=200)
    userId = serializers.IntegerField()
    username = serializers.CharField(max_length=200)
    profileImage=serializers.CharField(max_length=300)
    replies = serializers.ListField(child = repliesData())

class getAllUserData(serializers.Serializer):
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
    categoryId  = serializers.CharField(max_length=200)
    categoryName = serializers.CharField(max_length=200)
    mediaType = serializers.CharField(max_length=30)
    aspectRatio = serializers.CharField(max_length=30)
    canComment = serializers.IntegerField()
    canSharePost = serializers.IntegerField()

class postData(serializers.Serializer):
    _id = serializers.CharField(max_length=50)
    type = serializers.IntegerField()
    createdById=serializers.IntegerField()
    createdByUsername=serializers.CharField(max_length=50)
    profileImage= serializers.CharField(max_length=300)
    loginUser = serializers.IntegerField()
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
     
class getAllMyWorksData(serializers.Serializer):
    interestId = serializers.IntegerField()
    interestName = serializers.CharField(max_length=50)
    categoryId = serializers.IntegerField()
    categoryName = serializers.CharField(max_length=50)
    posts = serializers.ListField(child = postData())

class getAllUserPostResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = getAllUserData()

class getAllMyWorksResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = getAllMyWorksData()
    
class ErrorResponsePortfolio(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True)   

class userPostRequest(serializers.Serializer):
    caption = serializers.CharField(max_length=300)
    visibility = serializers.CharField(max_length=30)
    taggedUser = serializers.ListField(child = userData())
    hashtags =  serializers.CharField(max_length=300)
    mediaUrl = serializers.CharField(max_length=300)
    key =  serializers.CharField(max_length=300)
    latitude = serializers.CharField(max_length=100)
    longitude = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200)
    #likes = serializers.IntegerField()
    categoryId = serializers.CharField(max_length=50)
    mediaType = serializers.CharField(max_length=50)
    aspectRatio = serializers.CharField(max_length=50)
    '''
    {
    "caption": "MJ Video Choreo",
    "visibility": "1",
    "taggedUser": [
      {
        "userId": "1"
      }
    ,{
        "userId": "2"
     }
    ],
    "hastags": "#michael #mj",
    "mediaUrl":null,
    "key":null,
    "latitude":"11.004556",
    "longitude":"76.961632",
    "likes":null
    }
    '''

class userPostResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True)   

class fetchCommentsResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.ListField(child = fetchCommentData())

class commentsRequest(serializers.Serializer):
    post_id = serializers.CharField(max_length=200)
    comment_id = serializers.CharField(max_length=200)
    type = serializers.IntegerField()
    comment = serializers.CharField(max_length=300)

class likeRequest(serializers.Serializer):
    post_id = serializers.CharField(max_length=200)

class commentData(serializers.Serializer):
    comment = serializers.CharField(max_length=150)
    likes = serializers.IntegerField()
    date = serializers.DateTimeField()
    post_id = serializers.CharField(max_length=200)
    comment_id= serializers.CharField(max_length=200)
    userId = serializers.IntegerField()
    username = serializers.CharField(max_length=200)

class commentsResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.ListField(child=commentData()) 

class likeResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True)   

class followRequest(serializers.Serializer):
    followingId = serializers.CharField(max_length=200)

class followResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True)   

class fetchFollowersRequest(serializers.Serializer):
    viewerId = serializers.CharField(max_length=200)
    keyword=serializers.CharField(max_length=200)

class fetchFollowersResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.ListField(child = followData())   

class getMyWorksRequest(serializers.Serializer):
    viewerId = serializers.CharField(max_length=200)

class getAllUserPostsRequest(serializers.Serializer):
    viewerId = serializers.CharField(max_length=200)

class fetchFollowingRequest(serializers.Serializer):
    viewerId = serializers.CharField(max_length=200)
    keyword=serializers.CharField(max_length=200)

class fetchFollowingResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.ListField(child = followData())   

class dashboardData(serializers.Serializer):
    profileImage=serializers.CharField(max_length=300)
    userId=serializers.IntegerField()
    username=serializers.CharField(max_length=100)
    fullname=serializers.CharField(max_length=100)
    bio=serializers.CharField(max_length=300)
    posts=serializers.IntegerField()
    followers=serializers.IntegerField()
    following=serializers.IntegerField()
    isConnected=serializers.IntegerField()
    isPrivate=serializers.IntegerField() 

class dashboardRequest(serializers.Serializer):
    viewerId = serializers.CharField(max_length=200)

class dashboardResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.ListField(child = dashboardData())   

class myFeedsRequest(serializers.Serializer):
    #viewerId = serializers.CharField(max_length=200)
    page_size = serializers.IntegerField()
    page = serializers.IntegerField()

class getMyFeedsData(serializers.Serializer):
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

class feedsWithPagination(serializers.Serializer):
    totalPost = serializers.IntegerField()
    isNextPageAvailable = serializers.IntegerField()
    finalData = serializers.ListField(child = getMyFeedsData())

class myFeedsResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = feedsWithPagination()

class myBookmarksRequest(serializers.Serializer):
   post_id = serializers.CharField(max_length=200)

class myBookmarksResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True) 

class fetchBookmarkData(serializers.Serializer):
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
    categoryId  = serializers.CharField(max_length=200)
    categoryName = serializers.CharField(max_length=200)
    mediaType = serializers.CharField(max_length=30)
    aspectRatio = serializers.CharField(max_length=30)
    canComment = serializers.IntegerField()

class fetchBookmarkResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.ListField(child = fetchBookmarkData() )

class updateFollowRequest(serializers.Serializer):
   userId = serializers.CharField(max_length=20)    
   status = serializers.CharField(max_length=20)

class updateFollowResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True) 

class deletePostRequest(serializers.Serializer):
    post_id = serializers.CharField(max_length=200)

class deletePostResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True) 

class updatePostRequest(serializers.Serializer):
    post_id = serializers.CharField(max_length=200)
    caption = serializers.CharField(max_length=300)
    visibility = serializers.CharField(max_length=30)
    taggedUser = serializers.ListField(child = userData())
    hashtags =  serializers.CharField(max_length=300)
    latitude = serializers.CharField(max_length=100)
    longitude = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200)
    categoryId = serializers.CharField(max_length=50)

class updatePostResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True) 

class reportRequest(serializers.Serializer):
    reportId = serializers.IntegerField()
    post_id = serializers.CharField(max_length=100)

class reportResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True) 

class fetchReportData(serializers.Serializer):
    id=serializers.IntegerField()
    reason=serializers.CharField(max_length=200)
   
class fetchReportResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.ListField( child = fetchReportData() )