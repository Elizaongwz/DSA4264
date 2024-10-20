import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, Polyline, CircleMarker } from 'react-leaflet';

const BusRouteSelector = ({ onRoutesSelect }) => {
  const [busRoutes, setBusRoutes] = useState([]);
  const [selectedRoutes, setSelectedRoutes] = useState([]);
  const [mapData, setMapData] = useState({});

  useEffect(() => {
    // Fetch bus routes from Spring Boot
    axios.get('http://localhost:8080/api/routes')
      .then(response => {
        console.log(response.data);
        setBusRoutes(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching bus routes!", error);
      });
  }, []);

  useEffect(() => {
    // Fetch map data (train lines) from Spring Boot
    axios.get('http://localhost:8080/api/map/data')
      .then(response => {
        console.log(response.data);
        setMapData(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching map data!", error);
      });
  }, []);

  const handleRouteChange = (event) => {
    const { options } = event.target;
    const selected = [];
    for (let i = 0, len = options.length; i < len; i++) {
      if (options[i].selected) {
        selected.push(options[i].value);
      }
    }
    setSelectedRoutes(selected);
    onRoutesSelect(selected);  // Pass the selected routes to the parent component
  };

  return (
    <div>
      <label>Select Bus Routes:</label>
      <select multiple value={selectedRoutes} onChange={handleRouteChange}>
        {busRoutes.map(route => (
          <option key={route} value={route}>
            {route}
          </option>
        ))}
      </select>
      <MapContainer center={[1.359394, 103.814301]} zoom={12} style={{ height: '600px', width: '900px' }}>
        {mapData.trainLines && mapData.trainLines.map((line, index) => (
          <Polyline key={index} positions={line.geometry} color="grey" weight={2.5} />
        ))}
        {selectedRoutes.map(route => (
          <Polyline key={route} positions={mapData.busRoutes[route]} color="black" weight={2} />
        ))}
        {mapData.busStops && mapData.busStops.map((stop, index) => (
          <CircleMarker key={index} center={stop.geometry} radius={3} color="red" fill={true} fillOpacity={1} />
        ))}
      </MapContainer>
    </div>
  );
};

export default BusRouteSelector;