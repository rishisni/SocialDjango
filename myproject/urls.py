
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('verify-email/<int:user_id>/', views.verify_email, name='verify_email'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    
    path('social-auth/facebook/', include('social_django.urls', namespace='facebook')),
    path('social-auth/google-oauth2/', include('social_django.urls', namespace='google')),
]
