import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import LineString, Point
from bus_route_plot import original_route, new_route, original_and_new_route
from mrt_map import get_mrt_map

singapore = get_mrt_map()
proposed_bus_routes = pd.read_csv("Bus_RoutesStopsServices/proposed_bus_route.csv")
West_Rush_Hour_Express = ['17171', '17041', '17159', '12091', '43181', '43419', 
                    '28461', '28491', '28511', '28401','21431', '22009']
East_Rush_Hour_Express = ['64009', '63249', '63059', '64419', '64119', '66339', 
                    '54489', '54248', '53389', '52059', '52361', '60081', 
                    '60179', '80071', '80089', '80069', '80009']
tanjong_rhu_riverfront_route = ['90061', '90051', '1039', '7518', '7419', '7319','7111', 
                                '7031', '40011', '9037', '9219','9179', '9022','9037','5039','3031']

def get_proposed_bus_route(route):
    route_data = proposed_bus_routes[proposed_bus_routes['ServiceName'] == route].sort_values(by='Stop Sequence')

    points = []
    for idx, row in route_data.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.7,
            popup=f"{row['ServiceName']} Bus Stop Code: {row['BusStopCode']} Stop {row['Stop Sequence']}"
        ).add_to(singapore)

        points.append([row['Latitude'], row['Longitude']])

    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(singapore)

    return singapore
