from django import forms

from blog.models import CommentBlog


class CommentBlogForm(forms.ModelForm):
    class Meta:
        model = CommentBlog
        fields = ('full_name', 'text', 'email')
        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-control rounded-pill', 'placeholder': 'نام خود را وارد کنید ...'}),
            'text': forms.Textarea(attrs={'class': 'form-control w-100 rounded-lg p-3', 'cols': "30", 'rows': "10",
                                          'placeholder': 'دیدگاه خود را وارد کنید ...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill',
                                             'placeholder': 'ایمیل خود را وارد کنید ...'}),
        }
