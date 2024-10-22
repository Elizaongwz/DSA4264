import React, { useState } from 'react';
import axios from 'axios';

const MapDisplay = ({ selectedRoutes }) => {
    const [mapHtml, setMapHtml] = useState('');
    const handlePlotRoutes = () => {
      if (selectedRoutes.length > 0) {
        const requestBody = {
          service_no: selectedRoutes[0]
        };
        console.log("Request Body:", requestBody); // Add this line to verify the request body
        axios.post('http://localhost:8080/api/plot_routes', requestBody)
        .then(response => {
          console.log("Response from API:", response.data);
          setMapHtml(response.data);
        })
        .catch(error => {
          if (error.response) {
            // The request was made, and the server responded with a status code out of the 2xx range
            console.error("Error response from server:", error.response.data);
            console.error("Status code:", error.response.status);
            console.error("Headers:", error.response.headers);
          } else if (error.request) {
            // The request was made but no response was received
            console.error("No response received:", error.request);
          } else {
            // Something else caused the error
            console.error("Error in setting up request:", error.message);
          }
        })
      }
    }

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
