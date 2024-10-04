from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Model for Income
class Income(models.Model):

    SOURCE_CHOICES = [
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('investments', 'Investments'),
        ('gifts', 'Gifts'),
        ('other', 'Other'),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=40,choices=SOURCE_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.source} - {self.amount}"

# Model for Expense
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('rent', 'Rent'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ]
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(default=now)

    

    def __str__(self):
        return f"{self.user.username}'s budget for {self.month.strftime('%B %Y')}"
    