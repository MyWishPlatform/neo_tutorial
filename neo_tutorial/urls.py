"""neo_tutorial URL Configuration

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
from django.urls import path, re_path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from neo_tutorial.profile.views import portal_signup, portal_signup_activate


urlpatterns = [
    path('admin/', admin.site.urls)
]


urlpatterns += [
    path('administration/', include('neo_tutorial.administration.urls')),
    path('', include('neo_tutorial.portal.urls')),
    path('api/rest-auth/', include('rest_auth.urls')),
#    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/rest-auth/registration/', portal_signup),
    re_path(r'^api/rest-auth/registration/confirm-email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            portal_signup_activate, name='activate')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
