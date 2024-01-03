from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'username',)

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Некорректное имя пользователя.')
        return data


class TokenObtainSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate(self, data):
        if len(str(data.get('last_name'))) > 150:
            raise serializers.ValidationError(
                'Должно быть менее 254 символов.')
        return data

    def validate_email(self, value):
        if len(str(value)) > 254:
            raise serializers.ValidationError(
                'Должно быть менее 254 символов.'
            )
        return value
