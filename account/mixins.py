from django.shortcuts import redirect
from django.urls import reverse


class NoLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('home:home'))
        return super(NoLoginRequiredMixin, self).dispatch(request, args, kwargs)


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse('home:home'))
        return super(LoginRequiredMixin, self).dispatch(request, args, kwargs)


class NoActiveMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('user_email') is None or request.user.is_active:
            return redirect(reverse('home:home'))
        return super(NoActiveMixin, self).dispatch(request, *args, **kwargs)



