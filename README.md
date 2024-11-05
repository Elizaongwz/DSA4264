# Geospatial Analysis of Bus Services against Train Lines

## Setting up the repository
1. Run `python -m venv venv` to create your virtual environment
2. Run `source venv/bin/activate` to activate the virtual environment
3. Run `pip install -r requirements.txt` to install the full list of requirements

## Fixing shp file
1. Run `pip install gdal`
2. Run `ogr2ogr -f "ESRI Shapefile" repaired_shapefile.shp TrainStation_Jul2024\ 21-36-40-252/RapidTransitSystemStation.shp -nlt POLYGON -makevalid`

## Backend: Sequence 

### Obtaining Data and Extracted Features
Run the 'API Calls and Data Extraction' notebook to retrieve relevant datasets from the LTA DataMall platform as well as to clean and extract necessary features.
Follow the instructions above to correct the shapefile retrieved from LTA DataMall.

### Parallel Scoring Algorithm
Run the 'parallelscore' notebook to calculate and rank the parallelism scores for all trunk services.

### Modifying Bus Services
Before working with map visualisations, run 'mrt_map.py' and 'bus_route_plot.py' in the terminal. This ensures these files are available for import without errors. 
Run the 'Modifying Parallel Bus Routes' notebook to generate proposed adjustments for the trunk services.

### Proposed Routes
The 'proposed_routes' notebook documents the reasoning and methodology for each of the three suggested routes, including visualisations for each proposal.

## Frontend: Sequence
### Pre-requisites for running app interface
1. [Maven 3](https://maven.apache.org/download.cgi) for building the application

2. [MySQL Server](https://dev.mysql.com/downloads/mysql/) to host the database locally

   Configure the server to run on port `3306` (default port) and run the following queries to initialise the database:
    ```sql
    create database my_database
    create user 'my_user' identified by 'password'
    ```
3. Ensure all csv files for bus routes, bus services, train lines are called using your API key. Simply run the notebook `Bus Data Cleaning.ipynb` to get this

### Running the application

1. Start Flask application from command line using `python app.py`

2. Go to root folder using `cd interface` in another terminal

3. In the root folder, start the springboot backend using `./mvnw spring-boot:run`
   - Ensure that the database server is running
   - Ensure that the database configuration in `src/main/resources/application.properties` is correct (**do not push** if you change it)

4. Start the frontend by doing the following:
   ```bash
   cd bus-visualization
   npm install # if you are running for the first time
   npm run start
   ```
### Development server
1. To reset the map, simply refresh the page
   
## API Endpoints
| Method    | Endpoint          | Request Body  | Response |
|:------------:|:------------:|:------------:|:------------:|
| GET  | /bus_routes | - | List of bus routes once user clicks on dropdown menu|
| GET  | /proposed_routes | - | List of proposed bus routes once user clicks on dropdown menu|
| GET  | /modified_routes | - | List of modified bus routes once user clicks on dropdown menu|
| GET  | /train_lines | - | Trains lines visualisation on leaflet map|
| POST  | /plot_routes   |  service_no: String|geoJSON data of bus route coordinates plotted onto map|
| POST  | /plot_proposed_routes   |  service_name: String|geoJSON data of proposed bus route coordinates plotted onto map|
| POST  | /plot_modified_routes   |  service_no: String|geoJSON data of modified bus route coordinates plotted onto map|
| POST      | /parallel_score   | service_no: String | Normalised parallelism score of bus routes with mrt lines appears |
| POST      | /rank   | service_no: String | Rank of parallelism score of bus routes with mrt lines appears |

