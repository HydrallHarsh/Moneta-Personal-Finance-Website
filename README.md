# Moneta - Personal Finance Manager

Moneta is a web-based personal finance manager that helps users track their income, expenses, and savings. It includes features for setting monthly budgets, receiving alerts when exceeding budgets, tracking savings goals, and exporting transactions in CSV format. Built using Django and PostgreSQL, it offers a simple, user-friendly interface for managing your finances with detailed visualizations.

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Monthly Budgets**: Users can set and manage their monthly budgets and get notified if they exceed their budget.
- **Transaction Management**: Easily add, edit, or delete income and expense transactions.
- **CSV Export**: Export all transactions into a CSV or Excel file for offline analysis.
- **Data Visualization**: Visualize income, expenses, and savings with the help of beautiful charts using Chart.js.
- **Savings Goals**: Track your savings goals and monitor progress over time.
- **PostgreSQL Database**: All data is securely stored in a PostgreSQL database.
- **Email Alerts**: Users receive an email alert when their spending exceeds their set budget for the month.
- **Random Quote API**: Budget-exceeded email alerts include an inspiring quote fetched from an external API.

---

## Demo
You can visit the live demo of the Moneta Personal Finance Tracker [here](https://moneta-personal-finance-website.onrender.com/).

---

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript (using Django Templates), Chart.js
- **Backend**: Django, Python
- **Database**: PostgreSQL
- **Deployment**: Render (or any alternative service you're using)
- **External Services**:
  - Email Service: Gmail SMTP
  - Random Quote API Ninjas API

---

## Installation

### Prerequisites
- **Python 3.8+** installed on your machine.
- **PostgreSQL** installed and running.
- Create a Gmail account and generate an **App Password** for SMTP (for email alerts).

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/HydrallHarsh/Moneta-Personal-Finance-Website.git
   cd Moneta-Personal-Finance-Website
2.Create Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
3.Install Dependencies:
  ```bash
  pip install -r requirements.txt
  ```
4.Set up your PostgreSQL database and environment variables:
  ```bash
  DEBUG=True
  SECRET_KEY=your-secret-key
  DATABASE_URL=your-database-url
  EMAIL_HOST_USER=your-gmail-username
  EMAIL_HOST_PASSWORD=your-app-password
  ```
5.Run Migrations
  ```bash
  python manage.py migrate
  ```
6.Start Django Devlopment Server
  ```bash
  python manage.py runserver
  ```
---

## Usage

- **Register**: Create an account on the platform to start managing your finances.
  
- **Login**: Log in to your account to access your personal finance dashboard.

- **Manage Transactions**: 
  - Add new income or expense transactions.
  - Edit or delete existing transactions as needed to keep your records up-to-date.

- **Set Monthly Budgets**: 
  - Define your monthly budget to control your spending.
  - Receive notifications via email when you exceed your budget limit.

- **Track Savings**: 
  - Track your savings progress.
  - Set and monitor savings goals to achieve financial milestones.

- **Visualize Data**:
  - Get a clear view of your financial health with visual charts and graphs.
  - Charts show detailed insights into your income, expenses, and net savings over time.

---

## Project Structure
```bash
Moneta-Personal-Finance-Website/
│
├── personal_finance_manager/
│   ├── personal_finance_manager/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── src/
│   ├── static/
│   └── tracker/
│       ├── templates/
│       ├── migrations/
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── views.py
│       └── ...
└── venv/
```
---
## Contributing

We welcome contributions to make Moneta even better! To contribute:

-Fork the repository.
-Create a new branch (git checkout -b feature-branch).
-Make your changes and commit (git commit -am 'Add new feature').
-Push the branch (git push origin feature-branch).
-Open a Pull Request.
