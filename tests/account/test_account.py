from tests.test import Test
from apps.views.account import SigninViewSet


class AccountTest(Test):
    """계정 관련 테스트 코드"""

    def setUp(self):
        super().setUp()
        self.request.data = {
            'email': self.user_email,
            'password': self.user_password
        }

    def test_signin1(self):
        """로그인 성공"""
        print('[로그인] 성공')
        user_login = SigninViewSet()
        message, status, is_signin = user_login.signin(self.request)

        self.assertEqual(True, is_signin)

    def test_signin2(self):
        """아이디 틀렸을때"""
        print('[로그인] 이메일 틀렸을때')
        self.request.data.update({
            'email': 'aaa@aaa.com',
            'password': '1qaz2wsx'
        })
        user_login = SigninViewSet()
        message, status, is_signin = user_login.signin(self.request)

        self.assertEqual(False, is_signin)
        self.assertEqual(
            '400-3', '400-3' if '400-3' in message.keys() else '0'
        )

    def test_signin3(self):
        """비밀번호 틀렸을때"""
        print('[로그인] 비밀번호 틀렸을때')
        self.request.data.update({
            'email': 'testuser1@test.com',
            'password': '123123'
        })
        user_login = SigninViewSet()
        message, status, is_signin = user_login.signin(self.request)

        self.assertEqual(False, is_signin)
        self.assertEqual(
            '400-3', '400-3' if '400-3' in message.keys() else '0'
        )

    def test_signin4(self):
        """계정 승인이 안되어 있을때"""
        print('[로그인] 승인이 안된 계정이 로그인 시도')
        self.assertEqual(self.user, True)
        self.user.is_approval = False
        self.user.save()
        user_login = SigninViewSet()
        message, status, is_signin = user_login.signin(self.request)

        self.assertEqual(False, is_signin)
        self.assertEqual(
            '400-2', '400-2' if '400-2' in message.keys() else '0'
        )

    def test_signin5(self):
        """탈퇴한 회원이 로그인 하려고 할때"""
        print('[로그인] 탈퇴한 회원의 로그인 시도')
        self.user.is_withdrawal = True
        self.user.save()
        user_login = SigninViewSet()
        message, status, is_signin = user_login.signin(self.request)

        self.assertEqual(False, is_signin)
        self.assertEqual(
            '400-4', '400-4' if '400-4' in message.keys() else '0'
        )

    def test_signout1(self):
        """로그아웃 성공"""
        print('[로그아웃] 성공')

    def test_signout2(self):
        """비인증 유저가 로그아웃 할때"""
        print('[로그아웃] 비인증 유저가 로그아웃 할때')

    def test_signup1(self):
        """회원가입 성공"""
        print('[회원가입] 성공')

    def test_signup2(self):
        """회원가입 이메일 중복"""
        print('[회원가입] 이메일 중복')

    def test_signup3(self):
        """회원가입 휴대폰 번호 중복"""
        print('[회원가입] 휴대폰 번호 중복')

    def test_signup4(self):
        """회원가입 닉네임 중복"""
        print('[회원가입] 닉네임 중복')

    def test_signup5(self):
        """회원가입 사장님 계정으로 가입"""
        print('[회원가입] 사장님 계정 가입 성공')

    def test_signup6(self):
        """회원가입 SMS 인증 성공"""
        print('[회원가입] SMS 인증 성공')

    def test_signup7(self):
        """회원가입 올바른 이메일 값이 맞는지 확인"""
        print('[회원가입] 올바른 이메일 입력인지 확인')

    def test_withdrawal(self):
        """회원탈퇴 성공"""
        print('[회원탈퇴] 성공')
