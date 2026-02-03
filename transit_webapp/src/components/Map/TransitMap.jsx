
import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png';

// Fix for default Leaflet marker icons not showing in React
// This is necessary because Webpack has issues with the default icon path
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
    iconRetinaUrl: iconRetina,
    iconUrl: icon,
    shadowUrl: iconShadow,
});

/**
 * Component to update map view when center prop changes
 * This allows the map to programmatically fly to new locations
 */
const MapUpdater = ({ center, zoom }) => {
    const map = useMap();
    useEffect(() => {
        if (center) {
            map.flyTo(center, zoom);
        }
    }, [center, zoom, map]);
    return null;
};

/**
 * TransitMap Component
 * 
 * Renders an interactive Leaflet map.
 * 
 * Props:
 * @param {Array} center - [latitude, longitude] coordinates for the map center. Default: Kuala Lumpur.
 * @param {number} zoom - Tool level. Default: 13.
 * @param {Array} markers - Array of objects { position: [lat, lng], popup: string } to display markers.
 * @param {string} className - CSS class for customization.
 */
const TransitMap = ({
    center = [3.1390, 101.6869], // Default to Kuala Lumpur
    zoom = 13,
    markers = [],
    className = "",
    style = { height: "100%", width: "100%" }
}) => {

    return (
        <div className={`map-container ${className}`} style={{ ...style, position: 'relative', zIndex: 0 }}>
            {/* MapContainer is the entry point for React-Leaflet */}
            <MapContainer
                center={center}
                zoom={zoom}
                scrollWheelZoom={true}
                style={{ height: "100%", width: "100%" }}
            >
                {/* 
                  TileLayer source. 
                  Using OpenStreetMap default tiles. 
                  Attribution is required by OSM.
                */}
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                {/* Helper component to handle updates to center/zoom props */}
                <MapUpdater center={center} zoom={zoom} />

                {/* Render any passed markers */}
                {markers.map((marker, idx) => (
                    <Marker key={idx} position={marker.position}>
                        {marker.popup && (
                            <Popup>
                                {marker.popup}
                            </Popup>
                        )}
                    </Marker>
                ))}

                {/* Example default marker for context if no markers provided */}
                {markers.length === 0 && (
                    <Marker position={center}>
                        <Popup>
                            Current Location
                        </Popup>
                    </Marker>
                )}
            </MapContainer>
        </div>
    );
};

export default TransitMap;
