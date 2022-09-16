from rest_framework import serializers

class sigupRequest(serializers.Serializer):
    firstName = serializers.CharField(max_length=30,required=True)
    lastName = serializers.CharField(max_length=30,required=True)
    mobileNumber = serializers.CharField(max_length=15,required=False)  
    email = serializers.CharField(max_length=50,required=True)  
    role = serializers.CharField(max_length=5,required=True) 
    password = serializers.CharField(max_length=50,required=True)  
    confirm_password = serializers.CharField(max_length=50,required=True)  
    termsAgreed = serializers.IntegerField()
    isOnBoardingCompleted = serializers.IntegerField()
    
class signUpData(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    mobileNumber = serializers.CharField(max_length=15)
    otp = serializers.IntegerField()

class signupResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data=signUpData()


class ErrorResponse(serializers.Serializer):
    message=serializers.CharField(max_length=50)
    status=serializers.IntegerField()
    data = serializers.CharField(allow_null=True)   
  
class loginEmailPwdRequest(serializers.Serializer):
    emailMobile=serializers.CharField(max_length=50)
    password=serializers.CharField(max_length=50)

class loginMobilePwdRequest(serializers.Serializer):
    mobileNumber=serializers.CharField(max_length=50)
    password=serializers.CharField(max_length=50)

class loginData(serializers.Serializer):
    refresh = serializers.CharField(max_length=250)
    access  = serializers.CharField(max_length=250)
    otp = serializers.IntegerField()
    email = serializers.CharField(max_length=50)
    mobileNumber = serializers.CharField(max_length=15)
    mobileNumberVerified = serializers.BooleanField()
    isOnBoardingCompleted = serializers.IntegerField()

class loginResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=loginData()

class notVerifiedData(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    mobileNumber = serializers.CharField(max_length=15)
    otp = serializers.IntegerField()

class notVerifiedReponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data= notVerifiedData()

class verifyOTPRequest(serializers.Serializer):
    otp = serializers.IntegerField()
    email = serializers.CharField(max_length=50)
    mobileNumber = serializers.CharField(max_length=15)
    
class verifyOTPData(serializers.Serializer) :
    refresh = serializers.CharField(max_length=250)
    access  = serializers.CharField(max_length=250)
    isOnBoardingCompleted = serializers.IntegerField()

class verifyOTPResponse(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.CharField(max_length=50)
    data = verifyOTPData()

class resetPasswordRequest(serializers.Serializer):
    password = serializers.CharField(max_length=250)
    confirmPassword = serializers.CharField(max_length=250)

class resetPasswordResponse(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.CharField(max_length=50)

class loginWithOTPRequest(serializers.Serializer):
    mobileNumber = serializers.CharField(max_length=50)

class loginWithOTPData(serializers.Serializer):
    #refresh = serializers.CharField(max_length=250)
    #access  = serializers.CharField(max_length=250)
    email = serializers.CharField(max_length=50)
    mobileNumber = serializers.CharField(max_length=15)
    mobileNumberVerified = serializers.BooleanField()
    otp = serializers.IntegerField()
    isOnBoardingCompleted = serializers.IntegerField()

class loginWithOTPResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=loginWithOTPData()

class validateUsernameRequest(serializers.Serializer):
   username=serializers.CharField(max_length=50,required=True)  
   type = serializers.IntegerField()

class validateUsernameResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)

class validateEmailRequest(serializers.Serializer):
    email=serializers.CharField(max_length=50,required=True)  

class validateEmailResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)

class profilePicRequest(serializers.Serializer):
    profileImage = serializers.FileField()

class profilePicData(serializers.Serializer):
    profileImage = serializers.CharField(max_length=250)

class profilePicResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data = profilePicData()

class langPrefRequest(serializers.Serializer):
    ids=serializers.ListField(child = serializers.IntegerField(min_value = 0, max_value = 10000))

class langPrefResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)

class userInterestRequest(serializers.Serializer):
    ids=serializers.ListField(child = serializers.IntegerField(min_value = 0, max_value = 10000))

class userInterestResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)

class userCategoryRequest(serializers.Serializer):
    ids=serializers.ListField(child = serializers.IntegerField(min_value = 0, max_value = 10000))

class userCategoryResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)

class getUserInterestData(serializers.Serializer):
    id=serializers.IntegerField()
    interest=serializers.CharField(max_length=100)
    isSelected=serializers.IntegerField()

class getUserInterestResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data = getUserInterestData()

class getUserLanguageData(serializers.Serializer):
    id=serializers.IntegerField()
    language=serializers.CharField(max_length=100)
    isSelected=serializers.IntegerField()

class getUserlanguageResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=serializers.ListField(child = getUserLanguageData())

class getUserCategoryData(serializers.Serializer):
    id=serializers.IntegerField()
    category=serializers.CharField(max_length=100)
    isSelected=serializers.IntegerField()

class getUserCategoryResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=getUserCategoryData()

class getUserTalentData(serializers.Serializer):
    id=serializers.IntegerField()
    talents=serializers.CharField(max_length=150)
    tag=serializers.CharField(max_length=150)
    isSelected=serializers.IntegerField()

class getUserTalentResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=serializers.ListField(child = getUserTalentData())

class userGenderData(serializers.Serializer):
    id=serializers.IntegerField()
    gender=serializers.CharField(max_length=15)

