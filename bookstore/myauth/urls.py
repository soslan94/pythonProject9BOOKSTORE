from django.urls import path
from .views import login_view, RegisterView, logout_view, AboutMeView

app_name = 'myauth'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    ]

