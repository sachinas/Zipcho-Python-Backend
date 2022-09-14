from django.http import HttpResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import *
from .zipchoReponse import *


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard(request):
    html = "<html><body>Dashboard</body></html>"
    return HttpResponse(html)

@extend_schema(methods=['get'],
                    responses={200: languagesReponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([AllowAny,])                    
def getAllLanguages(request):
    try : 
        print("At languages")
        langData = list(language.objects.all().values('id','language'))
        print(langData)
        return Response({"status": 200,"message":"Success","data":langData})
       
    except Exception as e : 
        print(e)
        message = "Failed while fetching Languages "
        return Response({"status": 400,"message": message, "data": None})
    
@extend_schema(methods=['get'],
                    responses={200: interestReponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([AllowAny,])                    
def getAllInterests(request):
    try : 
        print("At getAllInterests")
        intData = list(interest.objects.all().values('id','interest'))
        print(intData)
        return Response({"status": 200,"message":"Success","data":intData})
       
    except Exception as e : 
        print(e)
        message = "Failed while fetching Interests "
        return Response({"status": 400,"message": message, "data": None})

@extend_schema(methods=['get'],
                    responses={200: genderReponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([AllowAny,])                    
def getAllGender(request):
    try : 
        print("At getAllGender")
        genData = list(gender.objects.all().values('id','gender'))
        print(genData)
        return Response({"status": 200,"message":"Success","data":genData})
       
    except Exception as e : 
        print(e)
        message = "Failed while fetching Gender "
        return Response({"status": 400,"message": message, "data": None})

@extend_schema(methods=['get'],
                    responses={200: categoryReponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([AllowAny,])                    
def getAllCategories(request):
    try : 
        print("At getAllCategories")
        catData = list(category.objects.all().values('id','interest','category'))
        print(catData)
        return Response({"status": 200,"message":"Success","data":catData})
       
    except Exception as e : 
        print(e)
        message = "Failed while fetching Category "
        return Response({"status": 400,"message": message, "data": None})

@extend_schema(methods=['get'],
                    responses={200: countryResponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([AllowAny,])                    
def getAllCountries(request):
    try : 
        print("At getAllCountries")
        counData = list(country.objects.all().values('id','country'))
        print(counData)
        return Response({"status": 200,"message":"Success","data":counData})
       
    except Exception as e : 
        print(e)
        message = "Failed while fetching Country "
        return Response({"status": 400,"message": message, "data": None})

@extend_schema(methods=['get'],
                    responses={200: identityDocumentsResponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([IsAuthenticated])                    
def getAllIdentityDocuments(request):
    try : 
        print("At getAllIdentityDocuments")
        idenData = list(identityDocument.objects.all().values('id','document'))
        print(idenData)
        return Response({"status": 200,"message":"Success","data":idenData})
       
    except Exception as e : 
        print(e)
        message = "Failed while fetching getAllIdentityDocuments "
        return Response({"status": 400,"message": message, "data": None})

@extend_schema(methods=['get'],
                    responses={200: verificationLinkResponse, 400: ErrorResponse})
@api_view(['GET'])
@permission_classes([IsAuthenticated])                    
def getAllVerificationLinks(request):
    try : 
        print(request.user.id)
        print("At getAllVerificationLinks")
        idenData = list(verificationLink.objects.all().values('id','linkType'))
        print(idenData)
        return Response({"status": 200,"message":"Success","data":idenData})
       
    except Exception as e : 
        print(e)
        message = "Failed while fetching getAllVerificationLinks "
        return Response({"status": 400,"message": message, "data": None})
