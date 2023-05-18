"""socialapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from social_core.backends.github import GithubOAuth2
from social_core.backends.google import GoogleOAuth2
from social_core.backends.facebook import FacebookOAuth2, FacebookAppOAuth2
from oauth2_provider.views import AuthorizationView
from blog.views import user_login
from socialapp import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view, name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    #   (r'^auth/', include('rest_framework_social_oauth2.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
