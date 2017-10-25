

~~~
sudo git clone https://github.com/geodatup/lampesCMS.git
sudo apt-get update
sudo apt-get install python3.5 python-dev libpq-dev

~~~

créer un environnement 

~~~
sudo useradd --system --gid webapps --shell /bin/bash --home /var/www/webapps/lampesCMS lampesCMS
sudo chown lampesCMS /var/www/webapps/lampesCMS
sudo su - lampesCMS
~~~



dans le dossier créer l'environnement virtuel et l'activer


~~~
cd lampesCMS
sudo virtualenv --python=python3.5 .
sudo source bin/activate
~~~

Installer les dep

~~~
pip install -r requirements.txt 
~~~


relancer le serveur web django 

~~~
sudo supervisorctl reload
~~~

collectstatic

~~~
sudo su - geodatup
python manage.py collectstatic
~~~

Installer tous les package python de base 

~~~
sudo su - geodatup
pip3 install -r requierements/base.txt
~~~
puis relancer supervisorctl en dehors de la session geodatup

# déploiement en production 


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
