from django.urls import path
from .views import logout_view, login_view , register, home

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'),
]