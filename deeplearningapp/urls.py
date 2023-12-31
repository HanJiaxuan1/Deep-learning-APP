"""
URL configuration for deeplearningapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views, upload_model
# from django.conf.static import serve
from django.views.static import serve
from django.conf import settings
from django.urls import re_path

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}), # 用于处理static里的文件

    path('', views.home, name='index'),
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('home/', views.home),
    path('document/', views.document),
    path('login/', views.login, name='login'),
    path('RegisterCheck/', views.RegisterCheck, name='RegisterCheck'),
    path('LoginCheck/', views.LoginCheck, name='LoginCheck'),
    path('logout/', views.logout, name='logout'),
    path('use_model/', views.use),
    path('about/', views.about),
    path('signup/', views.signup),
    path('profile/', views.profile),
    path('model-detail/', views.model_detail),
    path('api-model-detail/', views.api_model_detail),
    path('model-upload/', upload_model.upload_model),
    path('model-add-db/', upload_model.add_model),
    path('deployment/', views.deployment),
    path('upload_model/', views.upload_model, name='upload_model'),
    path('modify_profile/', views.modify_profile),
    path('download_model/', views.download_model)
]