class userCountryData(serializers.Serializer):
    id=serializers.IntegerField()
    country=serializers.CharField(max_length=25)

class getProfileData(serializers.Serializer):
    profileImage = serializers.CharField(max_length=300)
    userId = serializers.CharField(max_length=50)
    firstName = serializers.CharField(max_length=100)
    lastName = serializers.CharField(max_length=100)
    username  = serializers.CharField(max_length=100)
    bio  = serializers.CharField(max_length=250)
    email = serializers.CharField(max_length=100)
    mobileNumber = serializers.CharField(max_length=50)
    gender = userGenderData()
    country = userCountryData()
    isOnBoardingCompleted = serializers.IntegerField()
    
class getProfileResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data=getProfileData()

class UnauthorizedResponse(serializers.Serializer):
    status= serializers.IntegerField()
    messsage = serializers.CharField(max_length=50)

class updateProfileRequest(serializers.Serializer):
    #profileImage = serializers.ImageField(required=False)
    firstName = serializers.CharField(max_length=100, required=False)
    lastName = serializers.CharField(max_length=100, required=False)
    username  = serializers.CharField(max_length=100, required=False)
    bio  = serializers.CharField(max_length=250, required=False)
    #email = serializers.CharField(max_length=50,required=False)  
    #mobileNumber = serializers.CharField(max_length=15,required=False)  
    gender = serializers.IntegerField(required=False)
    country = serializers.IntegerField(required=False)
    isOnBoardingCompleted = serializers.IntegerField(required=False)

class updateProfileResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)

class userTalentRequest(serializers.Serializer):
    interest = serializers.ListField(child = serializers.IntegerField(min_value = 0, max_value = 10000))
    category = serializers.ListField(child = serializers.IntegerField(min_value = 0, max_value = 10000))

class userTalentResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)

class contactUsRequest(serializers.Serializer):
    username=serializers.CharField(max_length=100)
    email=serializers.CharField(max_length=100)
    message= serializers.CharField(max_length=300)

class contactUsResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data = serializers.CharField(allow_null=True) 

class helpData(serializers.Serializer):
    question = serializers.CharField(max_length=200)
    answer = serializers.CharField(max_length=500)

class helpResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data = serializers.ListField(child=helpData()) 

class fcmRegisterDeviceRequest(serializers.Serializer):
    registration_id=serializers.CharField(max_length=150)

class fcmRegisterDeviceResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data = serializers.CharField(allow_null=True) 

class accountPrivacyRequest(serializers.Serializer):
    privacy=serializers.IntegerField()

class accountPrivacyResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data = serializers.CharField(allow_null=True) 

class fetchAccountPrivacyData(serializers.Serializer):
    isPrivate = serializers.IntegerField()

class fetchAccountPrivacyResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data = fetchAccountPrivacyData()
'''
class mainSettingsData(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    mobileNumber = serializers.CharField(max_length=15)

class mainSettingsResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data = mainSettingsData()

class mainSettingRequest(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    mobileNumber = serializers.CharField(max_length=15)
'''

class updateNotifRequest(serializers.Serializer):
    status = serializers.IntegerField()

class fetchNotifData(serializers.Serializer):
    status = serializers.IntegerField()


class fetchNotifSettingsResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data = serializers.ListField(child = fetchNotifData())

class updateNotifResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data =serializers.CharField(allow_null=True) 

class updateInteractionRequest(serializers.Serializer):
    posts = serializers.IntegerField()
    comments = serializers.IntegerField()
    mentions = serializers.IntegerField()
    messages = serializers.IntegerField()
    activityStatus = serializers.IntegerField()

class updateInteractionResponse(serializers.Serializer):
    status=serializers.IntegerField()
    message=serializers.CharField(max_length=50)
    data =serializers.CharField(allow_null=True) 

class fetchInteractionData(serializers.Serializer):
    posts = serializers.IntegerField()
    comments = serializers.IntegerField()
    mentions = serializers.IntegerField()
    messages = serializers.IntegerField()
    activityStatus = serializers.IntegerField()

class fetchInterationsResponse(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.CharField(max_length=50)
    data = serializers.ListField(child = fetchInteractionData())

class linkData(serializers.Serializer):
    linkType = serializers.IntegerField()
    linkPath = serializers.CharField(max_length = 400)

class linkVerficationData(serializers.Serializer):
    linkType = serializers.IntegerField()
    linkPath = serializers.CharField(max_length = 400)

class fetchVerificationData(serializers.Serializer):
    username  = serializers.CharField(max_length=250)
    fullname = serializers.CharField(max_length=200)
    isZipchoVerified = serializers.IntegerField()
    documentId = serializers.IntegerField()
    docPath = serializers.CharField(max_length=400)
    link = serializers.ListField( child = linkVerficationData() )

class fetchVerificationResponse(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.CharField(max_length=50)
    data = serializers.ListField(child = fetchVerificationData())

class linkData(serializers.Serializer):
    linkType = serializers.IntegerField()
    linkPath = serializers.CharField(max_length = 400)

class applyVerificationRequest(serializers.Serializer):
    documentId = serializers.IntegerField()
    document = serializers.FileField()
    link = serializers.ListField( child = linkData() )

class applyVerificationResponse(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.CharField(max_length=50)
    data = serializers.CharField(allow_null=True) 

