from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Heartbeat

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class HeartbeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heartbeat
        fields = ['id', 'value', 'timestamp', 'user']
        read_only_fields = ['timestamp', 'user']
