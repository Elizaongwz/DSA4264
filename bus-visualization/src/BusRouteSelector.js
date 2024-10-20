import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BusRouteSelector = ({ onRoutesSelect }) => {
    const [busRoutes, setBusRoutes] = useState([]);
    const [selectedRoutes, setSelectedRoutes] = useState([]);

    useEffect(() => {
        // Fetch bus routes from Spring Boot
        axios.get('http://localhost:8080/bus/routes')
            .then(response => {
                console.log(response.data);
                setBusRoutes(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching bus routes!", error);
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
        </div>
    );
};

export default BusRouteSelector;
