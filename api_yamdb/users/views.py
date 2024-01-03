from random import randint

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .permissions import IsAdminOrSuperuser
from .serializers import (CustomUserSerializer, TokenObtainSerializer,
                          UserRegistrationSerializer)


class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            code = randint(111111, 999999)
            # убрать повторное сохранение
            serializer.save(confirmation_code=code)
            send_mail(
                subject='Регистрация в YaMDb',
                message=f'Код подтверждения: {code}.',
                from_email='not_reply@yamdb.com',
                recipient_list=[request.data.get('email')],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            confirmation_code = serializer.data.get('confirmation_code')
            user = get_object_or_404(CustomUser, username=username)
            if confirmation_code != user.confirmation_code:
                return Response(
                    serializer.errors,
                    status=status.HTTP_401_UNAUTHORIZED
                )
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomUserViewSet(viewsets.ModelViewSet):
    # PUT-запрос к `/api/v1/users/{username}/` не предусмотрен
    lookup_field = 'username'
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, IsAdminOrSuperuser,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        # methods=['get', "PATCH"],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = CustomUserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.validated_data['role'] = request.user.role
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = CustomUser.objects.get(username=user.username)
        return queryset
