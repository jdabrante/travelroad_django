
<center>

# TÍTULO DE LA PRÁCTICA


</center>

***Nombre:***
***Curso:*** 2º de Ciclo Superior de Desarrollo de Aplicaciones Web.

### ÍNDICE

+ [Introducción](#id1)
+ [Objetivos](#id2)
+ [Material empleado](#id3)
+ [Desarrollo](#id4)
+ [Conclusiones](#id5)


#### ***Introducción***. <a name="id1"></a>

Aquí explicamos brevemente la parte teórica que tiene que ver con la práctica que se va a realizar

#### ***Objetivos***. <a name="id2"></a>

Aquí explicamos los objetivos que se pretenden alcanzar al realizar la práctica.

#### ***Material empleado***. <a name="id3"></a>

Enumeramos el material empleado tanto hardware como software y las conficuraciones que hacemos (configuraciones de red por ejemplo) 

#### ***Desarrollo***. <a name="id4"></a>

#### Servidor de desarrollo

Para la realización de este proyecto es necesario, en primer lugar, la instalación de python. Para ello podemos seguir las instrucciones de este <a href="https://docs.python-guide.org/starting/install3/linux/"> enlance </a>.

Una vez instalado python podremos crear un entorno virtual con venv. Esto permitirá encapsular las dependencias para así poder, en un mismo sistema, tener versiones diferentes de diversas
librerias y frameworks, dependiendo de nuestras necesidades. Para ello podemos ejecutar el siguiente comando dentro de la carpeta donde alojaremos el proyecto:

```
python -m venv .venv --prompt travelroad_django 
```

Hecho esto, para activiar el entorno virtual usaremos el siguiente comando: 

```
source .venv/bin/activate
```

*En el caso de que deseemos salir del mismo basta con ejecutar el comando "deactivate".*

El siguiente paso, una vez dentro del entorno virtual, será instalar django: 

```
pip install django
```

Django es el framework web que usaremos para crear el proyecto. Así pues, para iniciar el mismo ejecutaremos el siguiente comando:

```
django-admin startproject main .
```

Para probar que el proyecto está bien creado podemos utilizar

```
python manage.py check
```

Y para lanzarlo:

```
python manage.py runserver
```

*Se lanza en el puerto 8000*

#### Creación de la aplicación

Tenemos creado el proyecto, ahora el siguiente paso es crear las aplicaciones que componen a la misma. Para ello utilizamos el siguinete comando:

```
python manage.py startapp places 
```

Una vez crada la aplicación es necesario añadirla dentro del fichero de configuración para que Django la reconozca como tal. Este fichero se encuentra dentro de la carpeta del proyecto ( en este caso main )

```
(travelroad_django) pc17-dpl@a109pc17dpl:~/travelroad_django$ nano main/settings.py
```

Dentro deberemos de buscar el apartado de INSTALLED_APPS y añadir la siguiente linea a la lista:

```
'places.apps.PlacesConfig'
```

#### Acceso a la base de datos

Cuando creamos un nuevo proyecto en Django este viene configurado por defecto para trabajar con sqlite3. No obstate soporta una gran variedad de gestores de base de datos, entre ellos postgreSQL, la cual usaremos en este proyecto. Para ello solo es necesario instalar psycopg así como modificar el fichero de configuración settings.py.
Para instalar psycopg:

```
pip install psycopg2-binary
```

Y en cuanto al fichero de configuración, será necesario encontrar la variable de entorno DATABASES y cambiarla por el siguiente contenido:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travelroad',
        'USER': 'travelroad_user',
        'PASSWORD': 'XXXXXXX',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
```

#### Modelos

Una vez configurado todo el proyecto queda la parte más importante, crear los modelos, las vistas y plantillas.

En Django existe un ORM que permite mapear clases escritas en Python (modelos) con entidades relacionales de la base de datos. Así pues será necesario crear un modelo para los lugares. Para ello deberemos de introducirnos en el directorio de la aplicación places y dentro de esta editar el fichero models.py:

```
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=255)
    visited = models.BooleanField()

    class Meta:
        # ↓ necesario porque ya partimos de una tabla creada ↓
        db_table = "places"

    def __str__(self):
        return self.name
```


#### Vistas

Las vistas son la parte de la aplicación con mayor lógica de negocio. Es donde llegarán las peticiones HTTP y se devolverán respuestas HTTP. Al igual que los modelos estas se encuentran dentro del directorio de la aplicación places ( cada aplicación tiene sus propios modelos y vistas entre otros ). Dentro del views.py será necesario añadir el siguiente contenido:

```
from django.http import HttpResponse
from django.template import loader

from .models import Place


def index(request):
    wished = Place.objects.filter(visited=False)
    visited = Place.objects.filter(visited=True)
    template = loader.get_template('places/index.html')
    context = {
        'wished': wished,
        'visited': visited,
    }
    return HttpResponse(template.render(context, request))
```

#### Plantillas

Hecha la vista, el siguiente paso es crear la plantilla, es decir, el fichero HTML al que se le suministrará las variables que se le ha sido suministrada por medio de la vista. Para ello, dentro de la aplicación de places será necesario crear una carpeta con el nombre "templates" ya que Django buscará las plantillas dentro de un directorio con este mismo nombre. Para el caso que nos ocupa, dentro de templates crearemos otra carpeta con el nombre de places y dentro de esta el fichero index.html ( al que hemos hecho referencia en la vista anteriormente creada ). Dentro de este fichero irá el siguiente contenido:

```
<h1>My Travel Bucket List</h1>

<h2>Places I'd Like to Visit</h2>

<ul>
  {% for place in wished %}
  <li>{{ place }}</li>
  {% endfor %}
</ul>

<h2>Places I've Already Been To</h2>

<ul>
  {% for place in visited %}
  <li>{{ place }}</li>
  {% endfor %}
</ul>
```

#### URLS

El último paso dentro de la creación del proyecto sería definir las URLS para vincular las mismas con las correspondientes vistas. Para ello en primer lugar crearemos el fichero de urls dentro de la aplicación places y dentro de este añadiremos el siguiente contenido:

```
from django.urls import path

from . import views

app_name = 'places'

urlpatterns = [
    path('', views.index, name='index'),
]
```

Hecho esto definimos las urls exteneras, a nivel del proyecto:

```
from django.contrib import admin
from django.urls import path
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # NUEVA LÍNEA ↓
    path('', include('places.urls', 'places')),
]
```

#### Parametrización de la configuración

Hay que tener en cuenta que algunos de los datos introducidos en nuestro proyecto pueden ser sensibles, como es el caso de la configuración de la base de datos, la cual cuenta con la contraseña de la misma. Es por esto por lo que se necesita de un fichero de configuración en el cual guardemos aquellas variables de entorno sensibles y el cual deberá de estár fuera del controlador de versiones. En este caso para ello se ha utilizado prettyconf, que permite guardas las variables en un fichero .env y llamarlas por medio de la función config. Para instalar este paqueta lo podemos hacer de la siguinete manera:

```
pip install prettyconf
```
Una vez instalado creamos las variables de entorno dentro del fichero .env y modificamos el fichero settings.py de la siguinte manera:

```
...
from pathlib import Path
# ↓ Nueva línea
from prettyconf import config
# ↑ Nueva línea
...
DEBUG = config('DEBUG', default=True, cast=config.boolean)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=config.list)
...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='travelroad'),
        'USER': config('DB_USERNAME', default='travelroad_user'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default=5432, cast=int)
    }
}
...
```

Otra buena práctrica y algo necesario en este caso, es introducir las dependencias de nuestro proyecto en un fichero requirements.txt el cual podremos utilizar para instalar todas las dependencias con un solo comando

```
pip install -r requirements.txt
```

#### Servidor de aplicación

Una vez terminado el proyecto es necesario desplegarlo. Para desplegar una aplicación Django existe variedad de opciones, no obstante en este caso vamos a utilizar gunicorn. Para ello en primer lugar instalamos gunicorn en nuestro entorno virtual:

```
pip install gunicorn
```

Una vez instalado podemos lanza el script que lanza el servidor:

```
 gunicorn main.wsgi:application
