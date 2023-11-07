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

## Built With

* [Python](https://www.python.org/) - The programming language used.
* [Django](https://www.djangoproject.com/) - The web framework used.

## Authors

* **Your Name** - *Initial work* - [YourGithubUsername](https://github.com/YourGithubUsername)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
