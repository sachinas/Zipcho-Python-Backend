from django.urls import include, path
from .views import *
urlpatterns = [
    #path("myDashboard", myDashboard, name = 'myDashboard'),
    path("dashboard", dashboard, name= 'dashboard'),

    path("getAllUserPosts", getAllUserPosts, name= 'getAllUserPosts'),
    path("userPosts", userPosts, name= 'userPosts'),
    path("updatePost", updatePost, name="updatePost"),
    path("deletePost/<str:post_id>", deletePost, name="deletePost"),

    path("fetchComments", fetchComments, name="fetchComments"),
    path("comment", comment, name="comment"),

    path("getMyWorks", getMyWorks , name = "getMyWorks"),

    #likes 
    path("userLike", userLike, name="userLike"),

    #follow
    path("userFollow", userFollow, name="userFollow"),
    path("fetchFollowers", fetchFollowers, name="fetchFollowers"),
    path("fetchFollowing", fetchFollowing, name="fetchFollowing"),
    path('updateFollowRequestStatus', updateFollowRequestStatus, name= 'updateFollowRequestStatus'),

    #feeds
    path("myFeeds",myFeeds, name="myFeeds"),

    #share 
    #path("share", share, name="share"),

    #Bookmark "
    path("userBookmark", userBookmark, name="userBookmark"),
    path("fetchBookmarks", fetchBookmarks, name="fetchBookmarks"),
    
    # Report 
    path('fetchReport', fetchReport, name= "fetchReport"),
    path("userReport", userReport , name= "userReport"),

    #path('bulkDelete', bulkDelete, name='bul delete')
]