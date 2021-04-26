from django.contrib import admin

# Register your models here.
from .models import Product ,Contect,Orders, OrderUpdate

admin.site.register(Product)
admin.site.register(Contect)
admin.site.register(Orders)
admin.site.register(OrderUpdate)

