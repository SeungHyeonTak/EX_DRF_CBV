from django.urls import path, include

app_name = 'apps'

urlpatterns = [
    path('api/v1/account/', include('apps.url.account.urls'))
]
