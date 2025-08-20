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
You can visit the live demo of the Moneta Personal Finance Tracker [here](https://moneta-personal-finance-website.vercel.app/).

---

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript (using Django Templates), Chart.js, Tailwind CSS
- **Backend**: Django, Python
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **Web Server**: Nginx (for production)
- **Deployment**: Render, Docker
- **External Services**:
  - Email Service: Gmail SMTP
  - Random Quote API Ninjas API

---

## Installation

You can install and run Moneta using either Docker (recommended) or traditional Python setup.

### Option 1: Docker Installation (Recommended)

#### Prerequisites
- **Docker** and **Docker Compose** installed on your machine
- Create a Gmail account and generate an **App Password** for SMTP (for email alerts)

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/HydrallHarsh/Moneta-Personal-Finance-Website.git
   cd Moneta-Personal-Finance-Website
   ```

2. Copy the environment file and configure it:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your settings:
   ```bash
   # Update these values
   SECRET_KEY=your-secret-key-here
   EMAIL_HOST_USER=your-gmail-username@gmail.com
   EMAIL_HOST_PASSWORD=your-gmail-app-password
   ```

3. Build and start the services:
   ```bash
   # For production with nginx
   docker-compose up --build -d
   
   # Or for development (without nginx)
   docker-compose -f docker-compose.dev.yml up --build
   ```

4. The application will be available at:
   - **Production**: http://localhost (port 80)
   - **Development**: http://localhost:8000

5. Access the admin panel:
   - URL: http://localhost/admin (or http://localhost:8000/admin for dev)
   - Default credentials: `admin` / `admin123`

#### Docker Commands

You can use the provided Makefile for common operations:

```bash
# Start services
make up          # Production mode with nginx
make up-dev      # Development mode

# View logs
make logs        # All services
make logs-web    # Web service only

# Database operations
make migrate     # Run migrations
make createsuperuser  # Create admin user

# Utilities
make shell       # Open shell in web container
make down        # Stop all services
make clean       # Remove all containers and volumes
```

### Option 2: Traditional Python Installation

#### Prerequisites
- **Python 3.8+** installed on your machine
- **PostgreSQL** installed and running
- **Node.js** and **npm** for frontend assets
- Create a Gmail account and generate an **App Password** for SMTP (for email alerts)

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/HydrallHarsh/Moneta-Personal-Finance-Website.git
   cd Moneta-Personal-Finance-Website
   ```

2. Create Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   npm install
   ```

4. Set up your PostgreSQL database and environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your database and email settings.

5. Build frontend assets:
   ```bash
   npm run build:css
   ```

6. Run Migrations:
   ```bash
   python manage.py migrate
   ```

7. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

8. Start Django Development Server:
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
├── pesonal_finance_manager/          # Django project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tracker/                          # Main Django app
│   ├── templates/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── ...
├── src/                              # Source files
├── static/                           # Static files
├── staticfiles_build/                # Built static files
├── Docker Configuration/
│   ├── Dockerfile                    # Docker image definition
│   ├── docker-compose.yml            # Production Docker setup
│   ├── docker-compose.dev.yml        # Development Docker setup
│   ├── docker-entrypoint.sh          # Container startup script
│   ├── nginx.conf                    # Nginx configuration
│   └── .dockerignore                 # Docker ignore file
├── Configuration Files/
│   ├── .env.example                  # Environment variables template
│   ├── requirements.txt              # Python dependencies
│   ├── package.json                  # Node.js dependencies
│   ├── tailwind.config.js            # Tailwind CSS config
│   └── Makefile                      # Docker helper commands
├── manage.py                         # Django management script
└── build.sh                          # Build script
```
---
## Contributing

We welcome contributions to make Moneta even better! To contribute:

- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Make your changes and commit (git commit -am 'Add new feature').
- Push the branch (git push origin feature-branch).
- Open a Pull Request.
