from rest_framework import serializers

class languageData(serializers.Serializer):
    id=serializers.IntegerField()
    language=serializers.CharField(max_length=50)
    
class languagesReponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=serializers.ListField(child =languageData())

class interestData(serializers.Serializer):
    id=serializers.IntegerField()
    interest=serializers.CharField(max_length=50)
    
class interestReponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=serializers.ListField(child =interestData())

class genderData(serializers.Serializer):
    id=serializers.IntegerField()
    gender=serializers.CharField(max_length=50)
    
class genderReponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=serializers.ListField(child =genderData())

class categoryData(serializers.Serializer):
    id=serializers.IntegerField()
    interest=serializers.IntegerField()
    category=serializers.CharField(max_length=50)
    
class categoryReponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=serializers.ListField(child =categoryData())

class countryData(serializers.Serializer):
    id=serializers.IntegerField()
    country=serializers.CharField(max_length=50)
    
class countryResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=serializers.ListField(child =countryData())

class identityDocumentsData(serializers.Serializer):
    id=serializers.IntegerField()
    document=serializers.CharField(max_length=250)

class identityDocumentsResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=serializers.ListField(child =identityDocumentsData())

class verificationLinkData(serializers.Serializer):
    id=serializers.IntegerField()
    linkType=serializers.CharField(max_length=250)

class verificationLinkResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=serializers.ListField(child =verificationLinkData())

class ErrorResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True)   

    class Meta : 
        ref_name = "zipchoAdminError"