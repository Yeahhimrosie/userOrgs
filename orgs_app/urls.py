from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('user/create', views.create_user),
    path('user/login', views.login),
    path('logout', views.logout),
    path('groups', views.main_page),
    path('create/org', views.create_org),
    path('groups/<int:org_id>', views.details),
    path('join/<int:org_id>', views.join),
    path('leave/<int:org_id>', views.leave),
    path('groups/delete/<int:org_id>', views.delete_org),
]