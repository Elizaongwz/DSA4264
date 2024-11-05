import folium
import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, LineString, mapping
from shapely.ops import nearest_points
import math
import numpy as np
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# Load all the necessary datasets
data_dir = "Bus_RoutesStopsServices"  # Directory where bus data is stored
bus_routes = pd.read_csv(f"{data_dir}/bus_routes.csv")  # Load bus routes data
bus_services = pd.read_csv(f"{data_dir}/bus_services.csv")  # Load bus services data
bus_stops = pd.read_csv(f"{data_dir}/bus_stops.csv")  # Load bus stops data
proposed_bus_routes = pd.read_csv(f"{data_dir}/proposed_bus_route.csv")  # Load proposed bus routes data
modified_bus_routes = pd.read_csv("top_10_buses_new_routes_only.csv", dtype={'ServiceNo': str})  # Load modified bus routes data  # Load modified bus routes data
train_stations = gpd.read_file("TrainStation_Jul2024/repaired_shapefile.shp")  # Load train stations shapefile
parallel_data = pd.read_csv("Bus_RoutesStopsServices/paralleltrunkservicesranked.csv")  # Load parallelism score and rank data

# Filter out trunk services from bus services
trunk = bus_services[bus_services['Category'] == 'TRUNK']

# Merge bus routes with trunk services to get only trunk routes
merged_data = pd.merge(bus_routes, trunk[['ServiceNo']], on='ServiceNo', how='inner')

# Merge the result with bus stop coordinates
final_data = pd.merge(merged_data, bus_stops, on='BusStopCode', how='left')

# Create dictionaries for parallelism scores and ranks
service_parallelism_dict = dict(zip(parallel_data['ServiceNo'], parallel_data['Score']))
rank_parallelism_dict = dict(zip(parallel_data['ServiceNo'], parallel_data['Rank']))

# Initialize Flask app and allow CORS (Cross-Origin Resource Sharing)
app = Flask(__name__)
CORS(app)

