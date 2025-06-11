from django.shortcuts import render,get_object_or_404
from rest_framework.generics import GenericAPIView,RetrieveUpdateAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from .serializers import UploadAvatarSerializer,SignupSerializer,ProfileSerializer, ChangePasswordSerializer,UpdateProfileSerializer
from django.contrib.auth import get_user_model, update_session_auth_hash
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Profile

User = get_user_model()

class SignupView(GenericAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'user created successfully'} , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if not hasattr(user, 'profile'):
            # پروفایل وجود نداره، بساز
            from accounts.models import Profile
            Profile.objects.create(user=user)
        return user.profile

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]

    def put(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = UpdateProfileSerializer(instance=profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"details": "Profile updated successfully "}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadAvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = UploadAvatarSerializer(instance=profile,data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response({'avatar_url': serializer.data['avatar']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublicProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        userid = self.kwargs['user_id']
        user = get_object_or_404(User, id=userid)

        return user.profile
        

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(request.data) 

        user = request.user

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"message": 'the current password is incorrect'},status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            update_session_auth_hash(request,user)

            return Response({"details": "Password changed successfully."},status=status.HTTP_200_OK)

        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        




