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
      axios.get('http://127.0.0.1:5000/api/train_lines')  // Call the Flask API for train lines
        .then(response => {
          setTrainLineData(response.data);  // Store the Train Line GeoJSON data
        })
        .catch(error => {
          console.error("Error fetching train line data:", error);
        });
    }
  }, [selectedRoute]);

  const handleRouteChange = (event) => {
    setSelectedRoute(event.target.value);
    setBusRouteData(null);  // Clear the current map data when selecting a new route
    setTrainLineData(null);  // Clear train lines as well
  };

  const trainLineStyle = (feature) => ({
    color: feature.properties.color,  // Use the color property from GeoJSON
    weight: 3,
    opacity: 0.8
  });

  const busRouteStyle = {
    color: "blue",  // Set the bus route color to blue
    weight: 3,
    opacity: 0.8
  };

  const pointToLayer = (feature, latlng) => {
    if (feature.geometry.type === 'Point') {
      return L.circleMarker(latlng, {
        radius: 5,
        fillColor: "red",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
      });
    }
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

      {/* Re-render map when selected route changes (mapKey forces re-render) */}
      <MapContainer key={mapKey} center={[1.359394, 103.814301]} zoom={12} style={{ height: '600px', width: '900px' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {/* Render train lines GeoJSON data if available */}
        {trainLineData && (
          <GeoJSON 
            data={trainLineData}
            style={trainLineStyle}  // Apply line style for train lines
          />
        )}

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
