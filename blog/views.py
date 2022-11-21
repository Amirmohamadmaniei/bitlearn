from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from blog.forms import CommentBlogForm
from blog.models import Blog, CommentBlog, Category


class BlogDetail(DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        context['form_comment'] = CommentBlogForm()
        context['another_blog'] = Blog.objects.filter().order_by('?')[0:3]
        return context


class BlogList(ListView):
    model = Blog
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['blog_category'] = Category.objects.all()
        return context


class BlogListSearch(ListView):
    model = Blog
    paginate_by = 6

    def get_queryset(self):
        return Blog.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogListSearch, self).get_context_data(**kwargs)
        context['blog_category'] = Category.objects.all()
        context['count_searched'] = Blog.objects.filter(title__icontains=self.request.GET.get('q')).count()
        return context


class BlogListFilter(ListView):
    model = Blog
    paginate_by = 6

    def get_queryset(self):
        f = self.request.GET.get('f')
        return Blog.objects.filter(category__title=f)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BlogListFilter, self).get_context_data(**kwargs)
        context['blog_category'] = Category.objects.all()
        return context


class AddCommentBlog(View):
    def get(self, requets, *args, **kwargs):
        return redirect(reverse('home:home'))

    def post(self, request, *args, **kwargs):
        form = CommentBlogForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            blog = Blog.objects.get(pk=request.POST.get('blog'))
            CommentBlog.objects.create(full_name=cd.get('full_name'),
                                       email=cd.get('email'),
                                       blog=blog,
                                       text=cd.get('text'),
                                       parent_id=request.POST.get('parent'))
            return redirect(blog.get_absolute_url())
