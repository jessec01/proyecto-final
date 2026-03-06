#userYC/urls.py

#importaciones de django
from django.urls import path

#importaciones de rest_framework
from rest_framework import routers

#importaciones internas
from . import views

routers = routers.DefaultRouter()
routers.register(r'users', views.UserYCViewSet, basename='user')
urlpatterns = [
    path("save-user/", views.SaveUserView.as_view(), name="save_user"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("404/", views.Error404View.as_view(), name="error_404"),
    path("user/", views.UserYCProfileTemplateView.as_view(), name="user"),
    path("user/<int:pk>/", views.UserYCViewSet.as_view({'get': 'retrieve'}), name="user_detail"),
    path("user/<int:pk>/update/", views.UserYCViewSet.as_view({'put': 'update'}), name="user_update"),
    path("user/<int:pk>/delete/", views.UserYCViewSet.as_view({'delete': 'destroy'}), name="user_delete"),
    path("user/<int:pk>/list/", views.UserYCViewSet.as_view({'get': 'list'}), name="user_list"),
    path("user/<int:pk>/create/", views.UserYCViewSet.as_view({'post': 'create'}), name="user_create"),
]
