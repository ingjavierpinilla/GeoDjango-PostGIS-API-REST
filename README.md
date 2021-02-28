# GeoDjango PostGIS API REST

Creation of REST API to store datasets of geographic elements using Django and PostgreSQL

# Features
![ds_structure](https://github.com/ingjavierpinilla/GeoDjango-PostGIS-API-REST/blob/main/ds_structure.png?raw=true)

  - Allows users to upload a file in CSV format via a POST method to be stored in a PostgreSQL database.
a POST method to be stored in a PostgreSQL database.
    - The data in the CSV file has the following format:
    
           latitude,longitude,client_id,client_name
           14.4234,-23.1236,21,walruss
           15.2351,-25.2426,23,hirsch
           16.6386,-75.4447,24,schmeterling
  - Convert latitude and longitude properties to a point in postgis.
  - It has:
    - Endpoint to obtain a record of all datasets with a pagination of 5 records.
    - Endpoint to obtain a list of rows stored in the database corresponding to a given dataset..
  - It allows to filter the records by means of query params, the fields that can be filtered by are:
    - dataset_id
    - name
    - point
- The dataset_id parameter of the query is mandatory. And if it is not sent it notifies the user in a custom message.
- It has a logger system in MongoDB, which must store each API consumption where the following data is recorded:
    - IP address.
    - Date and UTC - time.
    - user who used the API.
- It has a basic view made with the framework https://getbootstrap.com/ and uses the plugin https://bootstrap-table.com/ to display the Logger system stored in MongoDB.
- A Django Classview was created and return the MongoDB query of the Logger data in json format to display it in a Bootstrap Table..
- For the consumption of the Json object, the axios library is used to load the data to the Bootstrap table object.
- It has a custom error control, i.e. if for POST methods the values are not sent correctly, the API must respond and report the reason for the error..
- All API endpoints are JWT-authenticated.
- Unit tests for views and models.

### Technologies

The REST API was created using the following resources

* [Docker] 
* [Python] - Image 3.8.7-slim
* [PostGIS] - Image PostGIS from kartoza version 12.1
* [MongoDB]
* [Bootstrap] 
* [Bootstrap-table]


### Docker
A docker-compose file was created that is responsible for launching Python containers exposing port 8000, PostGIS with port 5432 and MongoDB on 27017.

Please note that before performing any procedure you must create the corresponding environment variables, the Dockerfile and ./app/app/settings.py files require the following environment variables:
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

To build the project execute:
```sh
cd magentrack-test
docker-compose build 
```
This will compile the local project and pull the necessary images.

The corresponding names for the containers are:
- Python -> app
- PostGIS -> postgis
- MongoDB -> mongodb

Once done, proceed to perform the migrations and migrate the database (the repository does not have it). Since the django project depends on databases, a script is used to wait until they are available. Execute: 
```sh
docker-compose run app sh -c "../wait && python manage.py makemigrations"
docker-compose run app sh -c "../wait && python manage.py migrate"
```
Finally you can launch the project using: 

```sh
docker-compose up
```
The project will be running on the following IP address 
```sh
127.0.0.1:8000
```



### To Do

 - Allow the administrator to change the pagination.

Licencia
----

MIT



   [Docker]: <https://www.docker.com>
   [Python]: <https://hub.docker.com/_/python>
   [PostGIS]: <https://hub.docker.com/r/kartoza/postgis/>
   [MongoDB]: <https://hub.docker.com/_/mongo>
   [Bootstrap]: <https://getbootstrap.com/> 
   [Bootstrap-table]: <https://bootstrap-table.com/>

