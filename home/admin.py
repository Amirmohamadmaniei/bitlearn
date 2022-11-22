from django.contrib import admin
from home.models import Ticket, Teach, ContactUs


class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject',)


class TeachAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'category',)
    list_filter = ('category',)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email',)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Teach, TeachAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
