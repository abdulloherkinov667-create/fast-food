from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['full_name', 'phone_number']

    def validate_phone_number(self, value):
        if Users.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Bu telefon raqami allaqachon ro'yxatdan o'tgan.")
        return value

    def create(self, validated_data):
        phone = validated_data.get('phone_number', '')
        validated_data['username'] = phone
        user = Users.objects.create(**validated_data)
        user.set_unusable_password()
        user.save()
        return user