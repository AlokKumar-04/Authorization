from django.urls import path
from django.contrib.auth import views as auth_views
from app.views import *

app_name = 'app'

urlpatterns = [
    path('', home, name='home'),
    path('SignUp', SignUp, name='SignUp'),
    path('SignIn/', SignIn, name='SignIn'),
    path('profile/', profile, name='profile'),
    path('SignOut/', SignOut, name='SignOut'),
    path('change-password/', change_password, name='change_password'),

    # Password Reset URLs
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt"
        ),
        name='password_reset'
    ),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
]
