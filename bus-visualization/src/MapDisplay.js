import React, { useState } from 'react';
import axios from 'axios';

const MapDisplay = ({ selectedRoutes }) => {
    const [mapHtml, setMapHtml] = useState('');

    const handlePlotRoutes = () => {
        // Post selected routes to Spring Boot
        axios.post('http://localhost:8080/api/plotRoutes', {
            busRoutes: selectedRoutes
          })
          .then(response => {
            setMapHtml(response.data);  // Get the map HTML
          })
          .catch(error => {
            console.error("Error plotting bus routes:", error);
          });

    };

    return (
        <div>
            <button onClick={handlePlotRoutes}>Plot Bus Routes</button>
            {mapHtml && (
                <div dangerouslySetInnerHTML={{ __html: mapHtml }} />
            )}
        </div>
    );
};

export default MapDisplay;