# API endpoint to return all available bus routes
@app.route('/api/bus_routes', methods=['GET'])
def get_bus_routes():
    try:
        # Return unique list of service numbers (bus routes)
        bus_routes = final_data['ServiceNo'].unique().tolist()
        return jsonify(bus_routes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error if something goes wrong

# API endpoint to return modified bus routes
@app.route('/api/modified_routes', methods=['GET'])
def get_modified_bus_routes():
    try:
        # Return unique list of modified service numbers (bus routes)
        bus_routes = modified_bus_routes['ServiceNo'].unique().tolist()
        return jsonify(bus_routes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error if something goes wrong

# API endpoint to return proposed bus routes
@app.route('/api/proposed_routes', methods=['GET'])
def get_proposed_routes():
    try:
        # Return unique list of proposed service names (bus routes)
        bus_routes = proposed_bus_routes['ServiceName'].unique().tolist()
        return jsonify(bus_routes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error if something goes wrong

# Function to convert non-serializable data (e.g., numpy types) to serializable data for JSON responses
def convert_to_serializable(obj):
    if isinstance(obj, np.int64):
        return int(obj)  # Convert numpy int64 to standard int
    if isinstance(obj, np.float64):
        return float(obj)  # Convert numpy float64 to standard float
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert numpy array to list
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}  # Recursively convert dicts
    if isinstance(obj, list):
        return [convert_to_serializable(i) for i in obj]  # Recursively convert lists
    return obj  # Return original object if it doesn't need conversion

# Function to generate train line GeoJSON data
@app.route('/api/train_lines', methods=['GET'])
def get_train_lines():
    # Dictionary mapping train line names to their stations
    mrt_lines = {
        'Thomson-East Coast Line': ['WOODLANDS NORTH MRT STATION','WOODLANDS MRT STATION','WOODLANDS SOUTH MRT STATION', 'SPRINGLEAF MRT STATION','LENTOR MRT STATION','MAYFLOWER MRT STATION','BRIGHT HILL MRT STATION',
                                    'UPPER THOMSON MRT STATION','CALDECOTT MRT STATION','STEVENS MRT STATION','NAPIER MRT STATION','ORCHARD BOULEVARD MRT STATION','ORCHARD MRT STATION','GREAT WORLD MRT STATION',
                                    'HAVELOCK MRT STATION','OUTRAM PARK MRT STATION','MAXWELL MRT STATION','SHENTON WAY MRT STATION','MARINA BAY MRT STATION','GARDENS BY THE BAY MRT STATION','TANJONG RHU MRT STATION',
                                    'KATONG PARK MRT STATION','TANJONG KATONG MRT STATION','MARINE PARADE MRT STATION','MARINE TERRACE MRT STATION','SIGLAP MRT STATION','BAYSHORE MRT STATION'],
        'North-South Line': ['JURONG EAST MRT STATION','BUKIT BATOK MRT STATION','BUKIT GOMBAK MRT STATION','CHOA CHU KANG MRT STATION','YEW TEE MRT STATION','KRANJI MRT STATION','MARSILING MRT STATION','WOODLANDS MRT STATION',
                            'ADMIRALTY MRT STATION','SEMBAWANG MRT STATION','CANBERRA MRT STATION','YISHUN MRT STATION','KHATIB MRT STATION','YIO CHU KANG MRT STATION','ANG MO KIO MRT STATION','BISHAN MRT STATION',
                            'BRADDELL MRT STATION','TOA PAYOH MRT STATION','NOVENA MRT STATION','NEWTON MRT STATION','ORCHARD MRT STATION','SOMERSET MRT STATION','DHOBY GHAUT MRT STATION','CITY HALL MRT STATION',
                            'RAFFLES PLACE MRT STATION','MARINA BAY MRT STATION','MARINA SOUTH PIER MRT STATION'],
        'Circle Line': ['DHOBY GHAUT MRT STATION', 'BRAS BASAH MRT STATION', 'ESPLANADE MRT STATION', 'PROMENADE MRT STATION','NICOLL HIGHWAY MRT STATION','STADIUM MRT STATION',
                        'MOUNTBATTEN MRT STATION','DAKOTA MRT STATION','PAYA LEBAR MRT STATION','MACPHERSON MRT STATION','TAI SENG MRT STATION','BARTLEY MRT STATION','SERANGOON MRT STATION','LORONG CHUAN MRT STATION',
                        'BISHAN MRT STATION','MARYMOUNT MRT STATION','CALDECOTT MRT STATION','BOTANIC GARDENS MRT STATION','FARRER ROAD MRT STATION','HOLLAND VILLAGE MRT STATION','BUONA VISTA MRT STATION','ONE-NORTH MRT STATION',
                        'KENT RIDGE MRT STATION', 'HAW PAR VILLA MRT STATION', 'PASIR PANJANG MRT STATION', 'LABRADOR PARK MRT STATION', 'TELOK BLANGAH MRT STATION','HABOURFRONT MRT STATION'],
        'Circle Line ': ['PROMENADE MRT STATION','BAYFRONT MRT STATION', 'MARINA BAY MRT STATION'],
        'North-East Line': ['HARBOURFRONT MRT STATION','OUTRAM PARK MRT STATION','CHINATOWN MRT STATION','CLARKE QUAY MRT STATION','DHOBY GHAUT MRT STATION','LITTLE INDIA MRT STATION','FARRER PARK MRT STATION','BOON KENG MRT STATION',
                            'POTONG PASIR MRT STATION','WOODLEIGH MRT STATION','SERANGOON MRT STATION','KOVAN MRT STATION','HOUGANG MRT STATION','BUANGKOK MRT STATION','SENGKANG MRT STATION','PUNGGOL MRT STATION'],
        'Downtown Line': ['BUKIT PANJANG MRT STATION', 'CASHEW MRT STATION', 'HILLVIEW MRT STATION', 'HUME MRT STATION', 'BEAUTY WORLD MRT STATION', 'KING ALBERT PARK MRT STATION', 'SIXTH AVENUE','TAN KAH KEE MRT STATION',
                        'BOTANIC GARDENS MRT STATION', 'STEVENS MRT STATION', 'NEWTON MRT STATION', 'LITTLE INDIA MRT STATION', 'ROCHOR MRT STATION', 'BUGIS MRT STATION', 'PROMENADE MRT STATION', 'BAYFRONT MRT STATION',
                        'DOWNTOWN MRT STATION', 'TELOK AYER MRT STATION', 'CHINATOWN MRT STATION', 'FORT CANNING MRT STATION', 'BENCOOLEN MRT STATION', 'JALAN BESAR MRT STATION', 'BENDEMEER MRT STATION', 'GEYLANG BAHRU MRT STATION',
                        'MATTAR MRT STATION', 'MACPHERSON MRT STATION', 'UBI MRT STATION', 'KAKI BUKIT MRT STATION', ' BEDOK NORTH MRT STATION', 'BEDOK RESERVOIR MRT STATION', 'TAMPINES WEST MRT STATION',
                        'TAMPINES MRT STATION', 'TAMPINES EAST MRT STATION', 'UPPER CHANGI MRT STATION', 'EXPO MRT STATION'],
        'East-West Line': ['PASIR RIS MRT STATION', 'TAMPINES MRT STATION', 'SIMEI MRT STATION', 'TANAH MERAH MRT STATION','BEDOK MRT STATION', 'KEMBANGAN MRT STATION', 'EUNOS MRT STATION', 'PAYA LEBAR MRT STATION',
                        'ALJUNIED MRT STATION', 'KALLANG MRT STATION', ' LAVENDER MRT STATION','BUGIS MRT STATION', 'CITY HALL MRT STATION', 'RAFFLES PLACE MRT STATION','TANJONG PAGAR MRT STATION', 'OUTRAM PARK MRT STATION',
                        'TIONG BAHRU MRT STATION', 'REDHILL MRT STATION', 'QUEENSTOWN MRT STATION', 'COMMONWEALTH MRT STATION','BUONA VISTA MRT STATION', 'DOVER MRT STATION', 'CLEMENTI MRT STATION', 'JURONG EAST MRT STATION',
                        'CHINESE GARDEN MRT STATION', 'LAKESIDE MRT STATION', 'BOON LAY MRT STATION', 'PIONEER MRT STATION','JOO KOON MRT STATION','GUL CIRCLE MRT STATION', 'TUAS CRESCENT MRT STATION', 
                        'TUAS WEST ROAD MRT STATION', 'TUAS LINK MRT STATION'],
        'East-West Line ':['TANAH MERAH MRT STATION','EXPO MRT STATION', 'CHANGI AIRPORT MRT STATION']
    }
    # Dictionary mapping MRT lines to their corresponding colour
    line_colors = {
        'North-South Line': 'red',
        'East-West Line': 'green',
        'East-West Line ': 'green',
        'Circle Line': 'darkorange',
        'Circle Line ': 'darkorange',
        'North-East Line': 'purple',
        'Downtown Line': 'blue',
        'Thomson-East Coast Line': 'brown'
    }
    # List to store MRT line data
    mrt_line_data = []
    for line, stations in mrt_lines.items():
        for index, station in enumerate(stations):
            mrt_line_data.append((station, line, index+1))
    
    # Merging datasets together to create DataFrame for MRT line data
    mrt_line_df = pd.DataFrame(mrt_line_data, columns=['STN_NAM_DE', 'MRT_LINE', 'STN_SEQUENCE'])
    train_stations_merged = train_stations.merge(mrt_line_df, on='STN_NAM_DE', how='left')
    # Remove duplicates and set the coordinate system (CRS)
    merged_stations_unique = train_stations_merged.drop_duplicates(subset=['STN_NAM_DE', 'MRT_LINE'])
    merged_stations_unique = merged_stations_unique.to_crs(epsg=4326)
    # Convert geometry to centroid
    merged_stations_unique['geometry'] = merged_stations_unique['geometry'].centroid
    merged_stations_unique = merged_stations_unique.to_crs(epsg=4326)
    # Group the stations by MRT line
    grouped_train_lines = merged_stations_unique.groupby(['MRT_LINE']).apply(lambda x: x[['STN_NAM_DE', 'STN_SEQUENCE','geometry']])
    grouped_train_lines = grouped_train_lines.sort_values(['MRT_LINE','STN_SEQUENCE'])

    grouped_train_lines = grouped_train_lines.to_crs(epsg=4326)
    # Prepare GeoJSON FeatureCollection
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Generate GeoJSON for MRT lines
    for MRT_LINE, group in grouped_train_lines.groupby(level='MRT_LINE'):
        group_sorted = group.sort_values('STN_SEQUENCE')
        train_coordinates = group_sorted['geometry'].centroid.apply(lambda geom: (geom.x, geom.y)).tolist()
        train_route_line = LineString(train_coordinates)

        # Add a new feature for the MRT line
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": train_coordinates
            },
            "properties": {
                "line_name": MRT_LINE,
                "color": line_colors.get(MRT_LINE, 'black')  # Get the color for this line
            }
        }

        geojson_data["features"].append(feature)

    # Recursively convert all non-serializable types to serializable types
    serializable_geojson = convert_to_serializable(geojson_data)

    # Return the GeoJSON data as a JSON response
    return jsonify(serializable_geojson)