```

Sin embargo para que esto se mantenga activo tendriamos que iniciarlo cada vez que iniciaramos el servidor de manera manual. Para evitar esto utilizaremos un servicio systemd, en este caso Supervisor, un sistema cleinte/servidor que permite monitorizar y controlar procesos en sistemas Linux/UNIX. Para instalarlo simplemente ejecutamos el siguiente comando:

```
sudo apt install -y supervisor
```

Una vez instalado podemos comprobar el estado del servicio con:

```
pc17-dpl@a109pc17dpl:~$ sudo systemctl status supervisor.service 
[sudo] contraseña para pc17-dpl: 
● supervisor.service - Supervisor process control system for UNIX
     Loaded: loaded (/lib/systemd/system/supervisor.service; enabled; preset: e>
     Active: active (running) since Sun 2024-01-21 19:33:01 WET; 3h 2min ago
       Docs: http://supervisord.org
   Main PID: 494 (supervisord)
      Tasks: 4 (limit: 2306)
     Memory: 90.4M
        CPU: 2.521s
     CGroup: /system.slice/supervisor.service
             ├─494 /usr/bin/python3 /usr/bin/supervisord -n -c /etc/supervisor/>
             ├─612 /bin/bash /home/pc17-dpl/travelroad_django/run.sh
             ├─614 /home/pc17-dpl/travelroad_django/.venv/bin/python3 /home/pc1>
             └─615 /home/pc17-dpl/travelroad_django/.venv/bin/python3 /home/pc1>
```

A continuación vamos a crear un grupo supervisor y unir al usuario a este grupo para que tenga permisos y pueda utilizar la herramienta supervisorctl que proporciona supervisor. Para ello primero debemos de crear el grupo

```
sudo groupadd supervisor
```

Editamos la configuración de Supervisor:

```
sudo nano /etc/supervisor/supervisord.conf
```

Y añadimos el siguiente contenido sobre la linea 5:

```
...
chmod=0770               ; socket file mode (default 0700)
chown=root:supervisor    ; grupo 'supervisor' para usuarios no privilegiados
...
```

Justo despues de esto reinicimos el servicio:

```
sudo systemctl restart supervisor
```

Y por último añadimos al usuario al grupo creado:

```
sudo usermod -a -G supervisor pc17-dpl
```

Hecho esto, un paso recomendado es crear un script de servicio para que la propia aplicación se encargue de levantar gunicorn. Para ello, dentro del proyecto creamos un fichero run.sh con el siguiente contenido:

```
#!/bin/bash

cd $(dirname $0)
source .venv/bin/activate
gunicorn -b unix:/tmp/travelroad.sock main.wsgi:application
```

Y le damos permisos de ejecución:

```
chmod +x run.sh
```

El último paso sería la configuración del propio Supervisor. Para ello vamos a crear la configuración de un proceso supervisor que lance gunicorn como servidor de aplicación para nuestra aplicación Django. Para ello deberemos de crear un fichero de configuración de la siguiente manera:

```
sudo nano /etc/supervisor/conf.d/travelroad_django.conf
```

Con el siguiente contenido:

```
[program:travelroad_django]
user = pc17-dpl
command = /home/pc17-dpl/travelroad_django/run.sh
autostart = true
autorestart = true
stopsignal = INT
killasgroup = true
stderr_logfile = /var/log/supervisor/travelroad_django.err.log
stdout_logfile = /var/log/supervisor/travelroad_django.out.log
```

Y añadimos el proceso con los siguinetes comandos:

```
supervisorctl reread
```

```
supervisorctl add travelroad_django
```

Comprobamos el estado

```
pc17-dpl@a109pc17dpl:~$ supervisorctl status
travelroad_django                RUNNING   pid 612, uptime 3:15:55
```

#### Nginx

El paso final es la configuración del propio Nginx. Para ello creamos un fichero de configuración para nuestra aplicación:

```
sudo nano /etc/nginx/conf.d/travelroad_django.conf
```

Con el siguiente contenido:

```
server {
    server_name travelroad_django;

    location / {
        include proxy_params;
        proxy_pass http://unix:/tmp/travelroad.sock;  # socket UNIX
    }
}
```

> ***IMPORTANTE:*** si estamos capturando una terminal no hace falta capturar todo el escritorio y es importante que se vea el nombre de usuario.

Si encontramos dificultades a la hora de realizar algún paso debemos explicar esas dificultades, que pasos hemos seguido para resolverla y los resultados obtenidos.

#### ***Conclusiones***. <a name="id5"></a>

En esta parte debemos exponer las conclusiones que sacamos del desarrollo de la prácica.