from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class ValidateUserNameMixin:

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Некорректное имя пользователя.')
        return value


class UserRegistrationSerializer(ValidateUserNameMixin,
                                 serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username',)


class TokenObtainSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(ValidateUserNameMixin,
                     serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'first_name',
                  'last_name', 'bio')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email',)
            )
        ]
        extra_kwargs = {
            'password': {'required': False},
            'bio': {'required': False}
        }


class MeUserSerializer(ValidateUserNameMixin,
                       serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)
