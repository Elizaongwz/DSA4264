import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';  // Import Leaflet

const BusRouteSelector = () => {
  const [busRoutes, setBusRoutes] = useState([]);
  const [proposedRoutes, setProposedRoutes] = useState([]);
  const [proposedRoutesData, setProposedRoutesData] = useState([]);
  const [modifiedRoutes, setModifiedRoutes] = useState([]);
  const [modifiedRoutesData, setModifiedRoutesData] = useState([]);
  const [selectedModifiedRoute, setSelectedModifiedRoute] = useState('');
  const [selectedRoute, setSelectedRoute] = useState('');
  const [selectedProposedRoute, setSelectedProposedRoute] = useState('');
  const [busRouteData, setBusRouteData] = useState(null);  // Store Bus Route GeoJSON data
  const [trainLineData, setTrainLineData] = useState(null);  // Store Train Line GeoJSON data
  const [parallelScore, setParallelScore] = useState(null);  // Store the parallel score
  const [rank, setRank] = useState(null);  // Store the rank
  const [mapKey, setMapKey] = useState(0);  // Key to force map re-render
  const [darkenTrainLines, setDarkenTrainLines] = useState(false);

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

  useEffect(() => {
    axios.get('http://localhost:8080/api/proposed_routes')
      .then(response => {
        setProposedRoutes(response.data);
      })
      .catch(error => {
        console.error("Error fetching bus routes:", error);
      });
  }, []);

  useEffect(() => {
    axios.get('http://localhost:8080/api/modified_routes')
      .then(response => {
        setModifiedRoutes(response.data);
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
      
      // Fetch the rank for the selected route
      axios.post('http://localhost:8080/api/rank', requestBody, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        setRank(response.data);  // Store the parallel score for the selected route
      })
      .catch(error => {
        console.error("Error fetching rank:", error);
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

  useEffect(() => {
    if (selectedProposedRoute) {
      const requestBody = { service_name: selectedProposedRoute };

      // Fetch the bus route from Spring Boot
      axios.post('http://localhost:8080/api/plot_proposed_routes', requestBody, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        setProposedRoutesData(response.data);  // Store the Bus Route GeoJSON data
        setMapKey(prevKey => prevKey + 1);  // Change the key to force re-render
      })
      .catch(error => {
        console.error("Error fetching bus route data:", error);
      });
    }
  }, [selectedProposedRoute]);

  useEffect(() => {
    if (selectedModifiedRoute) {
      const requestBody = { service_no: selectedModifiedRoute };

      // Fetch the bus route from Spring Boot
      axios.post('http://localhost:8080/api/plot_modified_routes', requestBody, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        setModifiedRoutesData(response.data);  // Store the Bus Route GeoJSON data
        setMapKey(prevKey => prevKey + 1);  // Change the key to force re-render
      })
      .catch(error => {
        console.error("Error fetching bus route data:", error);
      });
    }
  }, [selectedModifiedRoute]);

  useEffect(() => {
    if (darkenTrainLines) {
      // Fetch train line data when the checkbox is checked
      axios.get('http://localhost:8080/api/train_lines')
        .then(response => {
          setTrainLineData(response.data);
        })
        .catch(error => {
          console.error("Error fetching train line data:", error);
        });
    } else {
      // Reset train line data when checkbox is unchecked
      setTrainLineData(null);
    }
  }, [darkenTrainLines]);

  const handleRouteChange = (event) => {
    setSelectedRoute(event.target.value);
    setBusRouteData(null);
    setParallelScore(null);
    setRank(null);
  };

  const handleTrainChange = (event) => {
    setDarkenTrainLines(event.target.checked);
    setTrainLineData(null);
  }

  const handleProposedRouteChange = (event) => {
    setSelectedProposedRoute(event.target.value);
    setProposedRoutesData(null);
  };

  const handleModifiedRouteChange = (event) => {
    setSelectedModifiedRoute(event.target.value);
    setModifiedRoutesData(null);
  };

  // Style for train lines
  const trainLineStyle = (feature) => {
    return {
      color: feature.properties.color || "black",  // Use the color property from GeoJSON
      weight: 2,
      opacity: 0.6
    };
  };

  // Style for bus routes
  const busRouteStyle = {
    color: "#800000",
    weight: 3,
    opacity: 1
  };
  const proposedRouteStyle = {
    color: "#000000",  
    weight: 3,
    opacity: 1
  };
  const modifiedRouteStyle = {
    color: "magenta", 
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
        weight: 5,
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
        fillColor: "blue",
        color: "#000",
        weight: 3,
        opacity: 1,
        fillOpacity: 0.8
      });
    }
  };


  return (
    <div>
      <label>Select Bus Route:</label>
      <select value={selectedRoute} onChange={handleRouteChange} style={{ marginBottom: '20px', marginLeft: '5px', display: 'block' }}>
        <option value="" disabled>Select a route</option>
        {busRoutes.map(route => (
          <option key={route} value={route}>
            {route}
          </option>
        ))}
      </select>

      <label>Select Modified Bus Route:</label>
      <select value={selectedModifiedRoute} onChange={handleModifiedRouteChange} style={{ marginBottom: '40px', marginLeft: '5px', display: 'block'}}>
        <option value="" disabled>Select a route</option>
        {modifiedRoutes.map(route => (
          <option key={route} value={route}>
            {route}
          </option>
        ))}
      </select>

      <label>Select Proposed Bus Route:</label>
      <select value={selectedProposedRoute} onChange={handleProposedRouteChange} style={{ marginBottom: '20px', marginLeft: '5px', display: 'block'}}>
        <option value="" disabled>Select a route</option>
        {proposedRoutes.map(route => (
          <option key={route} value={route}>
            {route}
          </option>
        ))}
      </select>
      <label>
        <input type="checkbox" checked={darkenTrainLines} onChange={handleTrainChange} />
        Darken Train Lines
      </label>

      {/* Display the parallel score */}
      {parallelScore !== null && (
        <div>
          <h3>Parallel Score for Bus {selectedRoute}: {parallelScore}</h3>
        </div>
      )}

      {/* Display the rank */}
      {rank !== null && (
        <div>
          <h3> Rank for Bus {selectedRoute}: {rank}</h3>
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
        {busRouteData && (
          <GeoJSON 
            data={busRouteData}
            style={busRouteStyle}  // Apply line style for bus routes
            pointToLayer={pointToLayer}  // Apply marker style for bus stops
          />
        )}
        {proposedRoutesData && (
          <GeoJSON 
            data={proposedRoutesData}
            style={proposedRouteStyle}  // Apply line style for bus routes
            pointToLayer={proposedPointToLayer}  // Apply marker style for bus stops
          />
        )}
        {modifiedRoutesData && (
          <GeoJSON 
            data={modifiedRoutesData}
            style={modifiedRouteStyle}  // Apply line style for bus routes
            pointToLayer={modifiedPointToLayer}  // Apply marker style for bus stops
          />
        )}
      </MapContainer>
    </div>
  );
};

export default BusRouteSelector;
