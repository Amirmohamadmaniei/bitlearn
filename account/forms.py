from django import forms
from django.core.exceptions import ValidationError
from account.models import CustomUser, OTP, Profile, Skill


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری خود را وارد کنید'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور خود را وارد کنید'}))


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'رمز عبور خود را تکرار کنید'}))

    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'شماره تلفن خود را وارد کنید'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'ایمیل خود را وارد کنید'}),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control mb-2', 'placeholder': 'رمز عبور خود را وارد کنید'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            CustomUser.object.get(email=email)
            raise ValidationError('ایمیل قبلا ثبت شده است')
        except CustomUser.DoesNotExist:
            return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone.isdigit():
            raise ValidationError('شماره تلفن باید عددی باشد')

        if len(phone) != 11:
            raise ValidationError('شماره تلفن باید 11 رقم باشد')

        if not phone.startswith('09'):
            raise ValidationError('شماره تلفن باید با 09 شروع شود')

        try:
            CustomUser.object.get(phone=phone)
            raise ValidationError('شماره تلفن قبلا ثبت شده است')
        except CustomUser.DoesNotExist:
            return phone

    def clean_password(self):
        if len(self.cleaned_data.get('password')) < 8:
            raise ValidationError('رمز عبور یاید از 8 کارکتر بیشتر باشد')
        return self.cleaned_data.get('password')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('رمز عبور یکسان نیست')

        return password2


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز قدیمی خود را وارد کنید'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز جدید خود را وارد کنید'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز جدید خود را تکرار کنید'}))

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('کلمه غبور باید از 8 حرف بیشتر باشد')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('کلمه های عبور یکسان نیستند')
        return password2


class ForgetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'کد تایید برای ایمیل شما ارسال خواهد شد'}))


class OTPForm(forms.ModelForm):
    class Meta:
        model = OTP
        fields = ('code',)
        widgets = {
            'code': forms.TextInput(
                attrs={'class': 'form-control mb-2', 'placeholder': 'کد به ایمیل شما ارسال شده است'}),
        }


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز جدید خود را وارد کنید'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز جدید خود را تکرار کنید'}))

    def clean_password1(self):
        if len(self.cleaned_data.get('password1')) < 8:
            raise ValidationError('رمز عبور یاید از 8 کارکتر بیشتر باشد')
        return self.cleaned_data.get('password1')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('رمز عبور یکسان نیست')

        return password2


class ProfileForm(forms.ModelForm):
    email = forms.CharField(disabled=True, widget=forms.EmailInput(attrs={'class': 'form-control'}), )
    phone = forms.CharField(disabled=True, widget=forms.EmailInput(attrs={'class': 'form-control'}), )

    class Meta:
        model = CustomUser
        fields = ('fname', 'lname', 'phone', 'email')
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خود را وارد کنید'}),
            'lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوداگی خود را وارد کنید'}),
        }


class ProfileTeacherForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'grade', 'description', 'major', 'university')
        widgets = {
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مدرک تحصیلی خوذ را وارد کنید'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'بیوگرافی خود را وارد کنید'}),
            'major': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رشته تحصیلی خود را وارد کنید'}),
            'university': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'دانشگاه خود را وارد کنید'}),
            'image': forms.FileInput(
                attrs={'class': 'custom-file-input', 'id': 'customFile', 'placeholder': 'عکس خود را وارد کنید'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('title', 'percentage')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مهارت'}),
            'percentage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'درصد مهارت'}),
        }
