import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import LineString

def get_mrt_map():
    train_stations = gpd.read_file("TrainStation_Jul2024/repaired_shapefile.shp")
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
    grouped_train_lines = merged_stations_unique.groupby(['MRT_LINE']).apply(lambda x: x[['STN_NAM_DE', 'STN_SEQUENCE','geometry']])
    grouped_train_lines = grouped_train_lines.sort_values(['MRT_LINE','STN_SEQUENCE'])

    #singapore = folium.Map(location=(1.359394, 103.814301), zoom_start=12)

    grouped_train_lines = grouped_train_lines.to_crs(epsg=4326)

    singapore = folium.Map(location=(1.359394, 103.814301), zoom_start=12)
    folium.GeoJson(grouped_train_lines, name="Singapore Map").add_to(singapore)
    #grouped_train_lines.to_file("TrainStation_Jul2024/mrt_lines_shapefile.shp")
    
    # adding MRT lines to the map
    for MRT_LINE, group in grouped_train_lines.groupby(level='MRT_LINE'):
        group_sorted = group.sort_values('STN_SEQUENCE')
        coordinates = group_sorted['geometry'].centroid.apply(lambda geom: (geom.y, geom.x)).tolist()
        line_color = line_colors.get(MRT_LINE, 'black')

        folium.PolyLine(
            locations=coordinates,  
            weight=5,          
            color=line_color,     
            opacity=0.7,      
            popup=f"{MRT_LINE}"
        ).add_to(singapore)
    
    # uncomment the chunk below if you want to see pop-ups with station name & location
    # for idx, row in merged_stations_unique.iterrows():
    #     station_location = row['geometry'].representative_point()
    #     station_name = row['STN_NAM_DE']
    #     lat = station_location.y 
    #     lon = station_location.x 

    #     # Create a popup with station name and coordinates
    #     popup_html = f"""
    #     <div style="font-size: 12px;">
    #         <strong>{station_name}</strong><br>
    #         Lat: {lat:.6f}, Lon: {lon:.6f}
    #     </div>
    #     """

    #     folium.Marker(
    #         location=[lat, lon],  
    #         popup=folium.Popup(popup_html, max_width=80),  
    #         icon=folium.Icon(color='blue', icon='info-sign')
    #     ).add_to(singapore)
    print(train_coordinates)

    return singapore
