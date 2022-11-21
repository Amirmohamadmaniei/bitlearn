from django.db import models
from account.models import CustomUser
from course.models import Course


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    course = models.ManyToManyField(Course)
    total_price = models.IntegerField(default=0)
    total_price_with_discount = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.id:
            self.total_price_with_discount = 0
            self.total_price = 0
            for course in self.course.all():
                self.total_price_with_discount += course.price_with_discount
                self.total_price += course.price
        return super(Cart, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'
