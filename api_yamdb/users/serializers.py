import secrets
import string

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core import validators

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import ROLE_CHOICE

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=(validators.MaxLengthValidator(254),),
        required=True
    )

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
    email = serializers.EmailField(
        max_length=254,
        validators=(validators.MaxLengthValidator(254),)
    )
    username = serializers.SlugField(
        max_length=150,
        validators=(
            validators.MaxLengthValidator(150),
            validators.RegexValidator(r'^[\w.@+-]+\Z')
        )
    )
    role = serializers.ChoiceField(
        choices=ROLE_CHOICE,
        required=False,
        default='user'
    )

    class Meta:
        model = User
        fields = '__all__'
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

    def create(self, validated_data):
        generated_password = User.objects.make_random_password()
        validated_data['password'] = generated_password
        user = super().create(validated_data)
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(default='user')

    class Meta:
        model = User
        fields = ('username', 'email',)
