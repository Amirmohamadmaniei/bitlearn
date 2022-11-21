from django.urls import path
from home.views import HomeView, ContactUsView, ReqTeach, SendTicket

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact-us', ContactUsView.as_view(), name='contact_us'),
    path('req-teach', ReqTeach.as_view(), name='req_teach'),
    path('send-ticket', SendTicket.as_view(), name='send_ticket'),
]
