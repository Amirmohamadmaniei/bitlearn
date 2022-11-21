from django.urls import path, re_path

from blog.views import BlogDetail, BlogList, AddCommentBlog, BlogListSearch, BlogListFilter

app_name = 'blog'

urlpatterns = [
    re_path(r'detail/(?P<slug>[-\w]+)/', BlogDetail.as_view(), name='detail'),
    path('list', BlogList.as_view(), name='list'),
    path('search/', BlogListSearch.as_view(), name='search'),
    path('filter/', BlogListFilter.as_view(), name='filter'),
    path('add-comment', AddCommentBlog.as_view(), name='add_comment'),
]
