# Project 1


## Setting up the repository

1. Run `python -m venv venv` to create your virtual environment
2. Run `source venv/bin/activate` to activate the virtual environment
3. Run `pip install -r requirements.txt` to install the full list of requirements

## Fixing shp file
1. Run `pip install gdal`
2. Run `ogr2ogr -f "ESRI Shapefile" repaired_shapefile.shp TrainStation_Jul2024\ 21-36-40-252/RapidTransitSystemStation.shp -nlt POLYGON -makevalid`

## Pre-requisites for running app interface
1. [Maven 3](https://maven.apache.org/download.cgi) for building the application

2. [MySQL Server](https://dev.mysql.com/downloads/mysql/) to host the database locally

   Configure the server to run on port `3306` (default port) and run the following queries to initialise the database:
    ```sql
    create database my_database
    create user 'my_user' identified by 'password'
    ```
### Running the application

1. In the root folder, start the springboot backend using `./mvnw spring-boot:run`
   - Ensure that the database server is running
   - Ensure that the database configuration in `src/main/resources/application.properties` is correct (**do not push** if you change it)

2. Start the frontend by doing the following:
   ```bash
   cd frontend
   npm install # if you are running for the first time
   npm run dev
   ```
## API Endpoints
