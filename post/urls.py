from .views import RegisterAPI
from django.urls import path, include
from knox import views as knox_views
from .views import LoginAPI
from django.views.generic import TemplateView
from .views import ChangePasswordView
from . import views

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'), 
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # path('register/', RegistrationAPI.as_view()),
    path('', RegisterAPI.as_view(), name='program'),
    path('', RegisterAPI.as_view(), name='station'),
    # path('', RegisterAPI.as_view(), name='register'),
    path('index', views.index),
    path('home', views.home),
]

