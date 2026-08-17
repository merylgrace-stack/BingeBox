from django.shortcuts import render
from rest_framework.decorators import (api_view,permission_classes,authentication_classes)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (TokenAuthentication,SessionAuthentication,)
from django.http import JsonResponse

from .models import Media
from .serializers import MediaSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def home(request):
    media = Media.objects.all()

    return render(request, 'watchlist/home.html', {
        'media': media
    })


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def media_list(request):

    if request.method == 'GET':
        media = Media.objects.filter(user=request.user)
        serializer = MediaSerializer(media, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MediaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT','PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def media_detail(request, pk):
    try:
        media = Media.objects.get(pk=pk,user=request.user)
    except Media.DoesNotExist:
        return Response({"error": "Media not found"}, status=404)

    if request.method == 'GET':
        serializer = MediaSerializer(media)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = MediaSerializer(media, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == 'PATCH':
        serializer = MediaSerializer(
            media,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        media.delete()
        return Response(status=204)

def api_test(request):
    return JsonResponse({
        "message": "Welcome to BingeBox API",
        "status": "working"
    })

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"error": "Username and password are required."},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists."},
            status=400
        )

    user = User.objects.create_user(
        username=username,
        password=password
    )

    token = Token.objects.create(user=user)

    return Response({
        "message": "Account created successfully.",
        "token": token.key,
        "username": user.username
    }, status=201)