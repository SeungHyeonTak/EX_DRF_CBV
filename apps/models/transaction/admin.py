from django.contrib import admin
from .models import Payment, Coupon, CouponHistory, Point, PointHistory


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'price', 'payment_status', 'method_status', 'created_at')
    list_display_links = ('id',)
    raw_id_fields = ('user',)
    search_fields = ('user__email',)

    def get_user(self, obj):
        return obj.user.email

    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__email'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'valid_period_start', 'valid_period_end', 'is_used', 'is_expired', 'created_at')
    list_display_links = ('id',)
    raw_id_fields = ('user',)
    search_fields = ('user__email',)

    def get_user(self, obj):
        return obj.user.email

    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__email'


@admin.register(CouponHistory)
class CouponHistory(admin.ModelAdmin):
    list_display = ('id', 'get_coupon', 'get_restaurant', 'type', 'created_at',)
    list_display_links = ('id',)
    raw_id_fields = ('coupon', 'restaurant',)
    search_fields = ('coupon__title', 'restaurant__name')

    def get_coupon(self, obj):
        return obj.coupon.title

    def get_restaurant(self, obj):
        return obj.restaurant.name

    get_coupon.short_description = 'Coupon'
    get_coupon.admin_order_field = 'coupon__title'

    get_restaurant.short_description = 'Restaurant'
    get_restaurant.admin_order_field = 'restaurant__name'


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'created_at')
    list_display_links = ('id',)
    raw_id_fields = ('user',)
    search_fields = ('user__email',)

    def get_user(self, obj):
        return obj.user.email

    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__email'


@admin.register(PointHistory)
class PointHistory(admin.ModelAdmin):
    list_display = ('id', 'get_point', 'get_restaurant', 'type', 'created_at',)
    list_display_links = ('id',)
    raw_id_fields = ('point', 'restaurant',)
    search_fields = ('restaurant__name',)

    def get_point(self, obj):
        return obj.point

    def get_restaurant(self, obj):
        return obj.restaurant.name

    get_point.short_description = 'Point'
    get_point.admin_order_field = 'point'

    get_restaurant.short_description = 'Restaurant'
    get_restaurant.admin_order_field = 'restaurant__name'
