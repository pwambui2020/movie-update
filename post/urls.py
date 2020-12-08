from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI
from django.views.generic import TemplateView

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'), 
    
]

