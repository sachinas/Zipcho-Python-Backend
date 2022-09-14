from django.urls import include, path
from .views import *

urlpatterns = [
   path('people', people, name='people'),
   path('allSearch', allSearch, name='allSearch'),
   path('photo', photo, name='photo'),
   path('video', video, name='video'),
   path('hashtags', hashtagsDetails, name='hashtags')
]