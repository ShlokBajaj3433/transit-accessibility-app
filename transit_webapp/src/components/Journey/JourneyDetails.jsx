import React from 'react';
import ImpactBanner from './ImpactBanner';
import Itinerary from './Itinerary';

const JourneyDetails = () => {
    const steps = [
        {
            icon: '🚶',
            title: 'Walk to Shola Market',
            subtitle: '5 mins • 400m'
        },
        {
            icon: '🚌',
            title: 'Take Bus 42',
            subtitle: 'Board at Shola Market • 15 mins'
        },
        {
            icon: '🚶',
            title: 'Walk to destination',
            subtitle: '3 mins • 200m'
        },
        {
            icon: '📍',
            title: 'Arrive at City Center',
            subtitle: '10:55 AM'
        }
    ];

    return (
        <div className="screen">
            <ImpactBanner
                type="green"
                message="🌱 This route produces 38% less emissions than driving"
            />
            <Itinerary steps={steps} />
        </div>
    );
};

export default JourneyDetails;
