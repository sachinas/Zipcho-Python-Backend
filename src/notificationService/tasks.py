import json

import redis
import requests
from authentication.models import User
from celery.decorators import task
from core.settings.base import (PUSH_NOTIFICATIONS_SETTINGS, REDIS_HOST,
                                REDIS_PORT)

from notificationService.models import notifications

redisInstance = redis.Redis(host = REDIS_HOST,
                            port = REDIS_PORT, db=0)

def sendNotification(reqgistrationIds, title, message):
    try : 
        print("At Send Notification")
        url = "https://fcm.googleapis.com/fcm/send"

        headers = {
            "Content-Type": "appicatiomn/json",
            "Authorization": 'key='+PUSH_NOTIFICATIONS_SETTINGS['FCM_API_KEY']
        }

        payload = {
            "to" : reqgistrationIds[0]['registration_id'],
            "notification": {
                            "body": message,
                            "title": title
            }
        }

        result = requests.post(url, data=json.dumps(payload), headers=headers)
        print(result.json())


    except Exception as e :
        print(f"Failed while sending Notication: {e}")
