import folium
import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString, LineString
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
trunk = trunk[trunk['Direction'] == 1]

#bus routes data: filter for direction = 1 and trunk buses
bus_routes = bus_routes[bus_routes['Direction'] == 1]
merged_data = pd.merge(bus_routes, trunk[['ServiceNo']], on='ServiceNo', how='inner')
merged_data

# join to get the bus stop coordinates
final_data = pd.merge(merged_data, bus_stops, on='BusStopCode', how='left')

train_stations = gpd.read_file("TrainStation_Jul2024/repaired_shapefile.shp")

mrt_lines = {
    'Thomson-East Coast Line': ['WOODLANDS NORTH MRT STATION','WOODLANDS MRT STATION','WOODLANDS SOUTH MRT STATION', 'SPRINGLEAF MRT STATION','LENTOR MRT STATION','MAYFLOWER MRT STATION','BRIGHT HILL MRT STATION',
                                'UPPER THOMSON MRT STATION','CALDECOTT MRT STATION','STEVENS MRT STATION','NAPIER MRT STATION','ORCHARD BOULEVARD MRT STATION','ORCHARD MRT STATION','GREAT WORLD MRT STATION',
                                'HAVELOCK MRT STATION','OUTRAM PARK MRT STATION','MAXWELL MRT STATION','SHENTON WAY MRT STATION','MARINA BAY MRT STATION','GARDENS BY THE BAY MRT STATION','TANJONG RHU MRT STATION',
                                'KATONG PARK MRT STATION','TANJONG KATONG MRT STATION','MARINE PARADE MRT STATION','MARINE TERRACE MRT STATION','SIGLAP MRT STATION','BAYSHORE MRT STATION'],
    'North-South Line': ['JURONG EAST MRT STATION','BUKIT BATOK MRT STATION','BUKIT GOMBAK MRT STATION','CHOA CHU KANG MRT STATION','YEW TEE MRT STATION','KRANJI MRT STATION','MARSILING MRT STATION','WOODLANDS MRT STATION',
                         'ADMIRALTY MRT STATION','SEMBAWANG MRT STATION','CANBERRRA MRT STATION','YISHUN MRT STATION','KHATIB MRT STATION','YIO CHU KANG MRT STATION','ANG MO KIO MRT STATION','BISHAN MRT STATION',
                         'BRADDELL MRT STATION','TOA PAYOH MRT STATION','NOVENA MRT STATION','NEWTON MRT STATION','ORCHARD MRT STATION','SOMERSET MRT STATION','DHOBY GHAUT MRT STATION','CITY HALL MRT STATION',
                         'RAFFLES PLACE MRT STATION','MARINA BAY MRT STATION','MARINA SOUTH PIER MRT STATION'],
    'Circle Line': ['DHOBY GHAUT MRT STATION', 'BRAS BASAH MRT STATION', 'ESPLANADE MRT STATION', 'PROMENADE MRT STATION','NICOLL HIGHWAY MRT STATION','STADIUM MRT STATION',
                    'MOUNTBATTEN MRT STATION','DAKOTA MRT STATION','PAYA LEBAR MRT STATION','MACPHERSON MRT STATION','TAI SENG MRT STATION','BARTLEY MRT STATION','SERANGOON MRT STATION','LORONG CHUAN MRT STATION',
                    'BISHAN MRT STATION','MARYMOUNT MRT STATION','CALDECOTT MRT STATION','BOTANIC GARDENS MRT STATION','FARRER ROAD MRT STATION','HOLLAND VILLAGE MRT STATION','BUONA VISTA MRT STATION','ONE-NORTH MRT STATION',
                    'KENT RIDGE MRT STATION', 'HAW PAW VILLA MRT STATION', 'PASIR PANJANG MRT STATION', 'LABRADOR PARK MRT STATION', 'TELOK BLANGAH MRT STATION','HABOURFRONT MRT STATION'],
    'Circle Line.': ['PROMENADE MRT STATION','BAYFRONT MRT STATION', 'MARINA BAY MRT STATION'],
    'North-East Line': ['HARBOURFRONT MRT STATION','OUTRAM PARK MRT STATION','CHINATOWN MRT STATION','CLARKE QUAY MRT STATION','DHOBY GHAUT MRT STATION','LITTLE INDIA MRT STATION','FARRER PARK MRT STATION','BOON KENG MRT STATION',
                        'POTONG PASIR MRT STATION','WOODLEIGH MRT STATION','SERANGOON MRT STATION','KOVAN MRT STATION','HOUGANG MRT STATION','BUANGKOK MRT STATION','SENGKANG MRT STATION','PUNGGOL MRT STATION'],
    'Downtown Line': ['BUKIT PANJANG MRT STATION', 'CASHEW MRT STATION', 'HILLVIEW MRT STATION', 'HUME MRT STATION', 'BEAUTY WORLD MRT STATION', 'KING ALBERT PARK MRT STATION', 'SIXTH AVENUE','TAN KAH KEE MRT STATION',
                      'BOTANIC GARDENS MRT STATION', 'STEVENS MRT STATION', 'NEWTON MRT STATION', 'LITTLE INDIA MRT STATION', 'ROCHOR MRT STATION', 'BUGIS MRT STATION', 'PROMENADE MRT STATION', 'BAYFRONT MRT STATION',
                      'DOWNTOWN MRT STATION', 'TELOK AYER MRT STATION', 'CHINATOWN MRT STATION', 'FORT CANNING MRT STATION', ' BENCOOLEN MRT STATION', 'JALAN BESAR MRT STATION', 'BENDEMEER MRT STATION', 'GEYLANG  BAHRU MRT STATION',
                      'MATTAR MRT STATION', 'MACPHERSON MRT STATION', 'UBI MRT STATION', 'KAKI BUKIT MRT STATION', ' BEDOK NORTH MRT STATION', 'BEDOK RESERVOIR MRT STATION', 'TAMPINES WEST MRT STATION',
                      'TAMPINES MRT STATION', 'TAMPINES EAST MRT STATION', 'UPPER CHANGI MRT STATION', 'EXPO MRT STATION'],
    'East-West Line': ['PASIR RIS MRT STATION', 'TAMPINES MRT STATION', 'SIMEI MRT STATION', 'TANAH MERAH MRT STATION','BEDOK MRT STATION', 'KEMBANGAN MRT STATION', 'EUNOS MRT STATION', 'PAYA LEBAR MRT STATION',
                       'ALJUNIED MRT STATION', 'KALLANG MRT STATION', ' LAVENDER MRT STATION','BUGIS MRT STATION', 'CITY HALL MRT STATION', 'RAFFLES PLACE MRT STATION','TANJONG PAGAR MRT STATION', 'OUTRAM PARK MRT STATION',
                       'TIONG BAHRU MRT STATION', 'REDHILL MRT STATION', 'QUEENSTOWN MRT STATION', 'COMMONWEALTH MRT STATION','BUONA VISTA MRT STATION', 'DOVER MRT STATION', 'CLEMENTI MRT STATION', 'JURONG EAST MRT STATION',
                       'CHINESE GARDEN MRT STATION', 'LAKESIDE MRT STATION', 'BOON LAY MRT STATION', 'PIONEER MRT STATION','JOO KON MRT STATION',' GUL CIRCLE MRT STATION', 'TUAS CRESCENT MRT STATION', 
                       'TUAS WEST ROAD MRT STATION', 'TUAS LINK MRT STATION'],
    'East-West Line.':['TANAH MERAH MRT STATION','EXPO MRT STATION', 'CHANGI AIRPORT MRT STATION']
}
line_colors = {
    'North-South Line': 'red',
    'East-West Line': 'green',
    'East-West Line.': 'green',
    'Circle Line': 'darkorange',
    'Circle Line.': 'darkorange',
    #'Circle Line.': 'black', # can use this because orange hard to see
    #'Circle Line': 'black',
    'North-East Line': 'purple',
    'Downtown Line': 'blue',
    'Thomson-East Coast Line': 'brown'
}

