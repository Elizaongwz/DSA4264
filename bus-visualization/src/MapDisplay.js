import React, { useState } from 'react';
import axios from 'axios';

const MapDisplay = ({ selectedRoute }) => {
    const [mapHtml, setMapHtml] = useState('');

    const handlePlotRoutes = () => {
      if (selectedRoute) {
        const requestBody = {
          service_no: selectedRoute
        };
        console.log("Request Body:", requestBody); // Add this line to verify the request body
        axios.post('http://localhost:8080/api/plot_routes', requestBody)
        .then(response => {
          console.log("Response from API:", response.data);
          setMapHtml(response.data);
        })
        .catch(error => {
          if (error.response) {
            console.error("Error response from server:", error.response.data);
            console.error("Status code:", error.response.status);
            console.error("Headers:", error.response.headers);
          } else if (error.request) {
            console.error("No response received:", error.request);
          } else {
            console.error("Error in setting up request:", error.message);
          }
        });
      }
    }

    return (
        <div>
            <button onClick={handlePlotRoutes}>Plot Bus Route</button>
            {mapHtml && (
                <div dangerouslySetInnerHTML={{ __html: mapHtml }} />
            )}
        </div>
    );
};

export default MapDisplay;
