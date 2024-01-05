from django.contrib.auth import get_user_model
from django.core import validators

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# from .models import CustomUser


CustomUser = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=(validators.MaxLengthValidator(254),),
        required=True
    )

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

    class Meta:
        model = CustomUser
        fields = ('username', 'email',
                  'first_name', 'last_name', 'bio', 'role'
                  )
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['username', 'email']
            )
        ]
#        extra_kwargs = {
#            'username': {'required': True},
#            'email': {'required': True},
#        }


#    def validate(self, data):
#        string = str(data.get('last_name'))
#        if len(string) > 150:
#            raise serializers.ValidationError(
#                'Должно быть менее 254 символов.')
#        return data

#    def validate_email(self, value):
#        email_string = str(value)
#        if len(email_string) > 254:
#            raise serializers.ValidationError(
#                'Должно быть менее 254 символов.'
#            )
#        return value

class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(default='user')

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)
