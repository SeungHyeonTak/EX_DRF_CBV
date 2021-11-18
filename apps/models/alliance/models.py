import os
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta
from uuid import uuid4


def get_announcement_photo_path(instance, filename):
    """음식점 공지사항 이미지"""
    url = 'announcement_photo'
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()

    return '/'.join([url, ymd_path, uuid_name + extension])


def get_food_menu_photo_path(instance, filename):
    """메뉴 이미지"""
    url = 'food_menu_photo'
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()

    return '/'.join([url, ymd_path, uuid_name + extension])


def get_business_license_photo_path(instance, filename):
    """사업자등록증 사본 이미지"""
    url = 'business_license_photo'
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()

    return '/'.join([url, ymd_path, uuid_name + extension])


def get_review_photo_path(instance, filename):
    """리뷰 이미지"""
    url = 'review_photo'
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()

    return '/'.join([url, ymd_path, uuid_name + extension])


class Category(models.Model):
    """카테고리"""
    name = models.CharField(verbose_name='카테고리 이름', max_length=20)

    is_active = models.BooleanField(verbose_name='카테고리 활성', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    """음식점"""
    # 평균 별점은 여기서 함수로 작성하기
    ULTRA, BASIC, OPEN = 0, 1, 2
    paid_choice = (
        (ULTRA, '울트라콜'),
        (BASIC, '기본'),
        (OPEN, '오픈서비스'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='음식점 이름', max_length=50)
    lat = models.DecimalField(verbose_name='위도', max_digits=10, decimal_places=6, blank=True)
    lng = models.DecimalField(verbose_name='경도', max_digits=10, decimal_places=6, blank=True)
    min_price = models.CharField(verbose_name='최소주문금액', max_length=10)
    payment_method = models.CharField(verbose_name='결제방법', max_length=30)
    delivery_time = models.CharField(verbose_name='배달 시간', max_length=20)
    delivery_tip = models.CharField(verbose_name='배달 팁', max_length=10)
    information = models.TextField(verbose_name='정보', blank=True, null=True)
    country_origin = models.TextField(verbose_name='원산지', blank=True, null=True)
    announcement = models.TextField(verbose_name='공지사항', blank=True, null=True)
    announcement_photo = models.ImageField(
        verbose_name='공지사항 이미지',
        upload_to=get_announcement_photo_path,
        blank=True,
        null=True
    )
    paid_service = models.IntegerField(verbose_name='유료서비스', choices=paid_choice, default=1)

    is_active = models.BooleanField(verbose_name='가게 활성화', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_open_service(self):
        """가게 생성 후 일주일간 유료 서비스 무료 이용"""
        open_day = self.created_at
        last_paid = open_day + timedelta(days=7)
        if last_paid:
            self.paid_service = 2
        else:
            self.paid_service = 1
        return self.paid_service

    def __str__(self):
        return self.name


class MenuCategory(models.Model):
    """메뉴 카테고리"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='메뉴 카테고리', max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.restaurant}({self.name})'


class MenuInformation(models.Model):
    """메뉴 정보"""
    menu_category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='메뉴 이름', max_length=30)
    photo = models.ImageField(verbose_name='메뉴이미지', upload_to=get_food_menu_photo_path, blank=True)
    information = models.TextField(verbose_name='메뉴 소개')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class SalesInformation(models.Model):
    """영업 정보"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    business_name = models.CharField(verbose_name='상호명', max_length=30)
    business_hours = models.CharField(verbose_name='영업 시간', max_length=30)
    closed_day = models.CharField(verbose_name='휴무일', max_length=30)
    phone_number = models.CharField(verbose_name='전화번호', max_length=20)
    areas_interest = ArrayField(models.CharField(verbose_name='관심지역(4곳)', max_length=10), size=4, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.business_name


class EntrepreneurInformation(models.Model):
    """사업자 정보"""
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    representative_name = models.CharField(verbose_name='대표자 이름', max_length=10)
    business_license_photo = models.ImageField(verbose_name='사업자등록증(사본)', upload_to=get_business_license_photo_path)
    business_name = models.CharField(verbose_name='상호명', max_length=30)
    business_address = models.CharField(verbose_name='사업자 주소', max_length=50)
    business_license_number = models.CharField(verbose_name='사업자 등록 번호', max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_license_check(self):
        """사업자 등록증 이미지 확인 (이미지 파일인지 확인)"""
        return True if self.business_license_photo else False

    def __str__(self):
        return f'{self.representative_name}({self.business_name})'


class RestaurantLike(models.Model):
    """찜(좋아요)"""
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='like_users')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='like_restaurants')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Review(models.Model):
    """리뷰"""
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    food_photo = models.ImageField(verbose_name='음식 사진', upload_to=get_review_photo_path, blank=True)
    score = models.IntegerField(
        verbose_name='평점',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='1~5점 사이로 입력해주세요.'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
