from datetime import datetime, timedelta
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, View
from django.contrib import messages
from account.forms import LoginForm, RegisterForm, ChangePasswordForm, OTPForm, ResetPasswordForm, ForgetPasswordForm, \
    ProfileForm, ProfileTeacherForm, SkillForm
from account.models import CustomUser, OTP, Skill
from course.forms import CourseForm
from course.mixins import IsTeacher
from course.models import Course
from home.forms import TicketForm
from .mixins import NoLoginRequiredMixin, NoActiveMixin, LoginRequiredMixin
from .send_email import send_email


# Register User #
class Register(NoLoginRequiredMixin, FormView):
    template_name = 'account/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('account:active_account')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        password = form.cleaned_data.get('password')
        user = CustomUser.object.create_user(email=email, phone=phone)
        user.set_password(password)
        user.save()
        self.request.session['user_email'] = email
        send_email(user, email)

        return super(Register, self).form_valid(form)


# Activate Account or Verify Email #
class ActiveAccount(NoActiveMixin, View):
    def get(self, request, *args, **kwargs):
        form = OTPForm()
        return render(request, 'account/otp.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = OTPForm(request.POST or None)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            email = self.request.session['user_email']
            if OTP.objects.filter(code=code, email=email).exists():
                now = datetime.now()
                otp = OTP.objects.filter(code=code, email=email)[0]
                revoke = now - otp.expiration
                if revoke >= timedelta(minutes=2):
                    form.add_error('code', 'کد باطل شده است')
                    return render(request, 'account/otp.html', {'form': form})
                else:
                    user = CustomUser.object.get(email=email)
                    user.is_active = True
                    user.save()
                    otp.delete()
                    login(self.request, user)
            else:
                form.add_error('code', 'کد تایید اشتباه است')
                return render(request, 'account/otp.html', {'form': form})

        return redirect(reverse('home:home'))


# Resend Active Code For Active Account #
class ResendActiveCode(NoActiveMixin, View):
    def get(self, request, *args, **kwargs):
        email = self.request.session['user_email']
        user = CustomUser.object.get(email=email)
        send_email(user, email)
        return redirect(reverse('account:active_account'))


# Login User #
class Login(NoLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = CustomUser.object.filter(phone=username).exists() or CustomUser.object.filter(
                email=username).exists()

            if user is False:
                form.add_error('username', 'نام کاربری ثبت نشده است')
                return render(request, 'account/login.html', {'form': form})

            user = authenticate(request, username=username, password=password)

            if user is None:
                form.add_error('password', 'رمز عبور اشتباه است')
                return render(request, 'account/login.html', {'form': form})

            if user.is_active is False:
                try:
                    email = CustomUser.object.get(email=username).email
                except CustomUser.DoesNotExist:
                    email = CustomUser.object.get(phone=username).email
                user = CustomUser.object.get(email=email)
                request.session['user_email'] = email
                send_email(user, email)
                return redirect(reverse('account:active_account'))
            login(request, user)

        return redirect(reverse('home:home'))


# Forget Password #
class ForgetPassword(NoLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ForgetPasswordForm()
        return render(request, 'account/forget_password.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ForgetPasswordForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user_exists = CustomUser.object.filter(Q(phone=username) | Q(email=username)).exists()
            if user_exists is True:
                try:
                    email = CustomUser.object.get(phone=username).email
                except CustomUser.DoesNotExist:
                    email = CustomUser.object.get(email=username).email
                request.session['user_email'] = email
                user = CustomUser.object.get(email=email)
                send_email(user, email)
            else:
                form.add_error('username', 'نام کاربری شما در سیستم ثبت نشده است')
                return render(request, 'account/forget_password.html', {'form': form})

            return redirect(reverse('account:forget_password_code'))


# Code For ForgetPassword #
class ForgetPasswordCode(NoLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = OTPForm()
        return render(request, 'account/otp_forget_password.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = OTPForm(request.POST or None)
        if form.is_valid():
            email = request.session.get('user_email')
            code = form.cleaned_data.get('code')

            try:
                otp = OTP.objects.filter(email=email, code=code)[0]
                now = datetime.now()
                revoke = now - otp.expiration
                if revoke <= timedelta(minutes=2):
                    otp.delete()
                    return redirect(reverse('account:reset_password'))
                else:
                    form.add_error('code', 'کد باطل شده است')
                    return render(request, 'account/otp_forget_password.html', {'form': form})
            except:
                form.add_error('code', 'کد اشتباه است')
                return render(request, 'account/otp_forget_password.html', {'form': form})


# Reset New Password #
class ResetPassword(NoLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ResetPasswordForm()
        return render(request, 'account/reset_password.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ResetPasswordForm(request.POST or None)
        if form.is_valid():
            email = request.session.get('user_email')
            password = form.cleaned_data.get('password1')
            user = CustomUser.object.get(email=email)
            user.set_password(password)
            user.save()
            return redirect(reverse('account:login'))
        return render(request, 'account/reset_password.html', {'form': form})


# Resend New Code For Forget Password #
class ResendActiveCodeForgetPassword(NoLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        email = self.request.session['user_email']
        user = CustomUser.object.get(email=email)
        send_email(user, email)
        return redirect(reverse('account:forget_password_code'))


# Change Password #
class ChangePassword(View):
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, 'account/change_password.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST or None)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            password1 = form.cleaned_data.get('password1')
            user = authenticate(username=request.user.email, password=old_password)
            if user is not None:
                user.set_password(password1)
                user.save()
                messages.success(request, 'رمز عبور با موفقیت تغییر کرد')
                login(request, user)
            else:
                form.add_error('old_password', 'رمز عبور اشتباه است')

        return render(request, 'account/change_password.html', {'form': form})


# Profile #
class Profile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ProfileForm(instance=request.user)
        form_ticket = TicketForm()
        count_course = Course.objects.filter(publish=True).count()
        if request.user.is_teacher:
            form_teacher = ProfileTeacherForm(instance=request.user.profile)
            form_add_course = CourseForm()
            form_skill = SkillForm()
            course_in_line = Course.objects.filter(teacher=request.user.profile, publish=False).count()
            return render(request, 'account/profile.html',
                          {'form': form, 'form_teacher': form_teacher,
                           'form_add_course': form_add_course, 'form_skill': form_skill,
                           'count_course': count_course, 'course_in_line': course_in_line,
                           'form_ticket': form_ticket
                           })
        return render(request, 'account/profile.html', {'form': form, 'count_course': count_course,
                                                        'form_ticket': form_ticket})


# Edit Profile #
class EditProfile(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('account:profile'))

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None, instance=request.user)
        if request.user.is_teacher:
            form_teacher = ProfileTeacherForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid() and form_teacher.is_valid():
                form.save()
                form_teacher.save()

        else:
            if form.is_valid():
                form.save()

        messages.success(request, 'پروفایل بروزرسانی شد')
        return redirect(reverse('account:profile'))


class AddSkill(IsTeacher, View):
    def get(self, request, *args, **kwargs):
        if Skill.objects.filter(user=request.user.profile).count() < 5:
            form_skill = SkillForm(request.GET or None)
            if form_skill.is_valid():
                Skill.objects.create(user=request.user.profile,
                                     title=form_skill.cleaned_data.get('title'),
                                     percentage=form_skill.cleaned_data.get('percentage'))
            messages.success(request, 'با موفقیت اضافه گردید')
        else:
            messages.warning(request, 'تعداد مهارت های شما کامل است')
        return redirect(reverse('account:profile'))


# Logout User #
class Logout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('home:home'))
