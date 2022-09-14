from authentication.models import *
from django.db import models


class notifications(models.Model):
    userId = models.ForeignKey(User,on_delete=models.CASCADE, related_name='notifiedUser')
    notification = models.CharField(max_length=500, null=False, blank= False)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    fromId = models.ForeignKey(User,on_delete=models.CASCADE, related_name='fromUser')  
    lastVisitedTime = models.DateTimeField(auto_now_add=True)

    class Meta : 
        db_table = 'notifications'
