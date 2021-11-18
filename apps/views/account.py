import jwt
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from apps.models.account.models import User
from apps.serializers.account import SigninSerializer, SignoutSerializer
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from error_description import error


class UsersViewSet(ModelViewSet):
    """
    list : 유저 정보 조회
    partial_update : 유저 부분 수정
    """

    def list(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass


class SigninViewSet(ModelViewSet):
    """
    create : 로그인
    """
    queryset = User.objects.all()
    serializer_class = SigninSerializer
    permission_classes = []

    login_response_schema_dict = {
        201: openapi.Schema(
            'response_data',
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema('token 값(JWT)', type=openapi.TYPE_STRING),
            },
        ),
        400: openapi.Schema(
            'error_response',
            type=openapi.TYPE_OBJECT,
            properties={
                error.APPLY_400_1_NO_REQUIRED_PARAMETERS.get_error_code():
                    error.APPLY_400_1_NO_REQUIRED_PARAMETERS.get_error_description(),
                error.APPLY_400_2_AUTHENTICATION_REQUIRED.get_error_code():
                    error.APPLY_400_2_AUTHENTICATION_REQUIRED.get_error_description(),
                error.APPLY_400_3_ACCOUNT_ERROR.get_error_code():
                    error.APPLY_400_3_ACCOUNT_ERROR.get_error_description(),
                error.APPLY_400_4_WITHDRAWAL.get_error_code():
                    error.APPLY_400_4_WITHDRAWAL.get_error_description(),
            }
        ),
        405: openapi.Schema(
            'error_response',
            type=openapi.TYPE_OBJECT,
            properties={
                error.APPLY_405_METHOD_NOT_ALLOWED.get_error_code():
                    error.APPLY_405_METHOD_NOT_ALLOWED.get_error_description()
            }
        ),
        500: openapi.Schema(
            'error_response',
            type=openapi.TYPE_OBJECT,
            properties={
                error.APPLY_500_SERVER_ERROR.get_error_code():
                    error.APPLY_500_SERVER_ERROR.get_error_description()
            }
        )
    }

    def params_validate(self, request):
        """파라미터 유효성 검사"""
        loss_params = []
        is_params_checked = True
        response_message = {}
        status_code = status.HTTP_400_BAD_REQUEST

        # http method 는 없어도 됨
        if request.method == 'POST':
            request_data = request.data
        else:
            is_params_checked = False
            response_message = {'405': f'{request.method}요청은 허용하지 않습니다.'}
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            return response_message, status_code, is_params_checked

        email = request_data.get('email', None)
        password = request_data.get('password', None)

        if email is None:
            loss_params.append('email')
        if password is None:
            loss_params.append('password')

        if loss_params:
            is_params_checked = False
            response_message = {'400-1': f'필수파라미터({",".join(loss_params)})가 없습니다.'}
            return response_message, status_code, is_params_checked
        return response_message, status_code, is_params_checked

    def signin(self, request):
        """로그인을 위한 로직"""
        if self.params_validate(request):
            is_checked = False
            response_message = {}
            status_code = status.HTTP_400_BAD_REQUEST

            email = request.data.get('email')
            password = request.data.get('password')

            user = authenticate(email=email, password=password) if email and password else None

            if user and user.is_authenticated and user.is_active and user.is_approval and not user.is_withdrawal:
                is_checked = True
                login(request, user)
                encoded_jwt = jwt.encode(
                    {
                        'pk': user.pk
                    },
                    settings.SECRET_KEY,
                    algorithm='HS256'
                )
                response_message.update({
                    'token': encoded_jwt
                })
                status_code = status.HTTP_201_CREATED
                return response_message, status_code, is_checked
            elif user and not user.is_approval:
                response_message = {'400-2': '회원 계정 활성을 위해 SMS 인증이 필요합니다.'}
                return response_message, status_code, is_checked
            elif user and user.is_withdrawal:
                response_message = {'400-4': '탈퇴한 회원입니다.'}
                return response_message, status_code, is_checked
            else:
                response_message = {'400-3': '이메일 또는 패스워드가 일치하지 않습니다.'}
                return response_message, status_code, is_checked

    @swagger_auto_schema(
        responses=login_response_schema_dict
    )
    def create(self, request, *args, **kwargs):
        """
        로그인

        ---
        ## /api/v1/account/signin/
        """
        # 로그인 성공시 토큰 생성됨
        try:
            response_message, status_code, is_checked = self.params_validate(request)
            if is_checked:
                response_message, status_code, is_checked = self.signin(request)
            return Response(
                data=response_message if is_checked else response_message,
                status=status_code if is_checked else status_code
            )

        except Exception as e:
            print(f'error : {e}')
            response_message = {'500': '서버 에러'}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(data=response_message, status=status_code)


class SignoutViewSet(ModelViewSet):
    """
    update : 로그아웃
    """
    queryset = User.objects.all()
    serializer_class = SignoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def signout(self, request):
        """로그아웃을 위한 로직"""
        is_checked = False
        response_message = {}
        status_code = status.HTTP_401_UNAUTHORIZED

        if self.request.user.is_authenticated:
            is_checked = True
            logout(request)
            status_code = status.HTTP_200_OK
            return response_message, status_code, is_checked
        else:
            response_message = {'401-1': '유효하지 않은 정보입니다.'}
            return response_message, status_code, is_checked

    def update(self, request, *args, **kwargs):
        """
        로그아웃

        ---
        ## /api/v1/account/signout/
        """
        try:
            response_message, status_code, is_checked = self.signout(request)
            return Response(
                data=response_message if is_checked else response_message,
                status=status_code if is_checked else status_code
            )
        except Exception as e:
            print(f'error : {e}')
            response_message = {'500': '서버 에러'}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(data=response_message, status=status_code)
