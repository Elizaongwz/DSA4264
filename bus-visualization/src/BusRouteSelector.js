import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';  // Import Leaflet

const BusRouteSelector = () => {
  const [busRoutes, setBusRoutes] = useState([]);
  const [selectedRoute, setSelectedRoute] = useState('');
  const [busRouteData, setBusRouteData] = useState(null);  // Store Bus Route GeoJSON data
  const [trainLineData, setTrainLineData] = useState(null);  // Store Train Line GeoJSON data
  const [parallelScore, setParallelScore] = useState(null);  // Store the parallel score
  const [mapKey, setMapKey] = useState(0);  // Key to force map re-render

  // Fetch available bus routes from Spring Boot (via Python API)
  useEffect(() => {
    axios.get('http://localhost:8080/api/bus_routes')
      .then(response => {
        setBusRoutes(response.data);
      })
      .catch(error => {
        console.error("Error fetching bus routes:", error);
      });
  }, []);

  // Fetch selected bus route from Spring Boot (via Python API)
  useEffect(() => {
    if (selectedRoute) {
      const requestBody = { service_no: selectedRoute };

      // Fetch the bus route from Spring Boot
      axios.post('http://localhost:8080/api/plot_routes', requestBody, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        setBusRouteData(response.data);  // Store the Bus Route GeoJSON data
        setMapKey(prevKey => prevKey + 1);  // Change the key to force re-render
      })
      .catch(error => {
        console.error("Error fetching bus route data:", error);
      });

      // Fetch train line data directly from Flask API
      axios.get('http://localhost:8080/api/train_lines')  // Call the Flask API for train lines
        .then(response => {
          setTrainLineData(response.data);  // Store the Train Line GeoJSON data
        })
        .catch(error => {
          console.error("Error fetching train line data:", error);
        });

      // Fetch the parallel score for the selected route
      axios.post('http://localhost:8080/api/parallel_score', requestBody, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        setParallelScore(response.data);  // Store the parallel score for the selected route
      })
      .catch(error => {
        console.error("Error fetching parallel score:", error);
      });
    }
  }, [selectedRoute]);

  const handleRouteChange = (event) => {
    setSelectedRoute(event.target.value);
    setBusRouteData(null);  // Clear the current map data when selecting a new route
    setTrainLineData(null);  // Clear train lines as well
    setParallelScore(null);  // Clear the previous parallel score
  };

  // Style for train lines
  const trainLineStyle = (feature) => {
    return {
      color: feature.properties.color || "black",  // Use the color property from GeoJSON
      weight: 3,
      opacity: 1
    };
  };

  // Style for bus routes
  const busRouteStyle = {
    color: "blue",  // Set the bus route color to blue
    weight: 1.2,
    opacity: 1
  };

  // Point style for bus stops
  const pointToLayer = (feature, latlng) => {
    if (feature.geometry.type === 'Point') {
      return L.circleMarker(latlng, {
        radius: 2,
        fillColor: "red",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
      });
    }
  };

  const testGeoJSON = {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [103.8198, 1.3521],  // Singapore coordinates
            [103.8190, 1.3528]
          ]
        },
        "properties": {
          "line_name": "Test MRT Line",
          "color": "red"
        }
      }
    ]
  };

  return (
    <div>
      <label>Select Bus Route:</label>
      <select value={selectedRoute} onChange={handleRouteChange}>
        <option value="" disabled>Select a route</option>
        {busRoutes.map(route => (
          <option key={route} value={route}>
            {route}
          </option>
        ))}
      </select>

      {/* Display the parallel score */}
      {parallelScore !== null && (
        <div>
          <h3>Parallel Score for {selectedRoute}: {parallelScore}</h3>
        </div>
      )}

      {/* Re-render map when selected route changes (mapKey forces re-render) */}
      <MapContainer key={mapKey} center={[1.359394, 103.814301]} zoom={12} style={{ height: '600px', width: '1000px' }}>
        <TileLayer
        url="https://www.onemap.gov.sg/maps/tiles/Default/{z}/{x}/{y}.png"
        attribution='<img src="https://www.onemap.gov.sg/web-assets/images/logo/om_logo.png" style="height:20px;width:20px;"/>&nbsp;<a href="https://www.onemap.gov.sg/" target="_blank" rel="noopener noreferrer">OneMap</a>&nbsp;&copy;&nbsp;contributors&nbsp;&#124;&nbsp;<a href="https://www.sla.gov.sg/" target="_blank" rel="noopener noreferrer">Singapore Land Authority</a>'
        maxZoom={19}
        minZoom={11}
        detectRetina={true}
        />
        {/* Render train lines GeoJSON data if available */}
        {trainLineData && (
          <GeoJSON 
            data={trainLineData}
            style={trainLineStyle} />
        )}
        <GeoJSON
          data={testGeoJSON}
          style={trainLineStyle} />
        {/* Render bus route GeoJSON data if available */}
        {busRouteData && (
          <GeoJSON 
            data={busRouteData}
            style={busRouteStyle}  // Apply line style for bus routes
            pointToLayer={pointToLayer}  // Apply marker style for bus stops
          />
        )}
      </MapContainer>
    </div>
  );
};

export default BusRouteSelector;
