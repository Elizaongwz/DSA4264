import folium
import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, LineString, mapping
from shapely.ops import nearest_points
import math
import numpy as np
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS


data_dir = "Bus_RoutesStopsServices"
bus_routes = pd.read_csv(f"{data_dir}/bus_routes.csv")
bus_services = pd.read_csv(f"{data_dir}/bus_services.csv")
bus_stops = pd.read_csv(f"{data_dir}/bus_stops.csv")

# bus services data: filter for trunk, and direction = 1
trunk = bus_services[bus_services['Category'] == 'TRUNK']
#trunk = trunk[trunk['Direction'] == 1]

#bus routes data: filter for direction = 1 and trunk buses
#bus_routes = bus_routes[bus_routes['Direction'] == 1]
merged_data = pd.merge(bus_routes, trunk[['ServiceNo']], on='ServiceNo', how='inner')

# join to get the bus stop coordinates
final_data = pd.merge(merged_data, bus_stops, on='BusStopCode', how='left')

train_stations = gpd.read_file("TrainStation_Jul2024/repaired_shapefile.shp")

parallel_data = pd.read_csv("Bus_RoutesStopsServices/paralleltrunkservicesranked.csv")
service_parallelism_dict = dict(zip(parallel_data['ServiceNo'], parallel_data['ParallelismScore']))
app = Flask(__name__)
CORS(app)

# Endpoint to return all available bus routes
@app.route('/api/bus_routes', methods=['GET'])
def get_bus_routes():
    try:
        bus_routes = final_data['ServiceNo'].unique().tolist()
        return jsonify(bus_routes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def convert_to_serializable(obj):
    if isinstance(obj, np.int64):  # Convert numpy int64 to int
        return int(obj)
    if isinstance(obj, np.float64):  # Convert numpy float64 to float
        return float(obj)
    if isinstance(obj, np.ndarray):  # Convert numpy arrays to lists
        return obj.tolist()
    if isinstance(obj, dict):  # Recursively convert dicts
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):  # Recursively convert lists
        return [convert_to_serializable(i) for i in obj]
    return obj

@app.route('/api/train_lines', methods=['GET'])
def get_train_lines():
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

    mrt_line_data = []
    for line, stations in mrt_lines.items():
        for index, station in enumerate(stations):
            mrt_line_data.append((station, line, index+1))
    
    # merging datasets together 
    mrt_line_df = pd.DataFrame(mrt_line_data, columns=['STN_NAM_DE', 'MRT_LINE', 'STN_SEQUENCE'])
    train_stations_merged = train_stations.merge(mrt_line_df, on='STN_NAM_DE', how='left')
    merged_stations_unique = train_stations_merged.drop_duplicates(subset=['STN_NAM_DE', 'MRT_LINE'])
    merged_stations_unique = merged_stations_unique.to_crs(epsg=4326)
    merged_stations_unique['geometry'] = merged_stations_unique['geometry'].centroid
    merged_stations_unique = merged_stations_unique.to_crs(epsg=4326)
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
        train_coordinates = group_sorted['geometry'].centroid.apply(lambda geom: (geom.y, geom.x)).tolist()
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
        #feature = {
            #"type": "Feature",
            #"geometry": mapping(train_route_line),  # Convert LineString to GeoJSON format
            #"properties": {
                #"line_name": MRT_LINE,
                #"color": line_colors.get(MRT_LINE, 'black')  # Get the color for this line
            #}
        #}
        geojson_data["features"].append(feature)

    # Recursively convert all non-serializable types to serializable types
    serializable_geojson = convert_to_serializable(geojson_data)

    # Return the GeoJSON data as a JSON response
    return jsonify(serializable_geojson)


@app.route('/api/plot_routes', methods=['POST'])
def plot_routes():
    selected_service_no = request.json['service_no']
    
    # Filter the bus routes for the selected service number
    busroutes = final_data[final_data['ServiceNo'].isin([selected_service_no])]

    grouped_bus_routes = busroutes.groupby(['ServiceNo', 'Direction'])

    # Prepare a GeoJSON FeatureCollection
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Generate GeoJSON for bus routes (lines)
    for (service_no, direction), group in grouped_bus_routes:
        group_sorted = group.sort_values('StopSequence')
        bus_coordinates = list(zip(group_sorted['Latitude'], group_sorted['Longitude']))
        bus_route_line = LineString(bus_coordinates)

        # Add a new feature for the bus route
        feature = {
            "type": "Feature",
            "geometry": mapping(bus_route_line),  # Convert LineString to GeoJSON format
            "properties": {
                "service_no": service_no,
                "direction": direction
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



if __name__ == '__main__':
    app.run(debug=True)




