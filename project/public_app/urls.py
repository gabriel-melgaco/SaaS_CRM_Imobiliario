from public_app.views import index
from django.urls import path
from django.contrib import admin
from public_app.views import LoginView, RegisterView, RegisterClientView, logout_view, ActivationView, PasswordResetView, PasswordResetConfirmView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register_client/', RegisterClientView.as_view(), name='register_client'),
    path('logout/', logout_view, name="logout"),
    path('login/', LoginView.as_view(), name='login'),
    path('activation/<int:user_id>/', ActivationView.as_view(), name='activation'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<str:token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]