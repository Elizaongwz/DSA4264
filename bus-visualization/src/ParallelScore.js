import React, { useState } from 'react';
import axios from 'axios';

const ParallelScore = ({ selectedRoutes }) => {
    const [scores, setScores] = useState({});

    const handleGetScores = () => {
        axios.post('http://localhost:8080/api/parallelScore', {
            busRoutes: selectedRoutes
          })
          .then(response => {
            setScores(response.data); // Get the parallel scores
          })
          .catch(error => {
            console.error("Error calculating parallel scores:", error);
          });
    };

    return (
        <div>
            <button onClick={handleGetScores}>Calculate Parallel Scores</button>
            {Object.keys(scores).length > 0 && (
                <div>
                    <h3>Parallel Scores:</h3>
                    <ul>
                        {Object.entries(scores).map(([route, score]) => (
                            <li key={route}>
                                {route}: {score}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default ParallelScore;
