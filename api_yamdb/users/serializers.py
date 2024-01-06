from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import ROLE_CHOICE

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Некорректное имя пользователя.')
        return data


class TokenObtainSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=ROLE_CHOICE,
        required=False,
        default='user'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'first_name',
                  'last_name', 'bio')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'bio': {'required': False}
        }


class MeUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)
