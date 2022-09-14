from .views import*
from zipchoAdmin.views import *
from django.urls import path, include

urlpatterns = [
    path('fcmRegister', fcmRegisterDevice, name='fcmRegisterDevice'),
    path('login', login, name = 'login'),
    #path('requestOTP', requestOTP, name='requestOTP'),
    path('loginWithOTP', loginWithOTP, name="loginWithOTP"),
    path('signup', signUp, name="signupUser"),
    path('verifyOTP', verifyOTP, name='verifyOTP'),
    path('resetPassword', resetPassword, name='resetPassword'),

    path('validateUsername', validateUsername, name="validateUsername"),
    path('validateEmail', validateEmail, name="validateEmail"),

    #Profile 
    path('profilePicUpdate', profilePicUpdate.as_view()),
    #path('profilePicUpdate', profilePicUpdate, name ="profilePicUpdate"),
    path('getProfile', getProfile, name = 'getProfile'),
    path('updateProfile', updateProfile, name='updateProfile'),

    # gender 
    path("getUserGender", getUserGender, name= "getUserGender"),
    
    # Country
    path("getUserCountry", getAllCountry, name= "getUserCountry"),

    # Languages
    path('getUserlanguages', getUserlanguages, name="getUserlanguages"),
    path('languagePreferences', languagePreferences, name="languagePreferences"),
    
    # Interest 
    path('userInterests', userInterests, name="userInterests"),
    path('getUserInterests', getUserInterests, name="getUserInterests"),

    # Category 
    path('userCategory', userCategories, name="userCategory" ),
    path('getUserCategory', getUserCategory , name="getUserCategory"),

    # Talent 
    #path('getUserTalent', getUserTalent, name='getUserTalent'),
    #path('userTalent', userTalents, name='userTalent'),

    #Settings
    path('contactUs', contactUs, name='contactUs'),
    path('help', help, name='help'),
    #path('fetchMainSettings', fetchMainSettings, name='fetchMainSettings'),
    #path('mainSettings', mainSettings, name='mainSettings'),
    
    # Notification
    path('fetchNotificationSettings', fetchNotificationSettings, name='fetchNotificationSettings'),
    path('updateNotificationSettings', updateNotificationSettings, name = 'updateNotificationSettings'),

    # Privacy
    path('accountPrivacy', accountPrivacy, name='accountPrivacy'),
    path('fetchAccountPrivacy', fetchAccountPrivacy, name='fetchAccountPrivacy'),
    
    path('fetchInteractions', fetchInteractions, name='fetchInteractions'),
    path('updateInteractions', updateInteractions, name = 'updateInteractions'),

    # apply for verification
    path('fetchVerification', fetchVerification, name= 'fetchVerification'),
    path('applyVerification', applyVerification, name = 'applyVerification'),
    path("getAllIdentityDocuments", getAllIdentityDocuments, name= "getAllIdentityDocuments"),
    path("getAllVerificationLinks", getAllVerificationLinks, name= "getAllVerificationLinks")

]