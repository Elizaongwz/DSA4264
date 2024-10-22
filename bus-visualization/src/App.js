import React, { useState } from 'react';
import BusRouteSelector from './BusRouteSelector';
import MapDisplay from './MapDisplay';
import ParallelScore from './ParallelScore';

const App = () => {
    const [selectedRoute, setSelectedRoute] = useState('');

    return (
        <div className="App">
            <h1>Bus Route Visualizer</h1>
            <BusRouteSelector onRouteSelect={setSelectedRoute} />
            <MapDisplay selectedRoute={selectedRoute} />
            <ParallelScore selectedRoute={selectedRoute} />
        </div>
    );
};

export default App;
