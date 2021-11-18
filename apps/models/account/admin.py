from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        """암호 확인"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("password don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """사용자 업데이트를 위한 양식"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm

    list_display = ('id', 'email', 'nickname', 'rating', 'is_active', 'is_approval', 'is_admin')
    list_filter = ('is_active', 'is_admin')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Information', {'fields': ('nickname', 'phone', 'birthday', 'rating', 'photo')}),
        ('Permissions', {'fields': ('is_active', 'is_approval', 'is_admin', 'is_owner', 'is_withdrawal')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'birthday', 'phone', 'is_active'),
        }),
    )
    search_fields = ('email',),
    ordering = ('-created_at',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
