[![MIT License][license-shield]][license-url]

# riws-good-reads <!-- omit in toc -->
Práctica de web scraping de RIWS 2023

## Índice <!-- omit in toc -->

- [Introducción](#introduccion)
- [Dependencias](#dependencias)
	+ [Backend](#backend)
	+ [Frontend](#frontend)
- [Despliegue](#despliegue)
	+ [Automático (solo en Linux)](#automático-solo-en-linux)
	+ [Manual](#manual)
- [Autores](#autores)
- [Referencias](#referencias)

## Introducción

El proyecto consiste en obtener los datos de los libros que aparcen en listas de [Good Reads](https://www.goodreads.com/) utilizando técnicas de _web scraping_. Estos datos son guardados en un índice de Elasticsearch, que es consultado por un _frontend_ para mostrar y manejar dichos datos.

## Dependencias

### Backend

Las dependencias del _backend_ son las siguientes:

- [Python 3.10.12](https://www.python.org/downloads/release/python-31012/)
- [Poetry 1.7.0](https://python-poetry.org/docs/)
- [Elasticsearch 8.11.1](https://github.com/elastic/elasticsearch/releases/tag/v8.11.1)

Dentro del fichero [code/backend/pyproject.toml](code/backend/pyproject.toml), en la sección _tool.poetry.dependencies_, se listan las dependencias del proyecto. Se pueden obtener el listado completo de librerías de Python con la siguiente secuencia de comandos:

```bash
cd code/backend
poetry install
poetry shell
pip freeze
```

### Frontend



## Despliegue

### Automático (solo en Linux)
El script de Bash [autoinstall.sh](dist/autoinstall.sh) realiza las siguientes acciones:

- Instalación y comprobación de las [dependencias](#dependencias)
- Modificación de la configuración de Elasticsearch para adecuarse al contexto de la práctica
- Inicialización del servicio de Elastisearch
- Creación del índice de Elasticsearch
- Ejecución del _crawler_
- Ejecución del frontal

Para ejecutarlo, con permisos de superusuario, se lanzan los siguientes comandos:

```bash
cd dist
./autoinstall.sh <python_executable_path> #e.g python, python3, /usr/bin/python
```

### Manual

En caso de que el script de despliegue automático no funcione, se deben seguir los siguientes pasos de forma manual:

- Instalación de Elasticsearch
- Configuración de Elasticsearch:
	+ Introducir en el fichero de configuración de Elasticsearch 
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
- Instalación de Poetry
- Ejecutar los siguientes comandos

## Autores

- David Fraga Rodríguez (david.fraga.rodriguez@udc.es)
- María Rey Escobar (maria.rescobar@udc.es)

## Referencias

- [Link del proyecto](https://github.com/dfr99/riws-good-reads)

<!-- VARIABLES -->
[license-shield]:https://img.shields.io/badge/License-MIT-yellow.svg
[license-url]: https://github.com/torusware/ami-backup-lambdas/blob/main/LICENSE
