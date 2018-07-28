# Build an Item Catalog PostgreSQL Application Project

Source code to run an item catalog application.

## Project

This is an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.
This project makes part of the [Full-Stack Web Nanodegree Program](https://udacity.com/course/full-stack-web-developer-nanodegree--nd004) from Udacity.

## Code

Code is neatly formatted and follows the Python [PEP-8 Guidelines](http://pep8online.com/).

## Installation and Usage

In order to run this project you need python 3.x installed.

### Project Extensions

```sh
pip3 install Flask
pip3 install Flask-Babel
pip3 install flask-sqlalchemy
pip3 install flask-marshmallow
pip3 install -U flask-sqlalchemy marshmallow-sqlalchemy
pip3 install Flask-WTF
pip3 install Flask-OAuthlib
pip3 install --upgrade oauth2client
pip3 install flask_script
pip3 install flask_migrate
pip3 install psycopg2
```

```sh
git clone https://github.com/danielvito/item-catalog-postgresql-project.git
cd item-catalog-postgresql-project
```

### Database

This application uses a PostreSQL database managed automatically by SQLAlchemy and Alembic extensions.

You can follow the below steps if you want to create the database with samples records.

```sh
cd item-catalog-postgresql-project/
# creating user
sudo -u postgres createuser catalog
# creating database
sudo -u postgres createdb catalog
# giving the user a password
sudo -u postgres psql
psql=\# alter user catalog with encrypted password 'catalog';

# migrating the database
python manage.py db init
python manage.py db migrate
python manage.py db upgrade

# insert the sample records
python lotsofitens.py
```

### Running the application in dev mode on Linux

```sh
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_DEBUG=1
export FLASK_ENV=development
export FLASK_APP=project.py
flask run --host=0.0.0.0 --port=5000
```

Open url <http://localhost:5000/> with a web browser.

### Running the application in dev mode on Windows (Power Shell)

```sh
$env:LC_ALL='C.UTF-8'
$env:LANG='C.UTF-8'
$env:FLASK_DEBUG=1
$env:FLASK_ENV='development'
$env:FLASK_APP='project.py'
flask run --host=0.0.0.0 --port=5000
```

Open url <http://localhost:5000/> with a web browser.

### Running the application in shell mode

```sh
# after create FLASK_APP env var
flask shell
>>> app
<Flask 'app'>
>>> User
<class 'app.models.User'>
>>> Brand.query.all()
[<Brand Nike>, <Brand Adidas>, <Brand Wilson>]
```

### I18n

This app uses the Flask-babel extension for translation.

The code below finds every use of the function `_('any_key')` and updates the Portuguese and English translation files.

```sh
pybabel extract -F babel.cfg -k _l -o messages.pot .
pybabel update -i messages.pot -d app/translations
pybabel compile -d app/translations
```

## License

All the code in this project is a public domain work, dedicated using [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Feel free to do whatever you want with it.
