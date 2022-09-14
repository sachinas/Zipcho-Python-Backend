from rest_framework import serializers

class followRequestNotificationsRequest(serializers.Serializer):
    page_size = serializers.IntegerField()
    page = serializers.IntegerField()

class followReqData(serializers.Serializer):
    userId = serializers.CharField(max_length=50)
    username=serializers.CharField(max_length=100)
    fullname=serializers.CharField(max_length=100)
    profileImage=serializers.CharField(max_length=300)
    status = serializers.IntegerField()

class followRequestNotificationsResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data=serializers.ListField(
        child = followReqData()
    )   

class fetchActivityNotificationRequest(serializers.Serializer):
    page_size = serializers.IntegerField()
    page = serializers.IntegerField()

class activityNotificationData(serializers.Serializer):
    id = serializers.IntegerField()
    userId = serializers.CharField(max_length=500)
    notification = serializers.CharField(max_length=500)
    dateTime = serializers.DateField()
    lastVisitedTime = serializers.DateField()
    read = serializers.IntegerField()
    userId = serializers.CharField(max_length=50)
    username=serializers.CharField(max_length=100)
    fullname=serializers.CharField(max_length=100)
    profileImage=serializers.CharField(max_length=300)
    
class fetchActivityNotificationResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data=serializers.ListField(
        child = activityNotificationData()
    )   

class ErrorResponseNotification(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True)   
