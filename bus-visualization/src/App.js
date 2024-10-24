import React, { useState } from 'react';
import BusRouteSelector from './BusRouteSelector';

const App = () => {
    const [selectedRoute, setSelectedRoute] = useState('');

    return (
        <div className="App">
            <h1>Bus Route Visualiser</h1>
            <div className='bus-route-selector-container'>
                <BusRouteSelector onRouteSelect={setSelectedRoute} />
            </div>
        </div>
    );
};

export default App;
