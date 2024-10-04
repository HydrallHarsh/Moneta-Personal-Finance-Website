from django.contrib import admin

from .models import Expense, Income,Budget

# Register your models here.
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Budget)