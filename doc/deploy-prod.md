


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


créer un fichier .gitignore avec dedans
~~~
lampesCMS/setting
lampesCMS/static
~~~

penser à diviser les settings dans differents fichier 
https://code.djangoproject.com/wiki/SplitSettings




créer un environnement avec un user et tout

si besoin créer le groupe
sudo groupadd --system webapps

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

Installer les dep (python 3 donc avec pip3)

~~~
 pip3 install -r requirements.txt 
~~~

Installer Gunicorn et supervisor
~~~
 pip3 install gunicorn
~~~

~~~
export DJANGO_SETTINGS_MODULE=lampesCMS.settings.production
~~~



verifier que tout est ok 
~~~
gunicorn lampesCMS.wsgi:application --bind=0.0.0.0:8000
~~~



Puis créons le fichier /etc/supervisor/conf.d/lampesCMS.conf et donnons lui le contenu suivant:
nano /etc/supervisor/conf.d/lampesCMS.conf



~~~
[program:lampesCMS]
command = /var/www/webapps/lampesCMS/bin/gunicorn_start                    ; Command to start app
user = lampesCMS                                                          ; User to run as
stdout_logfile = /var/www/webapps/lampesCMS/logs/gunicorn_supervisor.log   ; Where to write log messages
redirect_stderr = true                                                ; Save stderr in the same log
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8                       ; Set UTF-8 as default encoding
~~~

créer le script gunicorn

et le rendre executable
~~~
sudo chmod ugo+x bin/gunicorn_start
~~~


créer le dossier logs et un fichier à populer 
~~~
mkdir /var/www/webapps/lampesCMS/logs/
touch /var/www/webapps/lampesCMS/logs/gunicorn_supervisor.log 
~~~



relancer le serveur web django 

~~~
sudo supervisorctl reread
sudo supervisorctl reload
sudo supervisorctl update
sudo supervisorctl status lampesCMS

~~~



configurer NGINX

inserer le fichier dans sites-available

sudo ln -s /etc/nginx/sites-available/lampesCMS /etc/nginx/sites-enabled/lampesCMS


restart NGINX


collectstatic 

change setting to feet base dir of STATICFILES_DIRS

~~~
DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
~~~

~~~
sudo su - lampesCMS
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
