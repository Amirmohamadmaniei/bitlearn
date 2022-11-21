from django.http import JsonResponse
from account.mixins import LoginRequiredMixin
from cart.models import Cart
from course.models import Course
from django.views import View


class AddToCart(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        course = Course.objects.get(pk=request.GET.get('course'))
        try:
            cart = Cart.objects.get(user=request.user.id)
            cart.course.add(course)
            cart.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
            cart.course.add(course)
            cart.save()
        return JsonResponse({'response': 'added', 'count': cart.course.all().count()})


class RemoveFromCart(View):
    def get(self, request, *args, **kwargs):
        cart = request.user.cart
        cart.course.remove(Course.objects.get(pk=request.GET.get('course')))
        cart.save()
        return JsonResponse({'count_course': cart.course.all().count(),
                             'total_price': cart.total_price,
                             'total_price_with_discount': cart.total_price_with_discount})
