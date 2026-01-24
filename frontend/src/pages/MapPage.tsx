import MapView from "../components/MapView";

export default function MapPage() {
  return (
    <div className="h-screen w-screen flex flex-col">
      {/* Map container */}
      <div className="flex-1">
        <MapView />
      </div>

      {/* Bottom info panel */}
      <div className="p-4 border-t bg-white">
        <p className="text-sm font-medium">ETA: --</p>
        <p className="text-sm text-gray-600">Distance: --</p>
        <p className="text-sm text-gray-600">Status: Waiting for route</p>
      </div>
    </div>
  );
}
