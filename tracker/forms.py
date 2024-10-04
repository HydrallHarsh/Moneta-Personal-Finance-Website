from django import forms
from .models import Income, Expense
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import now

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
# Income Form
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['description','amount','date','source']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

# Expense Form
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description','amount','date','category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount', 'month']

    MONTH_CHOICES = [
        (1, "January"), (2, "February"), (3, "March"),
        (4, "April"), (5, "May"), (6, "June"),
        (7, "July"), (8, "August"), (9, "September"),
        (10, "October"), (11, "November"), (12, "December")
    ]

    # Add the month selection dropdown
    month = forms.ChoiceField(choices=MONTH_CHOICES)

    def clean(self):
        cleaned_data = super().clean()
        selected_month = int(cleaned_data.get('month'))
        current_year = now().year

        # Construct the full date using the first day of the selected month
        cleaned_data['month'] = datetime.date(current_year, selected_month, 1)

        return cleaned_data