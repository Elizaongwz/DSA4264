import folium
import pandas as pd
from folium import PolyLine
from mrt_map import get_mrt_map

def original_route(*service_numbers):

    singapore = get_mrt_map()
    all_bus_data = pd.read_csv("Bus_RoutesStopsServices/all_bus_data.csv")

    #if specific service numbers are provided, filter for them
    if service_numbers:
        routes = all_bus_data[all_bus_data['ServiceNo'].isin(service_numbers)]
    #else use all routes
    else:
        routes = all_bus_data

    #for each serviceno
    for serviceno, route in routes.groupby('ServiceNo'):

        #plot bus stops
        for _, stop in route.iterrows():
            marker_size = 3 if stop['MRTBusStop'] == 0 else 9
            marker_color = 'blue' if stop['MRTBusStop'] == 0 else 'lightblue'

            folium.CircleMarker(
                location = [stop['Latitude'], stop['Longitude']],
                radius = marker_size,
                color = marker_color,
                fill = True,
                fill_color = marker_color,
                fill_opacity = 0.7
            ).add_to(singapore)
        
        #plot bus route
        bus_stop_locations = route[['Latitude', 'Longitude']].values.tolist()
        PolyLine(
            locations = bus_stop_locations,
            color = "black",
            weight = 3,
            opacity = 0.7
        ).add_to(singapore)

    return singapore

def new_route(*service_numbers):

    singapore = get_mrt_map()
    new_data = pd.read_csv("new_top_10_bus_data.csv", dtype={'ServiceNo': str})

    #if specific service numbers are provided, filter for them
    if service_numbers:
        routes = new_data[new_data['ServiceNo'].isin(service_numbers)]
    #else use all routes
    else:
        routes = new_data

    #for each serviceno
    for serviceno, route in routes.groupby('ServiceNo'):

        #plot bus stops - keep, remove, MRT bus stops
        for _, stop in route.iterrows():

            if stop['outcome'] == 'remove':
                marker_size = 3
                marker_color = 'red' 
            else:
                marker_size = 3 if stop['MRTBusStop'] == 0 else 9 
                marker_color = 'blue' if stop['MRTBusStop'] == 0 else 'lightblue'  

            folium.CircleMarker(
                location = [stop['Latitude'], stop['Longitude']],
                radius = marker_size,
                color = marker_color,
                fill = True,
                fill_color = marker_color,
                fill_opacity = 0.7
            ).add_to(singapore)

        #plot NEW bus route (outcome = keep)
        keep_stop_locations = route[route['outcome'] == 'keep'][['Latitude', 'Longitude']].values.tolist()
        if keep_stop_locations:
            PolyLine(
                locations = keep_stop_locations,
                color = "green", 
                weight = 5,
                opacity = 0.7
            ).add_to(singapore)

    return singapore

def original_and_new_route(*service_numbers):

    singapore = get_mrt_map()
    new_data = pd.read_csv("new_top_10_bus_data.csv", dtype={'ServiceNo': str})
    
    if service_numbers:
        routes = new_data[new_data['ServiceNo'].isin(service_numbers)]
    else:
        routes = new_data
    
    # for each serviceno
    for serviceno, route in routes.groupby('ServiceNo'):

        #plot bus stops
        for _, stop in route.iterrows():

            if stop['outcome'] != 'keep':
                marker_color = 'red' 
            else:
                marker_color = 'blue' if stop['MRTBusStop'] == 0 else 'lightblue' 

            marker_size = 3 if stop['MRTBusStop'] == 0 else 9
    
            folium.CircleMarker(
                location = [stop['Latitude'], stop['Longitude']],
                radius = marker_size,
                color = marker_color,
                fill = True,
                fill_color = marker_color,
                fill_opacity = 0.7
            ).add_to(singapore)
        
        #plot original route
        all_stop_locations = route[['Latitude', 'Longitude']].values.tolist()
        PolyLine(
            locations = all_stop_locations,
            color = "black",
            weight = 3,
            opacity = 0.7
        ).add_to(singapore)
        
        #plot new route
        new_stop_locations = route[route['outcome'] == 'keep'][['Latitude', 'Longitude']].values.tolist()
        PolyLine(
            locations = new_stop_locations,
            color = "green",  
            weight = 3,
            opacity = 0.7
        ).add_to(singapore)
    
    return singapore

