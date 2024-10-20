import React, { useState } from 'react';
import BusRouteSelector from './BusRouteSelector';
import MapDisplay from './MapDisplay';
import ParallelScore from './ParallelScore';

const App = () => {
    const [selectedRoutes, setSelectedRoutes] = useState([]);

    return (
        <div className="App">
            <h1>Bus Route Visualizer</h1>
            <BusRouteSelector onRoutesSelect={setSelectedRoutes} />
            <MapDisplay selectedRoutes={selectedRoutes} />
            <ParallelScore selectedRoutes={selectedRoutes} />
        </div>
    );
};

export default App;