# Endpoint to plot bus routes (returns GeoJSON for selected bus route)
@app.route('/api/plot_routes', methods=['POST'])
def plot_routes():
    selected_service_no = request.json['service_no']  # Get the selected bus service number from request body

    # Filter bus routes for the selected service number
    busroutes = final_data[final_data['ServiceNo'].isin([selected_service_no])]
    grouped_bus_routes = busroutes.groupby(['ServiceNo', 'Direction'])

    # Generate GeoJSON data for bus routes
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Create a LineString for each bus route and add it to GeoJSON data
    for (service_no, direction), group in grouped_bus_routes:
        bus_coordinates = list(zip(group['Longitude'], group['Latitude']))
        bus_route_line = LineString(bus_coordinates)

        feature = {
            "type": "Feature",
            "geometry": mapping(bus_route_line),
            "properties": {
                "service_no": service_no,
                "direction": direction
            }
        }
        geojson_data["features"].append(feature)

    # Add bus stop points to GeoJSON data
    for index, row in busroutes.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['Longitude'], row['Latitude']]
            },
            "properties": {
                "bus_stop_code": row['BusStopCode'],
                "service_no": row['ServiceNo']
            }
        }
        geojson_data["features"].append(feature)

    # Convert to serializable types and return the GeoJSON data
    serializable_geojson = convert_to_serializable(geojson_data)
    return jsonify(serializable_geojson)

