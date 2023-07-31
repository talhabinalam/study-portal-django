from django.contrib import admin
from django.urls import path, include
from app import views as app_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('register/', app_views.register, name='register'),
    path('login/', app_views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/logout.html'), name='logout'),
    path('profile/', app_views.profile, name='profile'),
]
