"""This module contain class serializers"""
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for entity user"""
    password = serializers.CharField(max_length=65, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=4)
    last_name = serializers.CharField(max_length=255, min_length=4)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email already used"})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
