# HISS

## To initialize DB

    $ heroku run python manage.py migrate --app hashmail

## To create superuser

    $ heroku run python manage.py createsuperuser --app hashmail

## 'master' branch is auto deployed to heroku

Visit: http://hashmail.herokuapp.com/