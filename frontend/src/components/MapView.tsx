import { MapContainer, TileLayer, Marker, Polyline, Popup } from 'react-leaflet'
import { Icon } from 'leaflet'

// Mock data for demonstration
const mockUserLocation: [number, number] = [40.7128, -74.0060] // New York City
const mockRoute: [number, number][] = [
  [40.7128, -74.0060],
  [40.7180, -74.0020],
  [40.7230, -73.9980],
  [40.7280, -73.9940]
]

// Fix for default marker icon in react-leaflet
const createCustomIcon = (color: string) => {
  return new Icon({
    iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  })
}

const userIcon = createCustomIcon('blue')
const destinationIcon = createCustomIcon('red')

interface MapViewProps {
  className?: string
}

function MapView({ className = '' }: MapViewProps) {
  return (
    <div className={`relative ${className}`}>
      <MapContainer
        center={mockUserLocation}
        zoom={13}
        className="h-full w-full"
        whenReady={() => {
        console.log('Leaflet map initialized')}}

        zoomControl={true}
        attributionControl={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* User location marker */}
        <Marker position={mockUserLocation} icon={userIcon}>
          <Popup>
            <div className="text-sm">
              <strong>Your Location</strong>
              <p className="text-gray-600">Starting point</p>
            </div>
          </Popup>
        </Marker>

        {/* Destination marker */}
        <Marker position={mockRoute[mockRoute.length - 1]} icon={destinationIcon}>
          <Popup>
            <div className="text-sm">
              <strong>Destination</strong>
              <p className="text-gray-600">End point</p>
            </div>
          </Popup>
        </Marker>

        {/* Route polyline */}
        <Polyline
          positions={mockRoute}
          color="#3b82f6"
          weight={4}
          opacity={0.7}
        />
      </MapContainer>
    </div>
  )
}

export default MapView
