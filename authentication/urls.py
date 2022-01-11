
from django.urls import path
from .views import RegistrationView, UserenameValidationView,RequestPasswordResetEmail,CompletePasswordReset, EmailValidationView, EmailVerificationView, LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('validate-username', csrf_exempt(UserenameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('activate-account/<uidb64>/<token>', EmailVerificationView.as_view(), name='activate-account'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('request-password-reset-link', RequestPasswordResetEmail.as_view(), name='request-password-reset-link'),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='set-new-password'),
]