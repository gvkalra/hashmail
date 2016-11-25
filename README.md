HISS
============

#Hashtag Image Sharing Service.

# Setting up development environment
--------------------------------------------
## Install Dependencies
Ruby
```bash
$ sudo apt-get install ruby-full
```
Heroku Command Line
```bash
$ wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
```
pip
```bash
$ sudo apt-get install python-pip
$ sudo pip install --upgrade pip
```
virtualenv
```bash
$ sudo pip install virtualenv
```
sqlitebrowser
```bash
$ sudo apt-get install sqlitebrowser
```

## Clone project
```bash
$ git clone git@github.com:gvkalra/hashmail.git
$ cd hashmail
```

## Create & activate virtualenv
```bash
$ virtualenv venv
$ source venv/bin/activate
(venv) $
```

## Install required packages
```
(venv) $ pip install -r requirements.txt
```

## Create database
```bash
(venv) $ python manage.py migrate
(venv) $ python manage.py migrate --run-syncdb
```

## Serve locally
```bash
(venv) $ heroku local -p 5000
```
After this you can navigate to http://127.0.0.1:5000/ and develop HISS. <br/>
It is not required to restart the server for editing files.

# Other useful commands
--------------------------------------------
## To create superuser in django
```bash
(venv) $ python manage.py createsuperuser
```
After this you can navigate to http://127.0.0.1:5000/admin and administer user accounts.

# Notes
--------------------------------------------
### 'master' branch is auto deployed to heroku
Visit: http://hashmail.herokuapp.com/

Authors
-----------------
- Gaurav Kalra (<gvkalra@kaist.ac.kr>)
- Noé Domínguez (<noe_dgz@kaist.ac.kr>)
- Azizi Omar (<azizi.bin.omar@kaist.ac.kr>)
- Leegeun Ha (<betown@kaist.ac.kr>)
