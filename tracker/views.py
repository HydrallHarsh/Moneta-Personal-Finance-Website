from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Income , Expense ,Budget
from django.db.models import Sum
from .forms import IncomeForm, ExpenseForm
from django.utils import timezone
import json,csv
import pandas as pd
from decimal import Decimal
from django.conf import settings
from django.core.mail import send_mail
from .forms import CustomUserCreationForm,BudgetForm
from openpyxl import Workbook


def home(request):
    context = {}
    if request.user.is_authenticated:
        context['greeting'] = f"Hello, {request.user.username}!"
    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to home page after successful login
    return render(request, 'login.html')

# views.py
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            auth_login(request, user)  # Automatically log in the user after registration

            try:
                # Send the welcome email
                subject = 'Welcome to Moneta - Finance Tracker!'
                message = f'Hi {user.username},\n\nThanks for registering on the website!'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user.email]

                send_mail(subject, message, from_email, recipient_list,fail_silently=False)
                # print(f"Number of successfully sent emails: {result}")
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            except Exception as e:
                # Print the error message in the terminal for debugging
                print(f"Error sending email: {e}")
                return HttpResponse('There was an error sending the email.')

            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    incomes = Income.objects.filter(user = request.user)
    expenses = Income.objects.filter(user = request.user)
    return render(request, 'profile.html',{'incomes' : incomes,'expenses' : expenses})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if(form.is_valid()):
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})

@login_required
def add_expense(request):
    if(request.method == 'POST'):
        form  = ExpenseForm(request.POST)
        if(form.is_valid()):
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            
            return redirect('dashboard')
        
    else:
        form = ExpenseForm()
    return render(request , 'add_expense.html' , {'form' : form})

