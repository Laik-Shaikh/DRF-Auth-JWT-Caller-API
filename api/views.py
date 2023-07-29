from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from . models import RegisterUser, SpamNumber
from . serializers import UserSerializer, LoginSerializer, SpamNumberSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from django.db.models import Q



@api_view(['GET'])
def index(request):
    dict = {
        'name' : "Computer Science",
        'cut-offs' : 92,
        'duration' : '4 Years',
        'fees' : 350000,
        "subjects" : ['C++', "Java", "Python", "Machine Learning"]
    }

    return Response(dict)

@api_view(['POST'])
def registerUser(request):
    if request.method == 'POST':
        data = request.data
        data['password'] = make_password(data['password'])
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=201)
            except:
                return Response({'message' : 'something went wrong'}, status=500)
        else:
            return Response(serializer.errors, status=400)


@api_view(['POST'])
def loginUser(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        data = serializer.data
        
        try:
            user = RegisterUser.objects.get(phone_number=data['phone_number'])
            if not check_password(data['password'], user.password):
                return Response({
                    'Success' : False,
                    'Message' : 'Invalid Credentials'
                }, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        except RegisterUser.DoesNotExist:
            return Response({
                'Success': False,
                'Message': 'This Phone Number is Not Registered.'
            }, status=status.HTTP_404_NOT_FOUND)
        
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
@api_view(['GET'])
def getUser(request, id):
    user = RegisterUser.objects.get(pk=id)
    serialize = UserSerializer(user)
    return Response(serialize.data)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getRegisteredUser(request):
    if request.method == 'GET':
        users = RegisterUser.objects.all()
        serialize = UserSerializer(users, many = True)
        return Response(serialize.data, status=200)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def markNumberSpam(request):
    data = request.data
    serializer = SpamNumberSerializer(data=data)

    if serializer.is_valid():
        data = serializer.data
        if SpamNumber.objects.filter(phone_number = data['phone_number']).exists():
            data = SpamNumber.objects.get(phone_number = data['phone_number'])
            data.spamCount = data.spamCount + 1
            data.save(update_fields=['spamCount'])
            serializer = SpamNumberSerializer(data) 
            return Response({
                'Success' : True,
                'data': serializer.data
            }, status=status.HTTP_202_ACCEPTED)
        else:
            print(data['phone_number'])
            markedSpam = SpamNumber.objects.create(phone_number = data['phone_number'])
            return Response({
                'Success' : True,
                'data': markedSpam
            }, status=status.HTTP_201_CREATED)

    return Response({
        'Success' : False,
        'Message' : serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getUsersUsingPhoneNumberOrName(request):
    param = request.GET.get('search', '')
    # print(type())
    param = json.loads(param)
    print(param)
    try:
        # users = RegisterUser.objects.filter(phone_number__icontains = param) | RegisterUser.objects.filter(name__contains = param)
        users = RegisterUser.objects.filter(Q(phone_number__contains = param) | Q(name__contains = param)).values()
        print(users.count())

        serialize = UserSerializer(users, many = True)
        
    except RegisterUser.DoesNotExist:
        return Response({
            'Success' : False,
            'Message' : "No Records Found"
        })

    return Response({
        'Success' : True,
        'data' : serialize.data
    }, status=status.HTTP_200_OK)