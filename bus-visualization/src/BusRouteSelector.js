import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const BusRouteSelector = ({ onRouteSelect }) => {
  const [busRoutes, setBusRoutes] = useState([]);
  const [selectedRoute, setSelectedRoute] = useState('');
  const [geoJsonData, setGeoJsonData] = useState(null);  // Store GeoJSON data

  useEffect(() => {
    // Fetch available bus routes from Spring Boot
    axios.get('http://localhost:8080/api/bus_routes')
      .then(response => {
        console.log("Available Routes: ", response.data);
        setBusRoutes(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching bus routes!", error);
      });
  }, []);

  useEffect(() => {
    if (selectedRoute) {
      // Log the selected route for debugging
      console.log("Selected Route: ", selectedRoute);
        
      // Prepare the request body
      const requestBody = { service_no: selectedRoute };
  
      // Log the request body for debugging
      console.log("Request Body:", requestBody);
  
      // Make the POST request to the Spring Boot backend
      axios.post('http://localhost:8080/api/plot_routes', requestBody, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        // Handle successful response and update GeoJSON data
        console.log("GeoJSON Data Response: ", response.data);
        setGeoJsonData(response.data);  // Store the GeoJSON data
      })
      .catch(error => {
        // Handle error and log detailed error information
        console.error("There was an error fetching map data!", error);
        if (error.response) {
          console.error("Error Response Data:", JSON.stringify(error.response.data, null, 2));
          console.error("Status Code:", error.response.status);
        } else if (error.request) {
          console.error("Request made but no response received:", error.request);
        } else {
          console.error("Something went wrong in setting up the request:", error.message);
        }
      });
    }
  }, [selectedRoute]);  // useEffect will run when selectedRoute changes
  
  const handleRouteChange = (event) => {
    const selected = event.target.value;
    setSelectedRoute(selected);
    onRouteSelect(selected);  // Pass the selected route to the parent component
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

      <MapContainer center={[1.359394, 103.814301]} zoom={12} style={{ height: '600px', width: '900px' }}>
        {/* Render GeoJSON data if available */}
        {geoJsonData && (
          <GeoJSON data={geoJsonData} />
        )}
      </MapContainer>
    </div>
  );
};

export default BusRouteSelector;
