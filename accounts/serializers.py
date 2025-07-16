from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser,Profile

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'nikname' ,'email', 'password', 'password2']

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('passwords do not match.')
        return attrs
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username',read_only=True)
    nikname = serializers.CharField(source='user.nikname',read_only=True)
    userid = serializers.CharField(source='user.id',read_only=True)

    class Meta:
        model = Profile 
        fields = ['id', 'userid','username','nikname', 'avatar','bio', 'is_online', 'last_seen']

class UpdateProfileSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    nikname = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    def update(self,instance, validated_data):
        user = instance.user 
        if 'username' in validated_data:
            user.username = validated_data['username']
            user.save()
        if 'nikname' in validated_data:
            user.nikname = validated_data['nikname']
            user.save()

        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance 

class UploadAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        if len(value) < 6 :
            raise serializers.ValidationError('Password must be at least 6 characters long.')
        return value

class GetUsersSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['id', 'nikname'] 

class UpdatePublicKeySerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['public_key']

class GetUserPublicKeySerializer(serializers.ModelSerializer):
    class Meta: 
        model = CustomUser
        fields = ['public_key']