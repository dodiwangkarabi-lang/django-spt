from accounts.api.serializers import (
    UserSerializer,
    ProfileSerializer, UserProfileSerializer
)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from django.contrib.auth.models import User
from accounts.models import Profile

from django.db import transaction

class UserAktifView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        instance = request.user
        serializers = UserProfileSerializer(instance, many=False)
        data = serializers.data
        return Response({
            "message": "success",
            "success": True,
            "data": data
        })

class UserView(APIView):
    def get(self, request, format=None):
        qs = User.objects.all()
        serializers = UserProfileSerializer(qs, many=True)
        data = serializers.data
        return Response({
            "message": "success",
            "success": True,
            "data": data
        })
    
    def post(self, request, format=None):
        pass
    
class UserDetailView(APIView):
    def get(self, request, user_id, format=None):
        instance = User.objects.get(id=user_id)
        serializer = UserProfileSerializer(instance, many=False)
        data = serializer.data
        return Response({
            "message": "success",
            "success": True,
            "data": data
        })
    
    def post(self, request, user_id, format=None):
        data = request.data
        instance = User.objects.get(id=user_id)
        serializer = UserProfileSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "success",
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "error",
            "success": False,
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, user_id, format=None):
        instance = User.objects.get(id=user_id)
        instance.delete()
        return Response({
            "message": "success",
            "success": True
        }, status=status.HTTP_200_OK)
        
    def put(self, request, user_id, format=None):
        data = request.data
        instance = User.objects.get(id=user_id)
        serializer = UserProfileSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "success",
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "error",
            "success": False,
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AkunMeView(APIView):
    permission_classes = [IsAuthenticated] # login required
    
    def get(self, request, format=None):
        obj = request.user
        serializer = UserProfileSerializer(obj, many=False)
        data = serializer.data
        
        return Response({
            "message": "success",
            "success": True,
            "data": data
        })

class AkunListView(APIView):
    permission_classes = [IsAuthenticated] # login required
    
    def get(self, request, format=None):
        qs = User.objects.all()
        serializer = UserProfileSerializer(qs, many=True)
        data = serializer.data
        return Response({
            "message": "success",
            "success": True,
            "data": data
        })

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    @transaction.atomic
    def perform_destroy(self, instance):

        user = instance.user

        instance.delete()

        user.delete()