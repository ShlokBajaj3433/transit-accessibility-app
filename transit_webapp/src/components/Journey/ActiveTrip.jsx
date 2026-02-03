import React from 'react';

const ActiveTrip = ({ currentAction, destination }) => {
    const handleStop = () => {
        console.log('Trip stopped');
    };

    return (
        <div className="screen">
            <div className="active-trip-header">
                <h2>{currentAction}</h2>
                <p>To {destination}</p>
            </div>

            <div className="active-trip-map">
                {/* Map placeholder - Integrate with mapping library */}
                <div>Active Trip Map with Route Tracing</div>
            </div>

            <button className="stop-button" onClick={handleStop}>
                ⏹️ STOP TRIP
            </button>
        </div>
    );
};

export default ActiveTrip;
