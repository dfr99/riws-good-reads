# riws-good-reads <!-- omit in toc -->

[![MIT License][license-shield]][license-url]

Práctica de web scraping de RIWS 2023

## Índice <!-- omit in toc -->

* [Introducción](#introduccion)
* [Dependencias](#dependencias)
    + [Backend](#backend)
    + [Frontend](#frontend)
* [Despliegue](#despliegue)
    + [Automático](#automático)
    + [Manual](#manual)
* [Recomendaciones](#recomendaciones)
* [Autores](#autores)
* [Referencias](#referencias)

## Introducción

El proyecto consiste en obtener los datos de los libros que aparcen en listas
de [Good Reads](https://www.goodreads.com/) utilizando técnicas de
_web scraping_. Estos datos son guardados en un índice de Elasticsearch, que es
consultado por un _frontend_ para mostrar y manejar dichos datos.

## Dependencias

El proyecto ha sido desarrollado en
[Ubuntu 22.04](https://releases.ubuntu.com/jammy/). El software necesario
ha sido instalado utilizando el repositorio de paquetes
[APT](https://ubuntu.com/server/docs/package-management) o scripts de
instalación escritos en [BASH](https://es.wikipedia.org/wiki/Bash).
A continuación, se muestran las dependencias específicas para cada parte
del proyecto.

### Backend

Las dependencias del _backend_ son las siguientes:

* [Python 3.10.12](https://www.python.org/downloads/release/python-31012/)
* [Poetry 1.7.0](https://github.com/python-poetry/poetry/releases/tag/1.7.0)
* [Elasticsearch 8.11.1](https://github.com/elastic/elasticsearch/releases/tag/v8.11.1)
* Adicionalmente, se requiere de
[ChromeDriver](https://chromedriver.chromium.org/), ya que es el
navegador utilizado por la librería Selenium para interactuar con las páginas
web. Se recomienda instalar
[Google Chrome](https://www.google.com/intl/es_es/chrome/) ya que el _driver_
se instala con dicho navegador.

Dentro del fichero [code/backend/pyproject.toml](code/backend/pyproject.toml),
en la sección _tool.poetry.dependencies_, se listan las dependencias del
proyecto. Se pueden obtener el listado completo de librerías de Python con la
siguiente secuencia de comandos:

```bash
cd code/backend
poetry install
poetry shell
pip freeze
```

### Frontend
Las dependencias del _frontend_ son las siguientes:

* [React 17.0.2](https://github.com/facebook/react/blob/main/CHANGELOG.md#1702-march-22-2021)
* [ReactiveSearch 3.45](https://github.com/appbaseio/reactivesearch/releases/tag/v3.45.0)
* [Node v12.22.9](https://nodejs.org/en/blog/release/v12.22.9): utilizamos esta versión de Node por compatibilidad con
  ReactiveSearch
* [npm 8.5.1](https://www.npmjs.com/package/npm/v/8.5.1)

Dentro de la carpeta [code/frontend/package.json](code/frontend/package.json),
se encuentran definidas las dependencias mencionadas anteriormente, así como
otras librerías requeridas en el proyecto.

## Despliegue

### Automático

El script de Bash [autoinstall.sh](dist/autoinstall.sh) realiza las siguientes acciones:

* Instalación de Elasticsearch y Poetry
* Comprobación de las [dependencias](#dependencias)
* Modificación de la configuración de Elasticsearch para adecuarse al contexto
  de la práctica
* Inicialización del servicio de Elastisearch
* Creación del índice de Elasticsearch
* Ejecución del _crawler_
* Ejecución del frontal

Para ejecutarlo, con permisos de superusuario, se lanzan los siguientes
comandos:

```bash
cd dist
./autoinstall.sh <python_executable_path> <good_reads_list>
```

siendo _python_executable_path_ la ruta donde se encuentra el ejecutable de
Python (e.g python, python3, /usr/bin/python) y _good_reads_list_ la lista de
Good Reads de la que se desean extraer los datos. Este último parámetro se
extrae de la URL de la lista. Tomando como ejemplo este
[enlace](https://www.goodreads.com/list/show/3116.Best_historical_fiction_novels)
, el valor del parámetro sería **3116.Best_historical_fiction_novels**.
Esto es aplicable a todas las listas de Good Reads.

### Manual

En caso de que el script de despliegue automático no funcione, se pueden
seguir los siguientes pasos de forma manual:

* [Instalación de Google Chrome](https://www.google.com/intl/es_es/chrome/)

* Actualizar los repositorios `apt` con el comando `sudo apt update`
* Instalación de Elasticsearch

    ```bash
    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
    sudo apt-get install -y apt-transport-https
    echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
    sudo apt-get update && sudo apt-get install -y elasticsearch
    ```

* Inicialización de Elasticsearch

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable elasticsearch
    sudo systemctl start elasticsearch
    sudo systemctl status elasticsearch
    ```

* Configuración de Elasticsearch:
    + Introducir en el fichero de configuración de Elasticsearch
      (en Ubuntu, en la ruta `/etc/elasticsearch/elasticsearch.yml`)

        ```yml
        ## Remove security
        xpack.security.enabled: false
        xpack.security.enrollment.enabled: false

        ## Allow CORS
        http.cors.enabled: true
        http.cors.allow-origin: "*"
        http.cors.allow-methods: OPTIONS, HEAD, GET, POST, PUT, DELETE
        http.cors.allow-headers: X-Requested-With, X-Auth-Token, Content-Type, Content-Length
        http.cors.allow-credentials: true
        ```

* Reinicio de Elasticsearch para aplicar los nuevos cambios en la configuración
  y comprobación de la instalación

    ```bash
    sudo systemctl restart elasticsearch
    curl -X GET 'http://localhost:9200'
    ```

* Crear el índice en Elasticsearch

    ```bash
    # Asegurarse de que no existe el índice que se va a utilizar
    curl -X DELETE 'localhost:9200/good_reads?pretty'

    # Creación del índice
    curl -X PUT 'localhost:9200/good_reads?pretty'
    ```

* Instalación de Poetry

    ```bash
    curl -sSL https://install.python-poetry.org | python -
    poetry self update 1.7.0
    poetry --version
    ```

* Instalación de Node y npm

    ```bash
    # Si se utiliza Ubuntu 22.04, en los repositorios apt, la última version
    # disponible es la v12.29.9, válida para este proyecto
    sudo apt install nodejs
    # En otro caso, instalar Node utilizando el script de instalación
    curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
    sudo apt install npm
    node -v
    npm -v
    ```

* En el fichero `code/backend/good_reads/spiders/.env`, modificar la variable de
entorno `GOOD_READS_LIST` con en nombre de la lista de la que se deseen extraer
los datos de los libros. Alternativamente, se puede hacer usando el CLI con el
siguiente comando:

    ```bash
    echo 'GOOD_READS_LIST=<good_reads_list>' > code/backend/good_reads/spiders/.env
    ```

* Ejecutar los siguientes comandos para lanzar el _crawler_ y levantar el frontal

    ```bash
    cd code/backend
    poetry install
    poetry run crawl

    # Una vez termine el comando anterior
    cd ../frontend
    npm install
    npm start
    ```

## Recomendaciones

* Se recomienda utilizar, para la ejecución de la práctica, un SO basado en
  Linux que utilice APT como gestor de paquetes y BASH como intérprete de
  comandos. Concretamente, se aconseja utilizar Ubuntu 22.04.
* Como primera opción, lanzar el [despliegue autómatico](#automatico).
  Recurrir a la [instalación manual](#manual) solo en caso de error.

## Autores

* David Fraga Rodríguez (david.fraga.rodriguez@udc.es)
* María Rey Escobar (maria.rescobar@udc.es)

## Referencias

* [Link del proyecto](https://github.com/dfr99/riws-good-reads)

<!-- VARIABLES -->
[license-shield]:https://img.shields.io/badge/License-MIT-yellow.svg
[license-url]: https://github.com/torusware/ami-backup-lambdas/blob/main/LICENSE
