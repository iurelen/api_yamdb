from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminOrSuperuser
from .serializers import (MeUserSerializer, TokenObtainSerializer,
                          UserRegistrationSerializer, UserSerializer)
from .utils import code_generator

User = get_user_model()


class SignupView(APIView):
    permission_classes = (AllowAny,)
    serializer = UserRegistrationSerializer

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        code = code_generator()
        if not User.objects.filter(username=username, email=email):
            serializer = UserRegistrationSerializer(data=request.data)
        else:
            user = User.objects.get(email=email)
            serializer = UserRegistrationSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(confirmation_code=code)
        send_mail(
            subject='Регистрация в YaMDb',
            message=f'Код подтверждения: {code}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.data.get('email')],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenObtainView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if 'username' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=request.data['username'])
        serializer = TokenObtainSerializer(
            user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get(
            'confirmation_code')
        if int(confirmation_code) != user.confirmation_code:
            return Response(
                {
                    'error': 'Некорректный код подтверждения.',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'token': str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.order_by('username')
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperuser,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = self.request.user
        serializer = MeUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
