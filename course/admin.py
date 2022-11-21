from django.contrib import admin

from .models import Course, Headline, Video, Subscribe, Comment

admin.site.register(Course)
admin.site.register(Headline)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Subscribe)