# Similar endpoint to plot modified bus routes
@app.route('/api/plot_modified_routes', methods=['POST'])
def plot_modified_routes():
    selected_service_no = request.json['service_no']
    
    # Filter the bus routes for the selected service number
    busroutes = modified_bus_routes[modified_bus_routes['ServiceNo'].isin([selected_service_no])]

    grouped_bus_routes = busroutes.groupby(['ServiceNo'])

    # Prepare a GeoJSON FeatureCollection
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Generate GeoJSON for bus routes (lines)
    for (service_no), group in grouped_bus_routes:
        group_sorted = group.sort_values('StopSequence')
        bus_coordinates = list(zip(group_sorted['Longitude'], group_sorted['Latitude']))
        bus_route_line = LineString(bus_coordinates)

        # Add a new feature for the bus route
        feature = {
            "type": "Feature",
            "geometry": mapping(bus_route_line),  # Convert LineString to GeoJSON format
            "properties": {
                "service_no": service_no,
            }
        }
        geojson_data["features"].append(feature)

    # Add GeoJSON for bus stop points
    for index, row in busroutes.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['Longitude'], row['Latitude']]
            },
            "properties": {
                "bus_stop_code": row['BusStopCode'],
                "service_no": row['ServiceNo']
            }
        }
        geojson_data["features"].append(feature)

    # Recursively convert all non-serializable types (e.g., np.int64) to serializable types
    serializable_geojson = convert_to_serializable(geojson_data)

    # Return the GeoJSON data as a JSON response
    return jsonify(serializable_geojson)

# Similar endpoint to plot proposed bus routes
@app.route('/api/plot_proposed_routes', methods=['POST'])
def plot_proposed_routes():
    selected_service_name = request.json['service_name']
    
    # Filter the bus routes for the selected service number
    busroutes = proposed_bus_routes[proposed_bus_routes['ServiceName'].isin([selected_service_name])]

    grouped_bus_routes = busroutes.groupby(['ServiceName'])

    # Prepare a GeoJSON FeatureCollection
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Generate GeoJSON for bus routes (lines)
    for (service_name), group in grouped_bus_routes:
        group_sorted = group.sort_values('Stop Sequence')
        bus_coordinates = list(zip(group_sorted['Longitude'], group_sorted['Latitude']))
        bus_route_line = LineString(bus_coordinates)

        # Add a new feature for the bus route
        feature = {
            "type": "Feature",
            "geometry": mapping(bus_route_line),  # Convert LineString to GeoJSON format
            "properties": {
                "service_name": service_name,
            }
        }
        geojson_data["features"].append(feature)

    # Add GeoJSON for bus stop points
    for index, row in busroutes.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['Longitude'], row['Latitude']]
            },
            "properties": {
                "bus_stop_code": row['BusStopCode'],
                "service_name": row['ServiceName']
            }
        }
        geojson_data["features"].append(feature)

    # Recursively convert all non-serializable types (e.g., np.int64) to serializable types
    serializable_geojson = convert_to_serializable(geojson_data)

    # Return the GeoJSON data as a JSON response
    return jsonify(serializable_geojson)



# Endpoint for returning parallel score
@app.route('/api/parallel_score', methods=['POST'])
def parallel_score():
    try:
        # Extract service number from the JSON request body
        service_no = request.json['service_no']
        score = service_parallelism_dict.get(service_no)
        return jsonify(score)
    
    except Exception as e:
        # Handle any errors that occur and return an error message
        return jsonify({'error': str(e)}), 500

# Endpoint for returning rank based on parallel sore
@app.route('/api/rank', methods=['POST'])
def rank():
    try:
        # Extract service number from the JSON request body
        service_no = request.json['service_no']
        rank = rank_parallelism_dict.get(service_no)
        return jsonify(rank)
    
    except Exception as e:
        # Handle any errors that occur and return an error message
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)




