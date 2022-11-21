from django.urls import path
from .views import Login, Register, ChangePassword, ActiveAccount, ResendActiveCode, ForgetPassword, ForgetPasswordCode, \
    ResetPassword, ResendActiveCodeForgetPassword, Profile, Logout, EditProfile, AddSkill

app_name = 'account'

urlpatterns = [
    path('profile', Profile.as_view(), name='profile'),
    path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='Logout'),
    path('edit-profile', EditProfile.as_view(), name='edit_profile'),
    path('change-password', ChangePassword.as_view(), name='change_password'),
    path('forget-password', ForgetPassword.as_view(), name='forget_password'),
    path('forget-password-code', ForgetPasswordCode.as_view(), name='forget_password_code'),
    path('reset-password', ResetPassword.as_view(), name='reset_password'),
    path('verify-email', ActiveAccount.as_view(), name='active_account'),
    path('resend-activation-code', ResendActiveCode.as_view(), name='resend_activation_code'),
    path('resend-activation-code-forget-password', ResendActiveCodeForgetPassword.as_view(), name='resend_activation_code_forget_password'),
    path('add-skill', AddSkill.as_view(), name='add_skill')
]
