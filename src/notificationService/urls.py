
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from notificationService.views import *

urlpatterns = [
    path('followRequestNotifications', followRequestNotifications, name = 'followRequestNotifications'),
    path('fetchActivity', fetchActivity, name= 'fetchActivity')
]
