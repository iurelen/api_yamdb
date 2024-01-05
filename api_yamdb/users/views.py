from django.contrib.auth import get_user_model
from django.core.mail import send_mail

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
from .utils import code_generator

CustomUser = get_user_model()


class SignupTestView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        code = code_generator()
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(confirmation_code=code, role='admin')
            send_mail(
                subject='Регистрация в YaMDb',
                message=f'Код подтверждения: {code}.',
                from_email='not_reply@yamdb.com',
                recipient_list=[request.data.get('email')],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if 'username' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        code = code_generator()
        if CustomUser.objects.filter(
            username=request.data['username']
        ).exists():
            user = CustomUser.objects.get(username=request.data['username'])
            serializer = UserRegistrationSerializer(user, data=request.data)
        else:
            serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
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
        if 'username' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(username=request.data['username'])
        serializer = TokenObtainSerializer(
            user, data=request.data
        )
        if serializer.is_valid():
            confirmation_code = serializer.data.get('confirmation_code')
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
    lookup_field = 'username'
    queryset = CustomUser.objects.all()
    # serializer_class = UserRegistrationSerializer
    serializer_class = CustomUserSerializer
    # permission_classes = (IsAuthenticated,)
    # permission_classes = (AllowAny,)
    permission_classes = (IsAuthenticated, IsAdminOrSuperuser,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

    # def get_serializer_class(self):
    #    if self.action == 'post':
    #        return UserRegistrationSerializer
    #    return CustomUserSerializer

#    def perform_create(self, serializer):
#        if 'role' not in serializer.validated_data:
#            serializer.save(role='user')

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = CustomUserSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.validated_data['role'] = request.user.role
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
