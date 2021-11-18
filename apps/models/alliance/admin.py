from django.contrib import admin
from .models import Category, Restaurant, MenuInformation, SalesInformation, EntrepreneurInformation, RestaurantLike, \
    Review, MenuCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_category',
        'name',
        'min_price',
        'delivery_time',
        'delivery_tip',
        'paid_service',
        'is_active'
    )
    list_display_links = ('name',)
    raw_id_fields = ('category',)
    search_fields = ('name',)

    def get_category(self, obj):
        return obj.category.name

    get_category.short_description = 'Category'
    get_category.admin_order_field = 'category__name'


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_restaurant', 'name', 'created_at', 'updated_at')
    list_display_links = ('name',)
    raw_id_fields = ('restaurant',)
    search_fields = ('name',)

    def get_restaurant(self, obj):
        return obj.restaurant.name

    get_restaurant.short_description = 'Restaurant'
    get_restaurant.admin_order_field = 'restaurant__name'


@admin.register(MenuInformation)
class MenuInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_menu_category', 'name', 'created_at')
    list_display_links = ('name',)
    raw_id_fields = ('menu_category',)
    search_fields = ('name',)

    def get_menu_category(self, obj):
        return obj.menu_category

    get_menu_category.short_description = 'MenuCategory'
    get_menu_category.admin_order_field = 'menu_category'


@admin.register(SalesInformation)
class SalesInformationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_restaurant',
        'business_name',
        'business_hours',
        'closed_day',
        'phone_number',
        'areas_interest',
        'created_at',
    )
    list_display_links = ('id', 'business_name',)
    raw_id_fields = ('restaurant',)
    search_fields = ('business_name',)

    def get_restaurant(self, obj):
        return obj.restaurant.name

    get_restaurant.short_description = 'Restaurant'
    get_restaurant.admin_order_field = 'restaurant__name'


@admin.register(EntrepreneurInformation)
class EntrepreneurInformationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_restaurant',
        'representative_name',
        'business_name',
        'business_address',
        'business_license_number',
        'created_at',
    )
    list_display_links = ('id', 'representative_name',)
    raw_id_fields = ('restaurant',)
    search_fields = ('representative_name',)

    def get_restaurant(self, obj):
        return obj.restaurant.name

    get_restaurant.short_description = 'Restaurant'
    get_restaurant.admin_order_field = 'restaurant__name'


@admin.register(RestaurantLike)
class RestaurantLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_restaurant', 'created_at',)
    list_display_links = ('id',)
    raw_id_fields = ('user', 'restaurant',)

    search_fields = ('user',)

    def get_user(self, obj):
        return obj.user.email

    def get_restaurant(self, obj):
        return obj.restaurant.name

    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__email'

    get_restaurant.short_description = 'Restaurant'
    get_restaurant.admin_order_field = 'restaurant__name'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'score', 'created_at',)
    list_display_links = ('id',)
    raw_id_fields = ('user',)
    search_fields = ('user__email',)

    def get_user(self, obj):
        return obj.user.email

    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__email'
