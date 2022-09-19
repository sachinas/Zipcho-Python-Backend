from django.urls import path, include
from .views import * 

urlpatterns = [
    path('fetchContestType', fetchContestType, name='fetch-Contest-Type'),
    path('createContest', createContest, name='createContest')
] 