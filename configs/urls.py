from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check_make', views.check_make, name='check_make'),
    path('check_model', views.check_model, name='check_model'),
    path('check_generation', views.check_generation, name='check_generation'),
    path('config/stage1/rate_stage1', views.rate_stage1, name='rate_stage1'),
    path('config/stage2/rate_stage2', views.rate_stage2, name='rate_stage2'),
    path('config/stage3/rate_stage3', views.rate_stage3, name='rate_stage3'),
    path('config/stage3plus/rate_stage3plus', views.rate_stage3plus, name='rate_stage3plus'),
    path('new_config/phase1/check_make', views.check_make, name='new_check_make'),
    path('new_config/phase1/check_model', views.check_model, name='new_check_model'),
    path('new_config/phase1/check_generation', views.check_generation, name='new_check_generation'),
    re_path(r'^new_config/phase1/(?P<pk>\d+)$', views.new_config_one, name="new-config-one"),
    re_path(r'^new_config/phase2/(?P<user_pk>\d+)/(?P<auto_pk>\d+)$', views.new_config_two, name="new-config-two"),
    re_path(r'^config/stage1/(?P<pk>\d+)$', views.check_stage1, name="check-stage1"),
    re_path(r'^config/stage2/(?P<pk>\d+)$', views.check_stage2, name="check-stage2"),
    re_path(r'^config/stage3/(?P<pk>\d+)$', views.check_stage3, name="check-stage3"),
    re_path(r'^config/stage3plus/(?P<pk>\d+)$', views.check_stage3plus, name="check-stage3plus"),
]
