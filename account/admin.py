from django.contrib import admin
from account.custom_user_form import CustomUserCreationForm, CustomUserChangeForm
from account.models import CustomUser, OTP, Profile, Skill
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class ProfileInline(admin.StackedInline):
    model = Profile


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    inlines = (ProfileInline,)

    list_display = ('email', 'phone', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('اطلاعات حساب کاربری', {'fields': ('email', 'phone', 'password')}),
        ('اطلاعات شخصی', {'fields': ('fname', 'lname',)}),
        ('دسترسی ها', {'fields': ('is_active', 'is_admin', 'is_teacher')}),
    )

    add_fieldsets = (
        ('اطلاعات حساب کاربری', {'fields': ('email', 'phone', 'password1', 'password2')}),
        ('اطلاعات شخصی', {'fields': ('fname', 'lname',)}),
        ('دسترسی ها', {'fields': ('is_active', 'is_admin', 'is_teacher')}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class OTPAdmin(BaseUserAdmin):
    list_display = ('email', 'code')
    list_filter = ('email',)

    fieldsets = (
        ('اطلاعات حساب کاربری', {'fields': ('email', 'code')}),
    )

    add_fieldsets = (
        ('اطلاعات حساب کاربری', {'fields': ('email', 'code')}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP, OTPAdmin)
admin.site.register(Skill)
admin.site.unregister(Group)
