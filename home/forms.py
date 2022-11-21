from django import forms

from course.choices import category_choices
from home.models import Ticket, Teach, ContactUs


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('created', 'user')
        widgets = {
            'subject': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': "عنوان مورد نظر خود را وارد کنید ..."}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'پیام خود را وارد کنید ...',
                                          'row': '3'}),
        }


class TeachForm(forms.ModelForm):
    class Meta:
        model = Teach
        exclude = ('created',)
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': "عنوان آموزش خود را وارد کنید"}),
            'full_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': "نام و نام خانوادگی خود را وارد کنید"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'پیام خود را وارد کنید ...',
                                                 'row': '3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "ایمیل خود را وارد کنید"}),
            'tel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "شماره خود را وارد کنید"}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': "لینک نمونه خود را وارد کنید"}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'دسته بندی را انتخاب کنید'},
                                     choices=category_choices),

        }


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('full_name', 'email', 'body')
        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-control rounded-pill', 'placeholder': "نام و نام خانوادگی خود را وارد کنید"}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control rounded-pill', 'placeholder': "ایمیل خود را وارد کنید"}),
            'body': forms.Textarea(
                attrs={'class': 'form-control w-100 rounded-lg p-3', 'placeholder': "ایمیل خود را وارد کنید",
                       'cols': "30", 'rows': "10"})

        }
