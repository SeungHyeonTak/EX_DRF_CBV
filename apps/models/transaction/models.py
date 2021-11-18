from django.db import models


class Point(models.Model):
    """포인트"""
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='points')
    point_amount = models.IntegerField(verbose_name='적립 포인트', default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user}({self.point_amount})'


class PointHistory(models.Model):
    """포인트 사용내역"""
    USE, CANCELLATION = 0, 1
    type_choice = (
        (USE, '사용'),
        (CANCELLATION, '취소'),
    )
    restaurant = models.ForeignKey('alliance.Restaurant', on_delete=models.CASCADE)  # 포인트를 사용한 가게
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    type = models.IntegerField(verbose_name='사용처리', choices=type_choice, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.point}({self.type})'


class Coupon(models.Model):
    """쿠폰"""
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='coupons')
    title = models.CharField(verbose_name='쿠폰 이름', max_length=50)
    discount_amount = models.IntegerField(verbose_name='할인 금액', default=0)
    valid_period_start = models.DateField(verbose_name='유효기간 시작일', blank=True, null=True)
    valid_period_end = models.DateField(verbose_name='유효기간 종료일', blank=True, null=True)
    is_used = models.BooleanField(verbose_name='쿠폰 사용 확인', default=False)
    is_expired = models.BooleanField(verbose_name='쿠폰 만료', default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title}'


class CouponHistory(models.Model):
    """쿠폰 사용내역"""
    USE, CANCELLATION = 0, 1
    type_choice = (
        (USE, '사용'),
        (CANCELLATION, '취소'),
    )
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='coupon_history')
    restaurant = models.ForeignKey('alliance.Restaurant', on_delete=models.CASCADE, related_name='rest_history')
    type = models.IntegerField(verbose_name='사용처리', choices=type_choice, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.coupon}({self.type})'


class Payment(models.Model):
    """결제"""
    # todo: 상황에 따라서 결제 요청 번호가 필요할 수 있음. (참고)
    REQUEST, CANCEL, FAIL, COMPLETE, REFUND_ALL = 0, 1, 2, 3, 4
    status_choice = (
        (REQUEST, '결제 요청'),
        (CANCEL, '결제 취소'),
        (FAIL, '결제 실패'),
        (COMPLETE, '결제 완료'),
        (REFUND_ALL, '전체 환불'),
    )
    IMMEDIATELY_CARD, MEET_CARD, CASH = 0, 1, 2
    method_choice = (
        (IMMEDIATELY_CARD, '즉시 결제'),
        (MEET_CARD, '만나서 결제'),
        (CASH, '현금 결제'),
    )

    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='user_payment')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True, related_name='coupon_payment')
    point = models.ForeignKey(Point, on_delete=models.CASCADE, blank=True, null=True, related_name='point_payment')
    _price = models.IntegerField(verbose_name='결제액', default=0)
    payment_status = models.IntegerField(verbose_name='결제상태', choices=status_choice, default=0)
    method_status = models.IntegerField(verbose_name='결제수단', choices=method_choice, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def price(self):
        if self.coupon and not self.point:
            return self._price - self.coupon.discount_amount

        if self.point and not self.coupon:
            return self._price - self.point.point_amount

        if self.point and self.coupon:
            return self._price - self.point.point_amount - self.coupon.discount_amount
        else:
            return self._price

    @price.setter
    def price(self, price):
        self._price = price

    def __str__(self):
        return f'{self.price}({self.payment_status})-{self.method_status}'