@login_required
def dashboard(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    
    # Fetch income and expense data for each month (for the yearly view)
    monthly_data = []
    months = []
    net_savings = []
    
    for month in range(1, 13):  # Loop through each month of the year
        monthly_expenses = Expense.objects.filter(user=request.user, date__month=month, date__year=current_year)
        monthly_incomes = Income.objects.filter(user=request.user, date__month=month, date__year=current_year)
        
        # Aggregate the sum of amounts for expenses and incomes
        monthly_expense_sum = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_income_sum = monthly_incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Calculate net savings for the month
        net = monthly_income_sum - monthly_expense_sum
        
        # Convert to float for JSON serialization
        net_savings.append(float(net))
        
        # Append month name
        month_name = timezone.datetime(current_year, month, 1).strftime('%B')
        months.append(month_name)
        
        # Append income and expense details to monthly_data
        monthly_data.append({
            'month': month_name,
            'income': monthly_income_sum,
            'expense': monthly_expense_sum,
            'net': net,
            'monthly_income_sources': monthly_incomes,  # Pass detailed income sources
            'expenses': monthly_expenses  # Pass detailed expenses
        })

    # Check if the user has exceeded their budget for the current month
    budget_exceeded, total_expenses, budget_amount = check_budget_status(request.user, current_month, current_year)

    # If the budget is exceeded, show a warning message
    if budget_exceeded:
        messages.warning(request, f"Your expenses are approaching your budget limit. Consider reviewing your spending habits. Total Expenses: {total_expenses} ,  Budget: {budget_amount}")

    # Fetch current month's income and expense data for the charts
    current_month_incomes = Income.objects.filter(user=request.user, date__month=current_month, date__year=current_year)
    current_month_expenses = Expense.objects.filter(user=request.user, date__month=current_month, date__year=current_year)

    # Aggregate the sum of amounts for the current month's incomes and expenses
    current_month_income_sum = current_month_incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    current_month_expense_sum = current_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Get detailed income and expense sources and amounts for the current month
    # Aggregate incomes by source for the current month
    income_data = current_month_incomes.values('source').annotate(total_amount=Sum('amount'))
    income_sources = [data['source'] for data in income_data]
    income_source_amounts = [float(data['total_amount']) for data in income_data]

    
   # Aggregate expenses by category for the current month
    expense_data = current_month_expenses.values('category').annotate(total_amount=Sum('amount'))
    expense_sources = [data['category'] for data in expense_data]
    expense_source_amounts = [float(data['total_amount']) for data in expense_data]

    # Existing data aggregation for the whole year
    total_income = Income.objects.filter(user=request.user, date__year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Expense.objects.filter(user=request.user, date__year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'monthly_data': monthly_data,
        'curr_year' : current_year,
        'income_sources': json.dumps(income_sources),  # Current month income sources
        'income_source_amounts': json.dumps(income_source_amounts),  # Current month income amounts
        'expense_sources': json.dumps(expense_sources),  # Current month expense categories
        'expense_source_amounts': json.dumps(expense_source_amounts),  # Current month expense amounts
        'total_income': float(total_income),
        'total_expense': float(total_expense),
        'months': json.dumps(months),
        'net_savings': json.dumps(net_savings),
        'current_month': timezone.datetime(current_year, current_month, 1).strftime('%B'),
        'current_month_income_sum': float(current_month_income_sum),
        'current_month_expense_sum': float(current_month_expense_sum),
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            # Extract form data
            amount = form.cleaned_data['amount']
            selected_month = form.cleaned_data['month']

            # Get the year and month from the selected_month
            selected_year = selected_month.year
            selected_month_number = selected_month.month

            # Check if a budget already exists for the user in the selected month
            existing_budget = Budget.objects.filter(
                user=request.user,
                month__year=selected_year,
                month__month=selected_month_number
            ).first()

            if existing_budget:
                # If budget exists, update it with new amount
                existing_budget.amount = amount
                existing_budget.save()
            else:
                # Create a new budget if one doesn't exist
                new_budget = Budget(
                    user=request.user,
                    amount=amount,
                    month=selected_month
                )
                new_budget.save()

            return redirect('dashboard')  # Redirect to a suitable page after saving
    else:
        form = BudgetForm()

    return render(request, 'set_budget.html', {'form': form})


def check_budget_status(user, current_month, current_year):
    try:
        # Correct reference: directly use the user argument passed
        budget = Budget.objects.get(user=user, month__month=current_month, month__year=current_year)
    except Budget.DoesNotExist:
        budget = None

    # Only proceed if the user has set a budget
    if budget:
        # Calculate the total expenses for the current month
        total_expenses = Expense.objects.filter(user=user, date__month=current_month, date__year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0

        # Compare total expenses with the budget amount
        if total_expenses > budget.amount:
            return True, total_expenses, budget.amount  # Budget exceeded
    return False, None, None  # Budget not exceeded or no budget set

@login_required
def download_transactions(request):
    # Fetch all income and expenses data
    incomes = Income.objects.filter(user=request.user).order_by('date')
    expenses = Expense.objects.filter(user=request.user).order_by('date')

    # Create an Excel workbook
    wb = Workbook()
    ws = wb.active

    # Write the Income section
    ws.append(['Income'])
    ws.append(['Month', 'Source', 'Date', 'Amount'])

    current_month = None
    for income in incomes:
        month = income.date.strftime('%B %Y')
        if month != current_month:
            ws.append([month])  # Write the month
            current_month = month
        
        # Write the transaction details
        ws.append(['', income.source, income.date.strftime('%Y-%m-%d'), income.amount])

    # Add space before Expenses
    ws.append([])
    
    # Write the Expense section
    ws.append(['Expenses'])
    ws.append(['Month', 'Category', 'Date', 'Amount'])

    current_month = None
    for expense in expenses:
        month = expense.date.strftime('%B %Y')
        if month != current_month:
            ws.append([month])  # Write the month
            current_month = month
        
        # Write the transaction details
        ws.append(['', expense.category, expense.date.strftime('%Y-%m-%d'), expense.amount])

    # Auto-adjust column width to avoid #######
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    # Create the response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="transactions.xlsx"'

    # Save the workbook to the response
    wb.save(response)
    return response