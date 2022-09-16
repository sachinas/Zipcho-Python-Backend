from unittest.util import _MAX_LENGTH
from rest_framework import serializers

class contestTypeData(serializers.Serializer):
    id = serializers.IntegerField
    contestType = serializers.CharField(max_length=200)
    is_active = serializers.IntegerField()

class fetchContestTypeResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.ListField(child = contestTypeData())

class createContestRequest(serializers.Serializer):
    cover_pic = serializers.CharField(max_length=500)
    display_pic = serializers.CharField(max_length=500)
    contest_title = serializers.CharField(max_length=500)
    start_date_time = serializers.DateTimeField()
    category_id = serializers.CharField(max_length=100)
    contestType_id = serializers.CharField(max_length=200)
    isPaid = serializers.BooleanField()

class createContestResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True)   

class ErrorResponseContest(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True)   
