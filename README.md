# Web Boards

[![Python Version](https://img.shields.io/badge/python-3.6-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-1.11-brightgreen.svg)](https://djangoproject.com)

Web Boards is a small project to practice Python and Django. It's a basic implementation of a kind of 'forum'.

In the project was implemented:
* basic CRUD operations
* tests
* account management (password change/reset with email)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Running locally

* Create and activate a virtualenv:

on Linux
```
virtualenv env
source env/bin/activate
```

on Windows
```
virtualenv env
.\env\Scipts\activate
```

* Clone the repository:

```
git clone https://github.com/zawi99/web-boards.git
```

* Install the requirements:

```
pip install -r requirements.txt
```

* Setup the local environment configurations:

```
cp .env.example .env
```

* Create the database:

```
python manage.py migrate
```

* You might need to create superuser:

```
python manage.py createsuperuser
```

* Run the development server:

```
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.

## Running the tests

To run the tests:

```
python manage.py test
```

## Authors

* **Michal Zawislak**