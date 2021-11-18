import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from uuid import uuid4
from apps.models.alliance.models import Restaurant


def get_user_photo_path(instance, filename):
    """사용자 프로필 이미지"""
    url = 'user_photo'
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()

    return '/'.join([url, ymd_path, uuid_name + extension])


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, phone, birthday, password=None):
        if not email:
            raise ValueError('no user email address.')
        if not nickname:
            raise ValueError('please enter a nickname.')
        if not phone:
            raise ValueError("I don't have a cell phone number.")

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            phone=phone,
            birthday='2000-01-01',
            is_active=True,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            nickname='관리자(닉네임 변경해주세요.)' if kwargs.get('nickname') else '관리자(닉네임 변경해주세요)',
            birthday=None if kwargs.get('birthday') else None,
            phone='0' if kwargs.get('phone') else '0',
            password=password
        )
        user.is_active = True
        user.is_admin = True

        return user


class User(AbstractBaseUser):
    """사용자"""
    GENERAL, SILVER, GOLD, VIP = 0, 1, 2, 3
    rating_choice = (
        (GENERAL, '일반'),
        (SILVER, '실버'),
        (GOLD, '골드'),
        (VIP, 'VIP'),
    )

    email = models.EmailField(verbose_name='이메일', max_length=255, unique=True)
    nickname = models.CharField(verbose_name='닉네임', max_length=50)
    phone = models.CharField(verbose_name='휴대폰', max_length=20)
    birthday = models.DateField(verbose_name='생년월일')
    rating = models.IntegerField(verbose_name='등급', choices=rating_choice, default=0)
    photo = models.ImageField(verbose_name='프로필사진', upload_to=get_user_photo_path, blank=True)

    is_active = models.BooleanField(verbose_name='계정활성', default=True)
    is_approval = models.BooleanField(verbose_name='가입승인', default=False)
    is_owner = models.BooleanField(verbose_name='사장님', default=False)
    is_admin = models.BooleanField(verbose_name='관리자', default=False)
    is_withdrawal = models.BooleanField(verbose_name='탈퇴', default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_nickname(self):
        return self.nickname

    @property
    def is_staff(self):
        return self.is_admin

    # noinspection PyMethodMayBeStatic
    def has_perm(self, perm, obj=None):
        return True

    # noinspection PyMethodMayBeStatic
    def has_module_perms(self, app_label):
        return True


class ShoppingBasket(models.Model):
    """장바구니"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class UserDeliveryList(models.Model):
    """사용자 음식 배달 리스트"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
