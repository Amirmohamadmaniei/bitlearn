from django.shortcuts import redirect
from django.urls import reverse


class IsTeacher:
    def dispatch(self, request):
        if request.user.is_anonymous or not request.user.is_teacher:
            return redirect(reverse('home:home'))
        return super(IsTeacher, self).dispatch(request)
