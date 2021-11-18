from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from apps.views.account import SigninViewSet, SignoutViewSet

signin = SigninViewSet.as_view({'post': 'create'})
signout = SignoutViewSet.as_view({'post': 'update'})

urlpatterns = [
    path('token/', obtain_jwt_token),  # JWT 토큰 획득
    path('token/refresh/', refresh_jwt_token),  # JWT 토큰 갱신
    path('token/verify/', verify_jwt_token),  # JWT 토큰 확인
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
]
