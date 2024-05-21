# Jotify-Backend

The backend application for Jotify, a simple online productivity app for saving notes and to-do lists.

## Project Description

This is the backend for Jotify, an app that let's registered users save categorized notes and save to-do tasks. The backend is built using Django and relies on the customizable Django REST framework to build the RESTful API for Jotify. The app is configured to use a postgresql database connection for storing and managing user account information, saved notes and tasks. For the frontend ui built with the React library, see [Jotify-Frontend](https://github.com/ThatDudeJude/Jotify-FE).

### Technology used
| Technology  |       Version    |      Utility    |
|-------------|------------------|-----------------|
|    Django   |  v4.1            | Python based web-framework|
|   Django REST Framework| v3.13.1    | A python-based toolkit for building Web APIs with Django|
|   Postgres  | v14.0            | SQL based Relational Database Management System (RDMS)|
| Psycopg2    |     v2.9.1       | A PostgreSQL database adapter for Python web apps |



## Installation and Setup


1. Launch your terminal.
2. Create a new folder and navigate to it.
   ```
    mkdir jotify-backend
    cd jotify-backend
   ```
3. Clone this github repository here: https://github.com/ThatDudeJude/Jotify-BE   
4. Ensure that [python](https://www.python.org) version v3.8+ and pip is installed in your computer.
5. Install a postgres server for your OS ([more info here](https://www.postgres.org/download)) if not installed. For windows users, you can add psql.exe to path.
6. Create a new virtual environment and activate it .For Linux and Mac OS run `python3 -m venv venv && ./venv/bin/activate` . For Windows cmd.exe run `c:\>c:\Python38\python -m venv venv && venv/SCRIPTS/activate.bat` .
7. Install a postgres server for your OS if not installed ([more info here](https://www.postgres.org/download)). 
8. Install all required libraries. 
   ```
   python3 -m pip install -r requirements.txt
   ```

9.  For the password recovery feature, you can set up an smtp service, preferrably [gmail's smtp](https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab). Add the following variables to your environment
```
    DEFAULT_FROM_EMAIL=[youraccount@gmail.com]
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_HOST_USER=[youraccount@gmail.com]
    EMAIL_HOST_PASSWORD=[your smtp service account password]        
```
10.  To create a local database for storage, open a new terminal and create a postgres database for development and testing purposes. 

For Mac and Linux users, run :
```    
    sudo su postgres
    psql postgres
    \! hostname
```

For Windows users, run:
```
    psql -U postgres    
    \! hostname
```
You need to create a role and assign the necessary priviledges
```    
    CREATE USER jotify_app with password 'jotify_app_password';        
    CREATE DATABASE jotify_app_db;
    GRANT ALL PRIVILEDGES ON DATABASE jotify_app_db TO jotify_app;
    \connect jotify_app_db
    \conninfo    
    \q
```
   
Now set the environment variables using information from hostname, the ez_pizza password, and the database's `\conninfo` output.
   ```
   DATABASE_URL=postgres://USERNAME:PASSWORD@HOSTNAME:PORT/jotify_app_db   
   ``` 
13.  Add a secret key for the Django app. To generate a secret key, type in ``python3 -c "import secrets; print(secrets.hex_token());" `` and use the output as the secret key.
```
    SECRET_KEY=[secret_key]        
    
```
To launch the django server, run ``python3 manage.py runserver`` and navigate to http://127.0.0.1:8000/ to view the application

## Tests

To test the API, run

```
    python manage.py test
```

## Contributing
Want to contribute? See contributing guidelines [here](/CONTRIBUTING.md).

## Codebeat

[![codebeat badge](https://codebeat.co/badges/04631858-5c13-457d-9e0a-000f97fd66b6)](https://codebeat.co/projects/github-com-thatdudejude-jotify-be-v1_final_touches)
## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE.txt)
