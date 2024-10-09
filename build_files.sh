echo "Building the project"
cd personal_finance_manager
python -m pip install -r requirements.txt


echo "Make migrations"
python manage.py makemigrations
python manage.py migrate

echo "Collect static files"
python manage.py collectstatic --noinput --clear