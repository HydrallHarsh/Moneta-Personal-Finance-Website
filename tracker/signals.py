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
import json
from dotenv import load_dotenv
load_dotenv()
# @receiver(post_save, sender=User)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created:  # Only send email on user creation
#         subject = 'Welcome to Finance Tracker!'
#         message = f'Hi {instance.username},\n\nThanks for registering on Finance Tracker! We’re excited to have you on board.'
#         from_email = settings.DEFAULT_FROM_EMAIL
#         recipient_list = [instance.email]
        
#         send_mail(subject, message, from_email, recipient_list)


def get_quote():
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer " + os.getenv("OPENROUTER_API_KEY"),
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "nvidia/nemotron-3-super-120b-a12b:free",
        "messages": [
            {
            "role": "user",
            "content": "You are acting as a financial advisor. Provide a motivational quote related to saving money and budgeting to encourage users to stay on track with their financial goals. Your message should be concise, inspiring, and relevant to personal finance management. Please provide only the quote without any additional commentary or explanation. Your message will be sent to users who have exceeded their budget to help motivate them to stay on track with their financial goals.Add noting else except the quote in your response.Make sure the quote is concise and inspiring, and directly related to saving money and budgeting.Try to make it unique and not a commonly known quote. Avoid using quotes from famous individuals or generic sayings. Instead, create an original quote that resonates with the challenges and rewards of managing personal finances effectively. You can make it a bit humorous or light-hearted to help users feel encouraged rather than discouraged about their financial situation. Remember, the goal is to motivate users to take positive action towards their financial goals, so the quote should be uplifting and empowering."
            }
        ],
        "reasoning": {"enabled": True}
        })
    )
    if response.status_code == requests.codes.ok:
        data = response.json()  # Extract JSON data from the response
        if data['choices']:  # Check if there are any quotes returned
            return data['choices'][0]['message']['content']  # Return the first quote
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