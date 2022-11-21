from django.contrib import admin

from blog.models import Blog, Category, Tag, CommentBlog

admin.site.register(Blog)
admin.site.register(CommentBlog)
admin.site.register(Tag)
admin.site.register(Category)
