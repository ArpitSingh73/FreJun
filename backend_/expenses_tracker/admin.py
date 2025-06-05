from django.contrib import admin

# Register your models here.
from .models import UserModel, Expense

admin.site.register(UserModel)
admin.site.register(Expense)