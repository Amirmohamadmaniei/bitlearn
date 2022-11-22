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

    list_display = ('email', 'phone', 'is_admin', 'is_teacher', 'is_active')
    list_filter = ('is_admin', 'is_teacher', 'is_active')
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

    search_fields = ('email', 'phone', 'full_name')
    ordering = ('email', 'is_admin', 'is_teacher', 'is_active')
    filter_horizontal = ()
    search_help_text = 'جستجو در ایمیل ، شماره تلفن ، نام'


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


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('grade', )
    search_fields = ('user',)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')
    search_fields = ('user',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP, OTPAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(Group)
