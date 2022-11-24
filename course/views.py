from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from course.forms import HeadlineForm, CourseForm, VideoForm, CommentForm
from course.mixins import IsTeacher
from course.models import Course, Headline, Video, Subscribe, Comment


class CourseList(ListView):
    model = Course
    queryset = Course.objects.filter(publish=True)
    paginate_by = 4


class CourseListSort(ListView):
    model = Course
    paginate_by = 4

    def get_queryset(self):
        s = self.request.GET.get('s')
        if s:
            return Course.objects.filter(publish=True).order_by(s)
        else:
            return Course.objects.filter(publish=True)


class CourseListFilter(ListView):
    model = Course
    paginate_by = 4

    def get_queryset(self):
        f = self.request.GET.get('f')
        if f == 'all':
            return Course.objects.filter(publish=True)
        return Course.objects.filter(publish=True, free=f)


class SearchList(ListView):
    model = Course
    paginate_by = 4
    template_name = 'course/search_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Course.objects.filter(publish=True, title__icontains=q)

    def get_context_data(self, *args, object_list=None, **kwargs):
        q = self.request.GET.get('q')
        context = super(SearchList, self).get_context_data(*args, **kwargs)
        context['count_searched'] = Course.objects.filter(title__icontains=q).count()
        return context


class CategoryList(ListView):
    model = Course
    paginate_by = 4
    template_name = 'course/course_list.html'

    def get_queryset(self):
        return Course.objects.filter(publish=True, category=self.request.GET.get('c'))


class CourseDetail(DetailView):
    model = Course
    queryset = Course.objects.filter(publish=True)

    def get_context_data(self, **kwargs):
        context = super(CourseDetail, self).get_context_data(**kwargs)
        context['form_headline'] = HeadlineForm()
        context['form_video'] = VideoForm()
        context['form_comment'] = CommentForm()
        context['suggest_course'] = Course.objects.filter(publish=True).order_by('?')[0:3]
        if self.request.user.is_authenticated:
            context['is_subscribe'] = Subscribe.objects.filter(course=self.object, student=self.request.user)
        return context


# Add Course For Teacher #
class AddCourse(IsTeacher, View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('home:home'))

    def post(self, request, *args, **kwargs):
        form_add_course = CourseForm(request.POST, request.FILES)
        if form_add_course.is_valid():
            cd = form_add_course.cleaned_data
            Course.objects.create(teacher_id=request.user.profile.pk, title=cd.get('title'),
                                  description=cd.get('description'),
                                  level=cd.get('level'), price=cd.get('price'), discount=cd.get('discount'),
                                  introduction_video=cd.get('introduction_video'),
                                  image=cd.get('image'),
                                  free=cd.get('free'),
                                  category=cd.get('category'))
            messages.success(request, 'دوره با موفقیت اضافه شد ، بعد از تایید منتشر خواهد شد', extra_tags='success')
        return redirect(reverse('account:profile'))


class AddHeadline(IsTeacher, View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('home:home'))

    def post(self, request, *args, **kwargs):
        form_headline = HeadlineForm(request.POST or None)
        course = Course.objects.get(pk=request.GET.get('course'))
        if form_headline.is_valid():
            Headline.objects.create(course=course, title=form_headline.cleaned_data.get('title'))

        return redirect(course.get_absolute_url)


class AddVideo(IsTeacher, View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('home:home'))

    def post(self, request, *args, **kwargs):
        form_video = VideoForm(request.POST or None, request.FILES)
        course = Course.objects.get(pk=request.GET.get('course'))
        headline = Headline.objects.get(pk=request.GET.get('headline'))
        if form_video.is_valid():
            Video.objects.create(title=form_video.cleaned_data.get('title'),
                                 video=form_video.cleaned_data.get('video'),
                                 course_id=course.id, headline_id=headline.id)
        return redirect(course.get_absolute_url)


class AddComment(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('home:home'))

    def post(self, request, *args, **kwargs):
        form_comment = CommentForm(request.POST or None)

        if form_comment.is_valid():
            cd = form_comment.cleaned_data
            course = Course.objects.get(pk=request.POST.get('course'))
            Comment.objects.create(full_name=cd.get('full_name'),
                                   email=cd.get('email'),
                                   text=cd.get('text'),
                                   course=course,
                                   parent_id=request.POST.get('parent'))
            return redirect(course.get_absolute_url)


class AddSubscribe(View):
    def get(self, request, *args, **kwargs):
        course = Course.objects.get(pk=request.GET.get('course'))
        Subscribe.objects.create(student=request.user, course=course)
        return redirect(course.get_absolute_url)
