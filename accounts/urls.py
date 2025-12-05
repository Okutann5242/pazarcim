from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("giris/", views.login_view, name="login"),
    path("kayit/", views.register_view, name="register"),
    path("panel/", views.dashboard, name="dashboard"),
    
]
