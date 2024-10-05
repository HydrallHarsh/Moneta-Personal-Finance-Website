# signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from .models import Expense, Budget
from django.db import models
import requests,random
import os
import os
from dotenv import load_dotenv
# @receiver(post_save, sender=User)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created:  # Only send email on user creation
#         subject = 'Welcome to Finance Tracker!'
#         message = f'Hi {instance.username},\n\nThanks for registering on Finance Tracker! We’re excited to have you on board.'
#         from_email = settings.DEFAULT_FROM_EMAIL
#         recipient_list = [instance.email]
        
#         send_mail(subject, message, from_email, recipient_list)


def get_quote():
    # Request a quote from the API
    import requests
    category = 'money'  # Change this to 'saving' or 'money' if you want specific quotes
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    
    response = requests.get(api_url, headers={'X-Api-Key': os.getenv("API_KEY")})
    
    if response.status_code == requests.codes.ok:
        data = response.json()  # Extract JSON data from the response
        if data:  # Check if there are any quotes returned
            return data[0]['quote']  # Return the first quote
        else:
            return "Stay motivated with your savings!"  # Fallback message if no quote is found
    else:
        return "Error fetching quote."  # Fallback message if the API call fails


@receiver(post_save, sender=Expense)
def check_budget_exceeded(sender, instance, **kwargs):
    quote = get_quote()
    user = instance.user
    total_expenses = Expense.objects.filter(user=user, date__month=instance.date.month).aggregate(total=models.Sum('amount'))['total'] or 0
    latest_expense = Expense.objects.filter(user=user,date__month = instance.date.month).latest('date')
    latest_expense_description = latest_expense.description
    budget = Budget.objects.filter(user=user, month__month=instance.date.month).first()
    
    email_body = email_body = (
        f'Hello {user.username},\n\n'
        f'You have exceeded your budget for {budget.month.strftime("%B %Y")}, 2024. Your total spending is now {total_expenses}, '
        f'which exceeds your set budget of {budget.amount}.\n\n'
        f'Your latest expense was {latest_expense_description} on {latest_expense.date}. Please review your expenses.\n\n'
        f'Here\'s a quote for you: "{quote}"\n\n'
        f'Best regards,\nMoneta Tracker Team'
    )
    if budget and total_expenses > budget.amount:
        # Send notification email
        send_mail(
            'Budget Exceeded Notification',
            email_body,
            'your-email@gmail.com',  # From email

            [user.email],            # To email
            fail_silently=False,
        )