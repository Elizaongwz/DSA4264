import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';  // Import Leaflet for mapping features

// Component for selecting and visualizing bus routes on a map
const BusRouteSelector = () => {
  // State variables to store bus routes, proposed and modified routes, and their respective GeoJSON data
  const [busRoutes, setBusRoutes] = useState([]);
  const [proposedRoutes, setProposedRoutes] = useState([]);
  const [proposedRoutesData, setProposedRoutesData] = useState([]);
  const [modifiedRoutes, setModifiedRoutes] = useState([]);
  const [modifiedRoutesData, setModifiedRoutesData] = useState([]);
  
  // State variables to store selected routes and train lines data
  const [selectedModifiedRoute, setSelectedModifiedRoute] = useState('');
  const [selectedRoute, setSelectedRoute] = useState('');
  const [selectedProposedRoute, setSelectedProposedRoute] = useState('');
  const [busRouteData, setBusRouteData] = useState(null);  // Store the GeoJSON data for the selected bus route
  const [trainLineData, setTrainLineData] = useState(null);  // Store GeoJSON data for train lines
  const [parallelScore, setParallelScore] = useState(null);  // Store the parallel score for selected bus route
  const [rank, setRank] = useState(null);  // Store the rank of the bus route
  const [mapKey, setMapKey] = useState(0);  // Force map re-render when this key changes
  const [darkenTrainLines, setDarkenTrainLines] = useState(false);  // State for toggling train line visibility

  // useEffect hook to fetch available bus routes from the backend (Spring Boot connected to Flask API)
  useEffect(() => {
    axios.get('http://localhost:8080/api/bus_routes')
      .then(response => {
        setBusRoutes(response.data);  // Set bus routes to state
      })
      .catch(error => {
        console.error("Error fetching bus routes:", error);  // Log error if any
      });
  }, []);  // Empty dependency array means this effect runs only once when the component mounts

  // Fetch proposed bus routes from the backend
  useEffect(() => {
    axios.get('http://localhost:8080/api/proposed_routes')
      .then(response => {
        setProposedRoutes(response.data);  // Set proposed routes to state
      })
      .catch(error => {
        console.error("Error fetching bus routes:", error);
      });
  }, []);

  // Fetch modified bus routes from the backend
  useEffect(() => {
    axios.get('http://localhost:8080/api/modified_routes')
      .then(response => {
        setModifiedRoutes(response.data);  // Set modified routes to state
      })
      .catch(error => {
        console.error("Error fetching bus routes:", error);
      });
  }, []);

  // Fetch selected bus route data from Spring Boot (calls Python API)
  useEffect(() => {
    if (selectedRoute) {
      const requestBody = { service_no: selectedRoute };  // Prepare the request body

      // Fetch the selected bus route GeoJSON data
      axios.post('http://localhost:8080/api/plot_routes', requestBody, {
        headers: { 'Content-Type': 'application/json' }
      })
      .then(response => {
        setBusRouteData(response.data);  // Store the GeoJSON data for the bus route
        setMapKey(prevKey => prevKey + 1);  // Force map re-render by changing the key
      })
      .catch(error => {
        console.error("Error fetching bus route data:", error);
      });
      
      // Fetch the rank of the selected route
      axios.post('http://localhost:8080/api/rank', requestBody, {
        headers: { 'Content-Type': 'application/json' }
      })
      .then(response => {
        setRank(response.data);  // Store the rank of the selected bus route
      })
      .catch(error => {
        console.error("Error fetching rank:", error);
      });

      // Fetch the parallel score for the selected bus route
      axios.post('http://localhost:8080/api/parallel_score', requestBody, {
        headers: { 'Content-Type': 'application/json' }
      })
      .then(response => {
        setParallelScore(response.data);  // Store the parallel score for the selected bus route
      })
      .catch(error => {
        console.error("Error fetching parallel score:", error);
      });
    }
  }, [selectedRoute]);  // Effect re-runs when selectedRoute changes

  // Fetch proposed bus route data when selected
  useEffect(() => {
    if (selectedProposedRoute) {
      const requestBody = { service_name: selectedProposedRoute };  // Prepare the request body

      // Fetch proposed bus route data (GeoJSON)
      axios.post('http://localhost:8080/api/plot_proposed_routes', requestBody, {
        headers: { 'Content-Type': 'application/json' }
      })
      .then(response => {
        setProposedRoutesData(response.data);  // Store the GeoJSON data for the proposed route
        setMapKey(prevKey => prevKey + 1);  // Force map re-render by changing the key
      })
      .catch(error => {
        console.error("Error fetching bus route data:", error);
      });
    }
  }, [selectedProposedRoute]);

  // Fetch modified bus route data when selected
  useEffect(() => {
    if (selectedModifiedRoute) {
      const requestBody = { service_no: selectedModifiedRoute };  // Prepare the request body

      // Fetch modified bus route data (GeoJSON)
      axios.post('http://localhost:8080/api/plot_modified_routes', requestBody, {
        headers: { 'Content-Type': 'application/json' }
      })
      .then(response => {
        setModifiedRoutesData(response.data);  // Store the GeoJSON data for the modified route
        setMapKey(prevKey => prevKey + 1);  // Force map re-render by changing the key
      })
      .catch(error => {
        console.error("Error fetching bus route data:", error);
      });
    }
  }, [selectedModifiedRoute]);

  // Fetch train lines if the checkbox is checked (darkenTrainLines is true)
  useEffect(() => {
    if (darkenTrainLines) {
      axios.get('http://localhost:8080/api/train_lines')  // Fetch train lines from the backend
        .then(response => {
          setTrainLineData(response.data);  // Store train lines GeoJSON data
        })
        .catch(error => {
          console.error("Error fetching train line data:", error);
        });
    } else {
      setTrainLineData(null);  // Reset train lines if the checkbox is unchecked
    }
  }, [darkenTrainLines]);  // Effect re-runs when darkenTrainLines changes

  // Event handler for bus route selection
  const handleRouteChange = (event) => {
    setSelectedRoute(event.target.value);  // Set the selected bus route
    setBusRouteData(null);  // Clear the current bus route data
    setParallelScore(null);  // Clear the current parallel score
    setRank(null);  // Clear the current rank
  };

  // Event handler for toggling train line visibility
  const handleTrainChange = (event) => {
    setDarkenTrainLines(event.target.checked);  // Update darkenTrainLines state based on checkbox value
    setTrainLineData(null);  // Clear the current train line data
  }

  // Event handler for proposed bus route selection
  const handleProposedRouteChange = (event) => {
    setSelectedProposedRoute(event.target.value);  // Set the selected proposed bus route
    setProposedRoutesData(null);  // Clear the current proposed route data
  };

  // Event handler for modified bus route selection
  const handleModifiedRouteChange = (event) => {
    setSelectedModifiedRoute(event.target.value);  // Set the selected modified bus route
    setModifiedRoutesData(null);  // Clear the current modified route data
  };

  // Style for train lines on the map
  const trainLineStyle = (feature) => {
    return {
      color: feature.properties.color || "black",  // Set the train line color based on GeoJSON property or default to black
      weight: 2,
      opacity: 0.6  // Set opacity to make train lines slightly transparent
    };
  };

  // Style for bus routes on the map
  const busRouteStyle = {
    color: "#800000",  // Maroon color for bus routes
    weight: 3,  // Line thickness
    opacity: 1  // Fully opaque lines
  };

  // Style for proposed bus routes
  const proposedRouteStyle = {
    color: "#000000",  // Black color for proposed bus routes
    weight: 3,
    opacity: 1
  };

  // Style for modified bus routes
  const modifiedRouteStyle = {
    color: "magenta",  // Magenta color for modified bus routes
    weight: 3,
    opacity: 1
  };

  // Point style for bus stops
  const pointToLayer = (feature, latlng) => {
    if (feature.geometry.type === 'Point') {
      return L.circleMarker(latlng, {
        radius: 2,
        fillColor: "red",
        color: "#000",
        weight: 3,
        opacity: 1,
        fillOpacity: 0.8
      });
    }
  };

  const proposedPointToLayer = (feature, latlng) => {
    if (feature.geometry.type === 'Point') {
      return L.circleMarker(latlng, {
        radius: 2,
        fillColor: "green",
        color: "#000",
        weight: 3,
        opacity: 1,
        fillOpacity: 0.8
      });
    }
  };

  const modifiedPointToLayer = (feature, latlng) => {
    if (feature.geometry.type === 'Point') {
      return L.circleMarker(latlng, {
        radius: 2,
        fillColor: "black",
        color: "#000",
        weight: 3,
        opacity: 1,
        fillOpacity: 0.8
      });
    }
  };

  return (
    <div>
      {/* Dropdown menu for selecting a bus route */}
      <label>Select Bus Route:</label>
      <select 
        value={selectedRoute} 
        onChange={handleRouteChange} 
        style={{ marginBottom: '20px', marginLeft: '5px', display: 'block' }}
      >
        <option value="" disabled>Select a route</option>
        {/* Populate dropdown with bus route options */}
        {busRoutes.map(route => (
          <option key={route} value={route}>
            {route}
          </option>
        ))}
      </select>

      {/* Dropdown menu for selecting a modified bus route */}
      <label>Select Modified Bus Route:</label>
      <select 
        value={selectedModifiedRoute} 
        onChange={handleModifiedRouteChange} 
        style={{ marginBottom: '40px', marginLeft: '5px', display: 'block' }}
      >
        <option value="" disabled>Select a route</option>
        {/* Populate dropdown with modified bus route options */}
        {modifiedRoutes.map(route => (
          <option key={route} value={route}>
            {route}
          </option>
        ))}
      </select>

      {/* Dropdown menu for selecting a proposed bus route */}
      <label>Select Proposed Bus Route:</label>
      <select 
        value={selectedProposedRoute} 
        onChange={handleProposedRouteChange} 
        style={{ marginBottom: '20px', marginLeft: '5px', display: 'block' }}
      >
        <option value="" disabled>Select a route</option>
        {/* Populate dropdown with proposed bus route options */}
        {proposedRoutes.map(route => (
          <option key={route} value={route}>
            {route}
          </option>
        ))}
      </select>

      {/* Checkbox for toggling train line visibility */}
      <label>
        <input 
          type="checkbox" 
          checked={darkenTrainLines} 
          onChange={handleTrainChange} 
        />
        Darken Train Lines
      </label>

      {/* Display the parallel score for the selected bus route */}
      {parallelScore !== null && (
        <div>
          <h3>Parallel Score for Bus {selectedRoute}: {parallelScore}</h3>
        </div>
      )}

      {/* Display the rank of the selected bus route */}
      {rank !== null && (
        <div>
          <h3>Rank for Bus {selectedRoute}: {rank}</h3>
        </div>
      )}

      {/* Map container that renders the leaflet map. The mapKey forces re-render when necessary */}
      <MapContainer 
        key={mapKey} 
        center={[1.359394, 103.814301]}  // Singapore's geographical center
        zoom={12}  // Set initial zoom level
        style={{ height: '600px', width: '1000px' }}  // Set map size
      >
        <TileLayer
          url="https://www.onemap.gov.sg/maps/tiles/Default/{z}/{x}/{y}.png"  // URL for the tile layer
          attribution='<img src="https://www.onemap.gov.sg/web-assets/images/logo/om_logo.png" style="height:20px;width:20px;"/>&nbsp;<a href="https://www.onemap.gov.sg/" target="_blank" rel="noopener noreferrer">OneMap</a>&nbsp;&copy;&nbsp;contributors&nbsp;&#124;&nbsp;<a href="https://www.sla.gov.sg/" target="_blank" rel="noopener noreferrer">Singapore Land Authority</a>'
          maxZoom={19}
          minZoom={11}
          detectRetina={true}
        />

        {/* Render train line GeoJSON data */}
        {trainLineData && (
          <GeoJSON 
            data={trainLineData} 
            style={trainLineStyle}  // Apply train line styling
          />
        )}

        {/* Render selected bus route GeoJSON data */}
        {busRouteData && (
          <GeoJSON 
            data={busRouteData} 
            style={busRouteStyle} // Apply styling for bus routes
            pointToLayer={pointToLayer}  // Apply marker style for bus  
          />
        )}

        {/* Render selected proposed bus route GeoJSON data */}
        {proposedRoutesData && (
          <GeoJSON 
            data={proposedRoutesData} 
            style={proposedRouteStyle}  // Apply styling for proposed bus routes
            pointToLayer={proposedPointToLayer}  // Apply marker style 
          />
        )}

        {/* Render selected modified bus route GeoJSON data */}
        {modifiedRoutesData && (
          <GeoJSON 
            data={modifiedRoutesData} 
            style={modifiedRouteStyle}  // Apply styling for modified bus routes
            pointToLayer={modifiedPointToLayer}  // Apply marker style 
          />
        )}
      </MapContainer>
    </div>
  );
};

export default BusRouteSelector;
