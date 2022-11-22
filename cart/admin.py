from django.contrib import admin
from cart.models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'total_price_with_discount',)
    search_fields = ('user',)


admin.site.register(Cart, CartAdmin)
