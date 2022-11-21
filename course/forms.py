from django import forms
from django.core.exceptions import ValidationError

from course.choices import level_choices, category_choices
from course.models import Course, Headline, Video, Comment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            'title', 'description', 'level', 'price', 'discount', 'introduction_video', 'image', 'free', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان دوره را وارد کنید'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'توضیخات دوره را شرح دهید'}),
            'level': forms.Select(attrs={'class': 'form-control', 'placeholder': 'سطح دوره را مشخص کنید'},
                                  choices=level_choices),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'دسته بهندی دوره را مشخص کنید'},
                                     choices=category_choices),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'قیمت دوره (تومان)'}),
            'discount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'میزان درصد را وارد کنید'}),
            'introduction_video': forms.FileInput(
                attrs={'class': 'custom-file-input', 'id': 'customFile2', 'placeholder': 'ویدئوی معرفی دوره'}),
            'image': forms.FileInput(
                attrs={'class': 'custom-file-input', 'id': 'customFile3', 'placeholder': 'عکس معرفی دوره'}),
            'free': forms.CheckboxInput(attrs={'class': 'form-control', 'id': 'free-checkbox'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Course.objects.filter(title=title).exists():
            raise ValidationError('نام دوره تکراری است')
        return title


class HeadlineForm(forms.ModelForm):
    class Meta:
        model = Headline
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان سرفصل'}),
        }


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'video')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان ویدئو'}),
            'video': forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'customFile4', 'placeholder': 'ویدئو'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('full_name', 'email', 'text',)
        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-control rounded-pill', 'placeholder': 'نام خود را وارد کنید ...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill', 'id': 'customFile4',
                                             'placeholder': 'ایمیل خود را وارد کنید ...'}),
            'text': forms.Textarea(attrs={'class': 'form-control w-100 rounded-lg p-3', 'rows': '10', 'cols': '30',
                                          'placeholder': 'دیدگاه خود را وارد کنید ...'}),
        }
