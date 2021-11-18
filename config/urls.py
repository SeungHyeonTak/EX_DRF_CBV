import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.urls'))
]

# API docs information
schema_view = get_schema_view(
    openapi.Info(
        title='배달서비스 API 문서',
        default_version='v1',
        description=
        """
        배달 서비스
        
        작성자 : 탁승현
        """,
        terms_of_service='',
        contact=openapi.Contact(name='탁승현', email='conficker77@gmail.com'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=urlpatterns
)

# API 작성에 필요한 url 경로
urlpatterns += [
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