mrt_line_data = []
for line, stations in mrt_lines.items():
    for index, station in enumerate(stations):
        mrt_line_data.append((station, line, index+1))
mrt_line_df = pd.DataFrame(mrt_line_data, columns=['STN_NAM_DE', 'MRT_LINE', 'STN_SEQUENCE'])

# Merge this DataFrame with your original train_stations DataFrame on the STN_NAM_DE column
train_stations_merged = train_stations.merge(mrt_line_df, on='STN_NAM_DE', how='left')
merged_stations_unique = train_stations_merged.drop_duplicates(subset=['STN_NAM_DE', 'MRT_LINE'])
merged_stations_unique = merged_stations_unique.to_crs(epsg=4326)
grouped_train_lines = merged_stations_unique.groupby(['MRT_LINE']).apply(lambda x: x[['STN_NAM_DE', 'STN_SEQUENCE','geometry']])
grouped_train_lines = grouped_train_lines.sort_values(['MRT_LINE','STN_SEQUENCE'])
grouped_train_lines = grouped_train_lines.to_crs(epsg=4326)

def haversine(coord1, coord2): ## ccomputes distance between two points on the surface of a sphere using the latitude and longitude  >> supposed to be better than eucidian 
    R = 6371.0  # Radius of Earth in kilometers
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def calculate_bearing(coord1, coord2):
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)
    delta_lon = lon2 - lon1
    x = np.sin(delta_lon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - (np.sin(lat1) * np.cos(lat2) * np.cos(delta_lon))
    bearing = np.degrees(np.arctan2(x, y))
    return (bearing + 360) % 360

def calculate_route_parallelism(bus_route_line, mrt_multiline):
    total_score = 0
    segment_scores = []
    total_length = 0  # Total length of the bus route in meters

    # Loop through each segment in the bus route
    for i in range(len(bus_route_line.coords) - 1):
        # Define the start and end points of the bus segment
        bus_segment = LineString([bus_route_line.coords[i], bus_route_line.coords[i + 1]])
        bus_bearing = calculate_bearing(bus_route_line.coords[i], bus_route_line.coords[i + 1])
        
        # Calculate the length of the bus segment (in meters)
        segment_length = haversine(bus_route_line.coords[i], bus_route_line.coords[i + 1]) * 1000
        total_length += segment_length

        # Find the nearest MRT line segment to this bus segment
        min_distance = float('inf')
        nearest_mrt_bearing = None

        # Loop through each MRT line segment in the MRT network
        for mrt_line in mrt_multiline.geoms:
            for j in range(len(mrt_line.coords) - 1):
                mrt_segment = LineString([mrt_line.coords[j], mrt_line.coords[j + 1]])
                mrt_bearing = calculate_bearing(mrt_line.coords[j], mrt_line.coords[j + 1])

                # Find the minimum distance from the bus segment to the MRT segment
                p1, p2 = nearest_points(bus_segment, mrt_segment)
                distance = haversine((p1.y, p1.x), (p2.y, p2.x)) * 1000

                if distance < min_distance:
                    min_distance = distance
                    nearest_mrt_bearing = mrt_bearing

        # Calculate the bearing difference between the bus segment and nearest MRT segment
        bearing_diff = abs(bus_bearing - nearest_mrt_bearing)
        if bearing_diff > 180:
            bearing_diff = 360 - bearing_diff

        # Calculate the parallelism score for this segment, considering both distance and bearing difference
        score = (1 / (1 + min_distance)) * (1 - bearing_diff / 180)  # Score decreases as distance or bearing diff increases

        # Weight the score by the segment length but smooth its influence by scaling
        # Using sqrt(segment_length) to reduce the extreme influence of very long segments without a hard cap
        weighted_score = score * np.sqrt(segment_length)
        segment_scores.append(weighted_score)
        total_score += weighted_score

    # Normalize the total score by the square root of the total route length
    # Smooths out the impact of route length and avoids inflating scores for shorter routes
    normalized_score = total_score / np.sqrt(total_length) if total_length > 0 else 0

    return normalized_score

#def calculate_route_parallelism(bus_route_line, mrt_multiline): ## WITHOUT SMOOTHING FOR WEIGHTAGE
    total_score = 0
    segment_scores = []
    total_length = 0  # Total length of the bus route
    
    # Loop through each segment in the bus route
    for i in range(len(bus_route_line.coords) - 1):
        # Define the start and end points of the bus segment
        bus_segment = LineString([bus_route_line.coords[i], bus_route_line.coords[i + 1]])
        bus_bearing = calculate_bearing(bus_route_line.coords[i], bus_route_line.coords[i + 1])
        
        # Calculate the length of the bus segment (in meters)
        segment_length = haversine(bus_route_line.coords[i], bus_route_line.coords[i + 1]) * 1000
        total_length += segment_length

        # Find the nearest MRT line segment to this bus segment
        min_distance = float('inf')
        nearest_mrt_bearing = None

        # Loop through each MRT line segment in the MRT network
        for mrt_line in mrt_multiline.geoms:
            for j in range(len(mrt_line.coords) - 1):
                mrt_segment = LineString([mrt_line.coords[j], mrt_line.coords[j + 1]])
                mrt_bearing = calculate_bearing(mrt_line.coords[j], mrt_line.coords[j + 1])

                # Find the minimum distance from the bus segment to the MRT segment
                p1, p2 = nearest_points(bus_segment, mrt_segment)
                distance = haversine((p1.y, p1.x), (p2.y, p2.x)) * 1000

                if distance < min_distance:
                    min_distance = distance
                    nearest_mrt_bearing = mrt_bearing

        # Calculate the bearing difference between the bus segment and nearest MRT segment
        bearing_diff = abs(bus_bearing - nearest_mrt_bearing)
        if bearing_diff > 180:
            bearing_diff = 360 - bearing_diff

        # Calculate the parallelism score for this segment
        score = (1 / (1 + min_distance)) * (1 - bearing_diff / 180)  # Score decreases as distance and bearing diff increases
        
        # Weight the score by the segment length
        weighted_score = score * segment_length
        segment_scores.append(weighted_score)
        total_score += weighted_score

    # Normalize the total score by the total length of the bus route
    average_score = total_score / total_length if total_length > 0 else 0
    
    return average_score

#def calculate_route_parallelism(bus_route_line, mrt_multiline): ## WITHOUT CONSIDERING LENGTH OF SEGMENT 
    total_score = 0
    segment_scores = []
    total_segments = len(bus_route_line.coords) - 1  # Number of segments in the bus route

    # Loop through each segment in the bus route
    for i in range(total_segments):
        # Define the start and end points of the bus segment
        bus_segment = LineString([bus_route_line.coords[i], bus_route_line.coords[i + 1]])
        bus_bearing = calculate_bearing(bus_route_line.coords[i], bus_route_line.coords[i + 1])
        
        # Find the nearest MRT line segment to this bus segment
        min_distance = float('inf')
        nearest_mrt_segment = None
        nearest_mrt_bearing = None

        # Loop through each MRT line segment in the MRT network
        for mrt_line in mrt_multiline.geoms:
            for j in range(len(mrt_line.coords) - 1):
                mrt_segment = LineString([mrt_line.coords[j], mrt_line.coords[j + 1]])
                mrt_bearing = calculate_bearing(mrt_line.coords[j], mrt_line.coords[j + 1])

                # Find the minimum distance from the bus segment to the MRT segment
                p1, p2 = nearest_points(bus_segment, mrt_segment)
                distance = haversine((p1.y, p1.x), (p2.y, p2.x)) * 1000

                # If this is the closest MRT segment so far, store it
                if distance < min_distance:
                    min_distance = distance
                    nearest_mrt_segment = mrt_segment
                    nearest_mrt_bearing = mrt_bearing

        # Calculate the bearing difference between the bus segment and nearest MRT segment > assess how parallel
        bearing_diff = abs(bus_bearing - nearest_mrt_bearing)
        if bearing_diff > 180:
            bearing_diff = 360 - bearing_diff

        # Calculate the parallelism score for this segment:
        # Considers both distance and bearing difference.
        # Score decreases as distance or bearing difference increases.
        score = 1 / (1 + min_distance) * (1 - bearing_diff / 180)  # Normalize bearing_diff to 0-1 range

        segment_scores.append(score)
        total_score += score

    # The overall parallelism score is the average of all segment scores
    average_score = total_score / total_segments if total_segments > 0 else 0
    return average_score

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

from flask import jsonify
import numpy as np
from shapely.geometry import mapping
import json

# Helper function to recursively convert non-serializable types (e.g., np.int64) to serializable types
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
        selected_routes = request.json
        scores = {}

        for route in selected_routes:
            bus_geom = final_data[final_data['ServiceNo'] == route]['geometry'].values[0]
            score = calculate_route_parallelism(bus_geom, train_stations['geometry'])
            scores[route] = score

        return jsonify(scores)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)




