from django.urls import path, re_path
from course.views import CourseDetail, CourseList, AddHeadline, AddCourse, AddVideo, AddComment, AddSubscribe, \
    CourseListFilter, CourseListSort, SearchList, CategoryList

app_name = 'course'

urlpatterns = [
    path('list', CourseList.as_view(), name='list'),
    path('filter/', CourseListFilter.as_view(), name='list_filter'),
    path('sort', CourseListSort.as_view(), name='list_sort'),
    path('search/', SearchList.as_view(), name='search'),
    path('category', CategoryList.as_view(), name='category'),
    re_path(r'detail/(?P<slug>[-\w]+)/', CourseDetail.as_view(), name='detail'),
    path('add-course', AddCourse.as_view(), name='add_course'),
    path('add-headline', AddHeadline.as_view(), name='add_headline'),
    path('add-video', AddVideo.as_view(), name='add_video'),
    path('add-comment', AddComment.as_view(), name='add_comment'),
    path('add-subscribe', AddSubscribe.as_view(), name='add_subscribe'),
]
