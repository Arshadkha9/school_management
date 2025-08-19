from rest_framework import serializers
from .models import UserLogin
from django.contrib.auth.password_validation import validate_password
from .models import ParentsData


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = ['id', 'name', 'mobile', 'email', 'user_id', 'is_active', 'is_superuser', 'last_login', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserLogin
        fields = ['email', 'name', 'mobile', 'password', 'password2', 'is_active', 'is_superuser']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = UserLogin.objects.create_user(password=password, **validated_data)
        return user



class ParentsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentsData
        fields = ['father_name',
            'father_occupation',
            'father_email',
            'mother_name',
            'mother_occupation',
            'mother_email',]

{
    "father_name":"arshad",
    "father_occupation":"farmer",
    "created_at":"2025-12-08"
}