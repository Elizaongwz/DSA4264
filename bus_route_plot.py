import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import LineString, Point
import pandas as pd
import folium
from mrt_map import get_mrt_map

def bus_route(busno):
    singapore = get_mrt_map()
    final_data = pd.read_csv("Bus_RoutesStopsServices/trunkroutes.csv")
    #busroutes = final_data
    #to see indiv bus routes
    busroutes = final_data[final_data['ServiceNo'].isin(['busno'])]
    grouped_bus_routes = busroutes.groupby(['ServiceNo', 'Direction'])
    for (service_no, direction), group in grouped_bus_routes:       
        group_sorted = group.sort_values('StopSequence') #ensure busstop for each bus is in correct sequence
        coordinates = list(zip(group_sorted['Latitude'], group_sorted['Longitude'])) #get the coordinates
        bus_route_line = LineString(coordinates) #plot the line 
        
        #plot bus routes in the map
        folium.PolyLine(
            locations=coordinates,  
            weight=2,          
            color='blue',     
            opacity=0.7,      
            popup=f"Service {service_no}"  # label with bus service number
        ).add_to(singapore)

    #add the bus stop points in the map too
    for index, row in busroutes.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=3,
            color='red',
            fill=True,
            fill_color='red',
            popup=f"Bus Stop: {row['BusStopCode']} (Service {row['ServiceNo']})"
        ).add_to(singapore)

    # grp data by service number and direction
    final_data = pd.read_csv("Bus_RoutesStopsServices/trunkroutes.csv")
    #busroutes = final_data

    #to see indiv bus routes
    busroutes = final_data[final_data['ServiceNo'].isin(['busno'])]

    grouped_bus_routes = busroutes.groupby(['ServiceNo', 'Direction'])

    for (service_no, direction), group in grouped_bus_routes:
        
        group_sorted = group.sort_values('StopSequence') #ensure busstop for each bus is in correct sequence
        coordinates = list(zip(group_sorted['Latitude'], group_sorted['Longitude'])) #get the coordinates
        bus_route_line = LineString(coordinates) #plot the line 
        
        #plot bus routes in the map
        folium.PolyLine(
            locations=coordinates,  
            weight=2,          
            color='blue',     
            opacity=0.7,      
            popup=f"Service {service_no}"  # label with bus service number
        ).add_to(singapore)

    #add the bus stop points in the map too
    for index, row in busroutes.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=3,
            color='red',
            fill=True,
            fill_color='red',
            popup=f"Bus Stop: {row['BusStopCode']} (Service {row['ServiceNo']})"
        ).add_to(singapore)

    return singapore