from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from api.models import Good,Token
from api.serializers import GoodSerializer,TokenSerializer
from rest_framework.decorators import api_view
from uuid import uuid4

@api_view(["GET"])
def get_token(request):
    token = Token(token=uuid4())
    while Token.objects.filter(token=token.token).exists():
        token = Token(token=uuid4())
    token.save()
    serializer = TokenSerializer(token)
    if serializer.is_valid:
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_goods(request):
    if request.GET.get('token'):
        token = request.GET.get("token")
    else:
        return Response("Token must be present",status=status.HTTP_401_UNAUTHORIZED)
    if not(Token.objects.filter(token=token).exists()):
        return Response("Token is invalid",status=status.HTTP_401_UNAUTHORIZED)
    goods = Good.objects.all()
    serializer = GoodSerializer(goods,many=True)
    if serializer.is_valid:
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # return Response(GoodSerializer(goods,many=True).data,status=status.HTTP_200_OK)

@api_view(["POST"])
def new_good(request):
    if request.GET.get('token'):
        token = request.GET.get("token")
    else:
        return Response("Token must be present",status=status.HTTP_401_UNAUTHORIZED)
    if not(Token.objects.filter(token=token).exists()):
        return Response("Token is invalid",status=status.HTTP_401_UNAUTHORIZED)
    post = request.data
    serializer = GoodSerializer(data=request.data)
    if serializer.is_valid():
        serializer.create(serializer.validated_data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
# Create your views here.
