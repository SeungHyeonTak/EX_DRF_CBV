from drf_yasg import openapi


class Error:
    """에러 메시지 불러오기"""

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def get_error_code(self):
        return self.code

    def get_error_description(self):
        return openapi.Schema(
            self.message,
            default=self.message,
            type=openapi.TYPE_STRING
        )


APPLY_400_1_NO_REQUIRED_PARAMETERS = Error(
    code='400-1',
    message='필수파라미터가 없습니다.'
)

APPLY_400_2_AUTHENTICATION_REQUIRED = Error(
    code='400-2',
    message='회원 계정 활성을 위해 SMS 인증이 필요합니다.'
)

APPLY_400_3_ACCOUNT_ERROR = Error(
    code='400-3',
    message='이메일 또는 패스워드가 일치하지 않습니다.'
)

APPLY_400_4_WITHDRAWAL = Error(
    code='400-4',
    message='탈퇴한 회원입니다.'
)

APPLY_401_UNAUTHORIZED = Error(
    code='401-1',
    message='유효하지 않은 정보입니다.'
)

APPLY_405_METHOD_NOT_ALLOWED = Error(
    code='405',
    message='(HTTP_METHOD)요청은 허용하지 않습니다.'
)

APPLY_500_SERVER_ERROR = Error(
    code='500',
    message='서버 에러'
)
