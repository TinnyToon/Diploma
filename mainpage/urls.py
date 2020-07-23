from django.urls import path, re_path
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.models import User
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    # path('accounts/register/', views.UserRegisterFormView.as_view()),
    path('accounts/register/', views.new_user_register, name='new-user-register'),
    path('accounts/register/check_user_exist', views.check_user_exist, name='check-user-exist'),
    re_path(r'^(?P<pk>\d+)$', views.delete_user, name="delete-user"),
    re_path(r'^(?P<pk>\d+)/change_profile/$', views.user_profile_change, name="user-profile-change"),
    re_path(r'^(?P<pk>\d+)/configs/$', views.check_user_configs, name="check-user-configs"),
]
