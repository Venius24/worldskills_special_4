from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Address, SecurityQuestion

User = get_user_model()


class SecurityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityQuestion
        fields = ['id', 'question']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    security_question = serializers.PrimaryKeyRelatedField(
        queryset=SecurityQuestion.objects.filter(is_active=True)
    )
    security_answer = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 
                  'confirm_password', 'security_question', 'security_answer', 'is_subscribed']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        security_answer = validated_data.pop('security_answer')
        user = User.objects.create_user(**validated_data)
        user.security_answer = security_answer
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 
                  'phone', 'profile_image', 'is_subscribed', 'preferred_delivery']
        read_only_fields = ['email']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'label', 'street', 'city', 'state', 'postal_code', 
                  'country', 'is_preferred', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']