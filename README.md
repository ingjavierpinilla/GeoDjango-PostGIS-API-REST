# Magentrack Test

Creacion de API REST para almacenar datasets de elementos geograficos usando Django y PostgreSQL

# Caracteristicas

  - Permite a los usuarios cargar un archivo en formato CSV por medio de
un método POST para ser almacenado en una base de datos PostgreSQL.
  - Convierte las propiedades latitude y longitude a un punto en postgis.
  - Endpoint para obtener un registro de todos los datasets con una paginación de 5 registros.
  - Endpoint para obtener listado de filas guardados en la base de datos correspondientes a un determinado dataset.
  - Permite filtrar los registros por medio de query params, los campos que por los que se puede filtrar son:
    - dataset_id
    - name
    - point
- El query param dataset_id es obligatorio. Y de no ser enviado notifica al usuario en un mensaje personalizado.
- Cuenta con un sistema de logger en MongoDB, este debe guardar cada consumo del API en donde se registren los siguientes datos:
    - IP
    - Fecha y hora en utc
    - usuario que genero el consumo del API
- Posee una vista basica hecha con el framework https://getbootstrap.com/ y utiliza el plugin https://bootstrap-table.com/ para mostrar el sistema de Logger almacenado en MongoDB.
- Se creó un Classview de Django y retornar la consulta de MongoDB de los datos del Logger en formato json para mostrarlo en una tabla de Bootstrap Table.
- Para el consumo del objeto Json se usa la librería axios y cargar los
datos al objeto de Bootstrap table.
- Tiene un control de errores personalizados es decir, si para los métodos POST no se envían correctamente los valores el API debe responder e informar la razón del error.
- Todos los endpoint del API cuentan con autenticación con JWT.
- Test unitarios para las vistas y modelos.

### Tegnologías

El API REST fue creado empleado los siguientes recursos

* [Docker] 
* [Python] - Imagen 3.8.7-slim
* [PostGIS] - Imagen PostGIS de kartoza version 12.1
* [MongoDB]
* [Bootstrap] 
* [Bootstrap-table]


### Docker
Se creo un archivo docker-compose que se encarga de lanzar contenedores de Python exponiendo el puerto 8000, PostGIS con el puerto 5432 y MongoDB en el 27017.

Por favor tenga en cuenta que antes de realizar cualquier procedimiento debe crear las correspondientes variables de entorno, los archivos Dockerfile y ./app/app/settings.py requieren de las siguientes variables de entorno:
- Dockerfile
    - POSTGRES_USER
    - POSTGRES_PASSWORD
    - POSTGRES_DB
    - MONGO_USER
    - MONGO_PASSWORD
- ./app/app/settings.py
    - POSTGRES_PASSWORD
    - POSTGRES_DB
    - POSTGRES_USER
    - MONGO_USER
    - MONGO_HOST
    - MONGO_DB
    - MONGO_PORT
    - MONGO_PASSWORD

Para construir el proyecto ejecute:
```sh
cd magentrack-test
docker-compose build 
```
Esto compilara el proyecto local y hara pull a las imagenes necesarias.

Los nombres correspondientes para los contenedores son:
- Python -> app
- PostGIS -> postgis
- MongoDB -> mongodb

Una vez realizado proceda a realizar las migraciones y migrar la base de datos (el repositorio no cuenta con ella). Ya que el proyecto de django depende de las bases de datos se usa un script que espera hasta que estas se encuentren disponibles. Ejecute: 
```sh
docker-compose run app sh -c "../wait && python manage.py makemigrations"
docker-compose run app sh -c "../wait && python manage.py migrate"
```
Finalmente puede lanzar el proyecto usando: 

```sh
docker-compose up
```
El proyecto estara corriendo en la direccion IP 
```sh
127.0.0.1:8000
```



### Todos

 - Permitir al administrador cambiar la paginación.

Licencia
----

MIT



   [Docker]: <https://www.docker.com>
   [Python]: <https://hub.docker.com/_/python>
   [PostGIS]: <https://hub.docker.com/r/kartoza/postgis/>
   [MongoDB]: <https://hub.docker.com/_/mongo>
   [Bootstrap]: <https://getbootstrap.com/> 
   [Bootstrap-table]: <https://bootstrap-table.com/>

