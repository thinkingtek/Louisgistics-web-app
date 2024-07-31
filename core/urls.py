"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from account.views import *
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard, name='dashboard'),
    path('delete-inactive-users/', deleteInactiveUsers,
         name='delete-inactive-users'),
    path('signup/', register, name='signup'),
    path('login/', loginView, name='login'),
    path('logout/', userLogout, name='logout'),
    # path('logout/', UserLogoutView.as_view(), name='logout'),
    path('activate/<slug:uidb64>/<slug:token>)/', activate, name='activate'),

    path('password-change/', PasswordChange.as_view(),
         name='password-change'),
    path('password-reset/', ResetPassword.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         ResetPasswordConfirm.as_view(), name='password_reset_confirm'),

    path('password-reset-complete/', ResetPasswordComplete.as_view(),
         name='password-reset-complete'),

    path('', include('logistics.urls', namespace='logistics')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Louisgistic Xpress'
