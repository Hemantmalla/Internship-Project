from django.contrib import admin
from .models import CustomUser, waiter, Reservation, SubCategory, MenuItem
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(waiter)
admin.site.register(Reservation)
admin.site.register(SubCategory)
admin.site.register(MenuItem)
