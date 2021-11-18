from django.test import TestCase
from django.http.request import HttpRequest
from django.contrib.sessions.backends.db import SessionStore
from apps.models.account.models import User


class Test(TestCase):
    """
    최상위 테스트 케이스

    생성 목적 :
    모든 테스트 케이스는 해당 클래스를 상속 받아 setUp()을 실행한다.
    setUp()은 동일한 테스트 환경을 구성하는데 목적이 있다.
    """
    user_email = 'testuser1@test.com'
    user_nickname = '테스트계정1'
    user_password = '1qaz2wsx'
    user_phone = '01000000000'
    user_birthday = '1999-12-31'

    user2_email = 'testuser2@test.com'
    user2_nickname = '테스트계정2'
    user2_password = '1qaz2wsx'
    user2_phone = '01011111111'
    user2_birthday = '1999-11-15'

    def setUp(self):
        """테스트 환경 셋팅 (유저 생성 등 필요한 부분을 미리 셋팅)"""
        # user1
        self.user = User(
            email=self.user_email,
            nickname=self.user_nickname,
            phone=self.user_phone,
            birthday=self.user_birthday,
        )
        self.user.is_active = True
        self.user.is_approval = True
        self.user.set_password(self.user_password)
        self.user.save()

        # user2
        self.user2 = User(
            email=self.user2_email,
            nickname=self.user2_nickname,
            phone=self.user2_phone,
            birthday=self.user2_birthday,
        )
        self.user2.is_active = True
        self.user2.is_approval = True
        self.user2.set_password(self.user2_password)
        self.user2.save()

        # Request 생성
        # user1
        self.request = HttpRequest()
        self.request.user = self.user
        session = SessionStore()
        # SessionBase에서 session_key가 None이면
        # string.ascii_lowercase + string.digits로 session_key를 설정해준다.
        self.request.session = session

        # user2
        self.request2 = HttpRequest()
        self.request2.user = self.user2
        session2 = SessionStore()
        self.request2.session = session2
