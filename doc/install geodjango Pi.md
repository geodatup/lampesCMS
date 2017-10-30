install geodjango Pi

get docker 
curl -sSL get.docker.com | sh


get postgis image

depuis geoppopy ou tobi312

démarrer la base depuis tobi312
~~~
sudo docker run --restart="always" --name postgis -d -p 5432:5432 -v /home/pi/.local/share/postgresql:/var/lib/postgresql/data -e POSTGRES_PASSWORD=mcot9a9.u tobi312/rpi-postgresql-postgis:9.6-2.3
~~~


create container and run

add geodjango dependencies
~~~
echo "for gdal:"
sudo apt-get install binutils libproj-dev gdal-bin
~~

building geos-3.6.2

export LD_LIBRARY_PATH=/usr/local/lib