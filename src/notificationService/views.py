import asyncio
from datetime import datetime

from authentication.models import User
from django.core.paginator import Paginator
from django.db import connection
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from post.utils import fetchFollowingDetails, getBasicDetails
from push_notifications.models import GCMDevice
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import *
from .notificationResponse import *

@extend_schema(methods=['post'],request = followRequestNotificationsRequest,
            responses={200: followRequestNotificationsResponse,
            400 : ErrorResponseNotification})
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def followRequestNotifications(request):
    print("Inside followRequestNotifications")
    try:
        user = User.objects.get(id = request.user.id)
        #notifDB = notifications.objects.filter(userId_id = user.id).values()

        dataToSend = []
        finalData = []
        #totalRecords=len(notifDB)
        page_size = 1 
        page = 1

        data = request.data
        
        temp = {}
        temp['userId'] = user.id
        temp['status'] = 0

        dataToSend = fetchFollowingDetails(temp)
      
        '''for i in range(len(notifDB)): 
            temp = {}
            temp['notification'] = notifDB[i]['notification']
            temp['dateTime'] = notifDB[i]['date']
            temp['read'] = notifDB[i]['read']
            dataToSend.append(temp)'''

        '''try : 
            page_size = request.GET['page_size']
            p = Paginator(dataToSend, page_size)
            page = request.GET.get('page', 1)
            finalData=p.page(page).object_list

        except Exception as e:
            print("Some error  occured" ,e)
            finalData = p.page(1).object_list'''
    
        return Response({
                    'status': 200,
                    'message': "Success",
                    'data' : dataToSend
                })

    except Exception as e:
        print(e)
        message="Failed to fetch followRequestNotifications "
        return Response({
                    'status': 400,
                    'message': message,
                    'data':None
                })

@extend_schema(methods=['post'],
            request = fetchActivityNotificationRequest,
            responses={200: fetchActivityNotificationResponse,
            400 : ErrorResponseNotification})
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def fetchActivity(request):
    print("Inside fetchActivity")
    try:
        user = User.objects.get(id = request.user.id)
        data = request.data
        
        finalData = []
        page_size = 1 
        page = 1

        notifDB = notifications.objects.filter(userId_id = user.id).values()
        #totalRecords=len(notifDB)
        for i in range(len(notifDB)): 
            temp = {}
            temp['id'] = notifDB[i]['id']
            temp['notification'] = notifDB[i]['notification']
            temp['dateTime'] = notifDB[i]['date']
            temp['read'] = int(notifDB[i]['read'])
            temp['lastVisitedTime'] = notifDB[i]['lastVisitedTime']
            userData = User.objects.get(id=int(notifDB[i]['fromId_id']))
           
            temp['userId'] = str(userData.id)
            temp['username'] = userData.username
            temp['fullname']  = userData.first_name + " " +userData.last_name
            
            profileData = profile.objects.get(user_id = userData.id)
            temp['profileImage'] = profileData.profileImage.url

            #  Mark every notification as read 
            try :
                notifDataToUpdate = notifications.objects.get(id = notifDB[i]['id'],
                                                            read = 0)
                notifDataToUpdate.read = 1
                notifDataToUpdate.lastVisitedTime = timezone.localtime(timezone.now())
                notifDataToUpdate.save()
            except Exception as e : 
                pass
            
            finalData.append(temp)
            
        return Response({
                    'status': 200,
                    'message': "Success",
                    'data' : finalData
                })

    except Exception as e:
        print(e)
        message="Failed to fetch activity "
        return Response({
                    'status': 400,
                    'message': message,
                    'data':None
                })



    