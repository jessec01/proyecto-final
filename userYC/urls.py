from django.urls import path
from . import views

urlpatterns = [
    path("save-user/", views.SaveUserView.as_view(), name="save_user"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("404/", views.Error404View.as_view(), name="error_404"),
]
