echo "Building the project"

# Install pip if not installed
if ! command -v pip &> /dev/null
then
    echo "Installing pip"
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3.9 get-pip.py
fi

# Install project dependencies
python3.9 -m pip install -r requirements.txt

echo "Make migrations"
python3.9 manage.py makemigrations
python3.9 manage.py migrate

echo "Collect static files"
python3.9 manage.py collectstatic --noinput --clear
