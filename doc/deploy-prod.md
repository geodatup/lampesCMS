
Penser à diviser les settings dans differents fichier 
https://code.djangoproject.com/wiki/SplitSettings

Publier l'application
~~~
pip freeze > requierements.txt
git add .
git commit -m "init"
~~~

~~~
sudo git clone https://github.com/geodatup/lampesCMS.git
sudo apt-get update
sudo apt-get install python3.5 python-dev libpq-dev
~~~

---

#### sous jessie python3.4 :
~~~
sudo apt-get install python3.4 python-dev libpq-dev libjpeg-dev
~~~

installer pip / virtualenv / virtualenvwrapper
~~~
sudo apt-get install -y python3-pip python3-dev
sudo pip3 install --upgrade virtualenv


~~~

because of this error 
~~~
ImportError: cannot import name IncompleteRead
~~~

uninstall python-pip and install pip
~~~
sudo apt-get remove python-pip
sudo easy_install pip3

~~~

add geodjango dependencies
~~~
echo "for gdal:"
sudo apt-get install binutils libproj-dev gdal-bin
~~~



créer un fichier .gitignore avec dedans
~~~
lampesCMS/setting
lampesCMS/static
~~~

---





créer un environnement avec un user et tout

si besoin créer le groupe
~~~
sudo groupadd --system webapps
~~~

~~~
sudo useradd --system --gid webapps --shell /bin/bash --home /var/www/webapps/lampesCMS lampesCMS
sudo chown lampesCMS -R /var/www/webapps/lampesCMS
sudo su - lampesCMS
~~~





dans le dossier créer l'environnement virtuel et l'activer


~~~
cd lampesCMS
sudo virtualenv --python=python3.5 .
sudo source bin/activate
~~~


###sous jessie
~~~
cd lampesCMS
sudo virtualenv --python=python3.4 .
source bin/activate
~~~


####Installer les dep (pip)

~~~
sudo pip install -r requirements.txt 
~~~

si erreur 
~~~
ImportError: No module named pkg_resources
~~~

lancer 
~~~
sudo apt-get install --reinstall python-pkg-resources
~~~


~~~
export DJANGO_SETTINGS_MODULE=lampesCMS.settings.production
export LD_LIBRARY_PATH=/usr/local/lib
~~~

edit the bash_profile 
~~~
echo "export DJANGO_SETTINGS_MODULE=lampesCMS.settings.production" >> ~/.bash_profile
echo "export LD_LIBRARY_PATH=/usr/local/lib" >> ~/.bash_profile
~~~

verifier que tout est ok 
~~~
gunicorn lampesCMS.wsgi:application --bind=0.0.0.0:8000
~~~



Depuis le user Pi (exit de lampesCMS), créons le fichier /etc/supervisor/conf.d/lampesCMS.conf et donnons lui le contenu suivant:
~~~
nano /etc/supervisor/conf.d/lampesCMS.conf
~~~


~~~

[program:lampesCMS]
command = /home/pirate/lampesCMS/bin/gunicorn_start                    ; Command to start app
user = lampesCMS                                                          ; User to run as
stdout_logfile = /home/pirate/lampesCMS/logs/gunicorn_supervisor.log   ; Where to write log messages
redirect_stderr = true                                                ; Save stderr in the same log
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8                       ; Set UTF-8 as default encoding
~~~

créer le script gunicorn_start dans `bin/gunicorn_start`

~~~
#!/bin/bash

NAME="lampesCMS"                                  # Name of the application
DJANGODIR=/home/pirate/lampesCMS             # Django project directory
SOCKFILE=/home/pirate/lampesCMS/run/gunicorn.sock  # we will communicte using this unix socket
USER=lampesCMS                                        # the user to run as
GROUP=webapps                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=lampesCMS.settings.production            # which settings file should Django use
DJANGO_WSGI_MODULE=lampesCMS.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
#  --bind=0.0.0.0:8000 \ 
  --log-level=debug \
~~~

et le rendre executable
~~~
chmod ugo+x bin/gunicorn_start
~~~


créer le dossier logs et un fichier à populer 
~~~
mkdir logs/
touch logs/gunicorn_supervisor.log 
~~~



relancer le serveur web django 

~~~
sudo supervisorctl reread
sudo supervisorctl reload
sudo supervisorctl update
sudo supervisorctl status lampesCMS
sudo supervisorctl stop lampesCMS
sudo supervisorctl start lampesCMS
~~~



configurer NGINX

inserer le fichier dans sites-available
~~~
sudo ln -s /etc/nginx/sites-available/lampesCMS /etc/nginx/sites-enabled/lampesCMS
~~~

restart NGINX

sudo /etc/init.d/nginx restart


collectstatic 

change setting to feet base dir of STATICFILES_DIRS

~~~
DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
~~~

~~~
sudo su - lampesCMS
source bin/activate
python manage.py collectstatic
~~~



# déploiement des données de production 


~~~
cd /var/www/webapps/website
source bin/activate
sudo git fetch
sudo git pull
sudo python manage.py migrate
sudo python manage.py loaddata dump/auth.json
sudo python manage.py loaddata dump/filer.json 
sudo python manage.py loaddata dump/dump-catformation.json
sudo python manage.py loaddata dump/dump-categorie.json
sudo python manage.py loaddata dump/dump-moduleformation.json
sudo python manage.py loaddata dump/dump-chapitreformation.json
sudo python manage.py loaddata dump/dump-formation.json
sudo python manage.py loaddata dump/dump-personne.json
sudo python manage.py loaddata dump/dump-reference.json
sudo python manage.py loaddata dump/dump-secteur.json
sudo python manage.py loaddata dump/dump-section.json
sudo python manage.py loaddata dump/dump-service.json 
sudo python manage.py loaddata dump/dump-software.json
sudo python manage.py loaddata dump/dump-plan.json
sudo python manage.py loaddata dump/dump-produit.json
sudo supervisorctl reload
sudo su - geodatup
python manage.py collectstatic
~~~


## Update du projet

démarrer l'environemment du projet
~~~
sudo su -u LampesCMS
~~~

~~~
git status
git fetch
git pull
exit
~~~

relancer le projet par supervisorctl depuis la session superuser
~~~
sudo supervisorctl restart lampesCMS
~~~


