from django.contrib import admin

from blog.models import Blog, Category, Tag, CommentBlog, IPAddress


class BlogAdmin(admin.ModelAdmin):
    list_display = ('image', 'author', 'category', 'title',)
    list_filter = ('category', 'tag')
    search_fields = ('title', 'author')
    search_help_text = 'جستجو در عنوان و نویسنده'


class CommentBlogAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'blog', 'parent',)
    list_filter = ('blog',)
    search_fields = ('text',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(CommentBlog, CommentBlogAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(IPAddress)
