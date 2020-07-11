"""feelings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from groups import urls as group_urls

#rest-framework
from rest_framework import routers
from thoughts.routers import router as thought_router

# from REST framework JWT (3d party package for create jwt token)
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

api_urlpatterns = [
    path('',include(thought_router.urls))
]
# вот сейчас непонятно: дублирование в рауте thought_router(see below)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('',TemplateView.as_view(template_name = 'index.html'),name='home'),
    path('thoughts/',include('thoughts.urls')),
    path('groups/',include(api_urlpatterns)),
    path('groups/',include(group_urls)),
]
urlpatterns += [
    path('api/v1/', include(thought_router.urls)), 
    path('api-token-auth/', obtain_jwt_token),  
    path('api-token-refresh/', refresh_jwt_token),     
    path('api-auth/', include('rest_framework.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    
]
# jwt  via postman
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNiwidXNlcm5hbWUiOiJmb3hkaWEyMDEzIiwiZXhwIjoxNTkwMDk1ODkxLCJlbWFpbCI6ImZveGRpYTIwMTNAeWFuZGV4LmNvbSJ9.t5UIc-9PrksaBrCBVbiamKCFEbnMeIWw-gd7oVK56Q0"
}


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    # urlpatterns += staticfiles_urlpatterns()
    urlpatterns += staticfiles_urlpatterns()
