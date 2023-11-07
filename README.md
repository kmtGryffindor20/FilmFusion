# FilmFusion

This is the backend repository of the FilmFusion web application. 

This is a Python project that interacts with a movie database. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. You can download it from the official website: https://www.python.org/downloads/

### Installing

1. Clone the repository to your local machine:
```bash
git clone https://github.com/kmtGryffindor20/FilmFusion.git
```
2. Navigate to the project directory:
```bash
cd FilmFusion
```
3. Install the required packages:
```bash
pip install -r requirements.txt
```


## Deployment

You will need to set up a MySQL database and update the DATABASES configuration in settings.py with your database name, user, password, host, and port.
Run the Django migrations to create the database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```
Finally, start the Django development server:
```bash
python manage.py runserver
```
Now, you can access the application by navigating to http://localhost:8000 in your web browser.

## Initializing Database
To import a MySQL database from a dump file, you can use the `mysql` command-line utility. Here are the steps:

1. Open your terminal.

2. Run the `mysql` command with the following syntax:
```bash
mysql -u [username] -p [database_name] <  dump.sql
```
Replace `[username]` with your MySQL username, `[database_name]` with the name of the database you want to import into.

3. You will be prompted to enter your MySQL password. After entering the password, the command will import the database from the specified file.

For example, if your username is `root`, your database name is `mydatabase`, and your dump file is named `dump.sql`, you would run:
```bash
mysql -u root -p mydatabase < dump.sql
```

This will populate the `mydatabase` database with the data from the `dump.sql` file.

## Built With

* [Python](https://www.python.org/) - The programming language used.
* [Django](https://www.djangoproject.com/) - The web framework used.
* [django-rest-framework](https://www.django-rest-framework.org/) - Django's API framework


## API Hosting

The API is currently hosted on [PythonAnywhere](https://www.pythonanywhere.com/) at the following [URL](https://kmtgryffindor20.pythonanywhere.com/api/movies/)
