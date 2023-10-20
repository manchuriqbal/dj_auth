from django.urls import path

from .views import (
    Home,
    Login,
    Logout,
    Registation
)

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('registation/', Registation.as_view(), name="registation"),
]
