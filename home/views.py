from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, FormView
from account.mixins import LoginRequiredMixin
from account.models import Profile
from blog.models import Blog
from course.models import Course
from home.forms import TicketForm, TeachForm, ContactUsForm
from home.models import Ticket


class HomeView(View):
    def get(self, request, *args, **kwargs):
        newest_courses = Course.objects.filter(publish=True).order_by('-created')[0:6]
        soon_courses = Course.objects.filter(publish=True, status='soon').order_by('-created')[0:3]
        teachers = Profile.objects.all().order_by('?')[0:5]
        blogs = Blog.objects.all().order_by('-created')[0:3]
        return render(request, 'home/index.html', {'newest_courses': newest_courses,
                                                   'soon_courses': soon_courses,
                                                   'teachers': teachers,
                                                   'blogs': blogs})


class SendTicket(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect('/')

    def post(self, request, *args, **kwargs):
        form = TicketForm(request.POST or None)
        if form.is_valid():
            Ticket.objects.create(user_id=request.user.id,
                                  subject=form.cleaned_data.get('subject'),
                                  body=form.cleaned_data.get('body'))
            messages.success(request, 'تیکت با موفقیت ارسال شد')
        return redirect(reverse('account:profile'))


class ContactUsView(FormView):
    template_name = 'home/contact_us.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('home:contact_us')

    def form_valid(self, form):
        form.save()
        return super(ContactUsView, self).form_valid(form)


class ReqTeach(FormView):
    template_name = 'home/req_teach.html'
    form_class = TeachForm
    success_url = reverse_lazy('home:req_teach')

    def form_valid(self, form):
        form.save()
        return super(ReqTeach, self).form_valid(form)


def error_404(request, exception):
    return render(request, 'home/404.html')
