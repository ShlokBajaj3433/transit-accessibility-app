import React, { useState, useMemo } from 'react';
import WeatherCard from './WeatherCard';
import CO2Card from './CO2Card';
import SearchBar from './SearchBar';
import { MapPin, Bus, Train, TrainFront, ChevronDown, Star } from 'lucide-react';
import RouteCard from '../Transit/RouteCard';
import TransitMap from '../Map/TransitMap';

const Home = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('bus');
  const [activeFilters, setActiveFilters] = useState(['accessible']);

  const routes = [
    {
      id: 1,
      type: 'bus',
      recommended: true,
      station: 'Meskel Square Station',
      distance: '6.5 km',
      duration: '25 mins',
      arrivalTime: '8:50 pm',
      cost: '$1.80',
      co2: '320g',
      tags: ['Accessible'],
      coordinates: [3.145, 101.690],
    },
    {
      id: 2,
      type: 'bus',
      recommended: false,
      station: 'Meskel Square Station',
      distance: '5.0 km',
      duration: '40 mins',
      arrivalTime: '8:30 pm',
      cost: '$1.50',
      co2: '200g',
      tags: ['Accessible'],
      isRisk: true,
      riskText: 'Risky Area (Bad Pollution)',
      coordinates: [3.140, 101.695],
    },
    {
      id: 3,
      type: 'train',
      recommended: true,
      station: 'Lideta Train Station',
      distance: '3.2 km',
      duration: '15 mins',
      arrivalTime: '8:45 pm',
      cost: '$2.50',
      co2: '150g',
      tags: ['Accessible'],
      coordinates: [3.135, 101.680],
    },
    {
      id: 4,
      type: 'mrt',
      recommended: false,
      station: 'Central MRT Station',
      distance: '4.0 km',
      duration: '18 mins',
      arrivalTime: '8:40 pm',
      cost: '$2.00',
      co2: '120g',
      tags: [],
      coordinates: [3.138, 101.688],
    },
  ];

  // ✅ Proper filtering logic
  const filteredRoutes = useMemo(() => {
    return routes
      .filter(r => r.type === activeTab)
      .filter(r => {
        if (activeFilters.includes('accessible') && !r.tags?.includes('Accessible')) {
          return false;
        }
        return true;
      });
  }, [routes, activeTab, activeFilters]);

  const isSearching = searchQuery.trim() !== '';

  return (
    <div className={`home-screen screen ${isSearching ? 'searching' : ''}`}>
      {!isSearching ? (
        <div className="home-content" style={{ paddingTop: 24, paddingBottom: 100 }}>
          {/* Header */}
          <div className="home-header">
            <div className="home-greeting">
              <div style={{ fontSize: 14, color: '#6C757D' }}>Welcome Back!</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <MapPin size={16} color="#D32F2F" fill="#D32F2F" />
                <h2 style={{ margin: 0, fontSize: 18 }}>Kuala Lumpur</h2>
              </div>
            </div>
          </div>

          {/* Weather + CO₂ */}
          <div className="home-grid">
            <WeatherCard />
            <CO2Card />
          </div>

          {/* Map */}
          <div style={{ marginTop: 24 }}>
            <h3 style={{ fontSize: 16, fontWeight: 600 }}>Nearby Transit Stations</h3>
            <div style={{ height: 300, borderRadius: 20, overflow: 'hidden' }}>
              <TransitMap
                center={[3.139, 101.6869]}
                zoom={13}
                markers={routes.map(r => ({
                  position: r.coordinates,
                  popup: `${r.station} (${r.duration})`,
                }))}
              />
            </div>
          </div>

          {/* Search */}
          <div style={{ marginTop: 24 }}>
            <SearchBar value={searchQuery} onChange={setSearchQuery} />
          </div>
        </div>
      ) : (
        <>
          {/* Search Map */}
          <div className="search-visual-header">
            <TransitMap
              markers={filteredRoutes.map(r => ({
                position: r.coordinates,
                popup: `${r.type.toUpperCase()} - ${r.station}`,
              }))}
            />
          </div>

          {/* Results Panel */}
          <div className="home-search-results-fixed">
            <div className="sheet-handle" />

            <div className="results-panel-content">
              <SearchBar
                value={searchQuery}
                onChange={setSearchQuery}
                autoFocus
              />

              <div className="results-header-row">
                <h3>Suggested Routes</h3>
                <span onClick={() => setSearchQuery('')} className="cancel-search-btn">
                  Cancel
                </span>
              </div>

              {/* Filters */}
              <div className="filters-scroll-row">
                <div className="filter-chip dropdown">
                  <span>Depart Now</span>
                  <ChevronDown size={14} />
                </div>

                <div
                  className={`filter-chip ${activeFilters.includes('accessible') ? 'active' : ''}`}
                  onClick={() =>
                    setActiveFilters(prev =>
                      prev.includes('accessible')
                        ? prev.filter(f => f !== 'accessible')
                        : [...prev, 'accessible']
                    )
                  }
                >
                  Accessible
                </div>
              </div>

              {/* Tabs */}
              <div className="transport-tabs-row">
                <div className={`transport-tab-item ${activeTab === 'bus' ? 'active' : ''}`} onClick={() => setActiveTab('bus')}>
                  <Bus size={20} />
                  <span>Bus</span>
                </div>

                <div className={`transport-tab-item ${activeTab === 'train' ? 'active' : ''}`} onClick={() => setActiveTab('train')}>
                  <Train size={20} />
                  <span>Train</span>
                </div>

                <div className={`transport-tab-item ${activeTab === 'mrt' ? 'active' : ''}`} onClick={() => setActiveTab('mrt')}>
                  <TrainFront size={20} />
                  <span>MRT/LRT</span>
                </div>
              </div>

              {/* Routes */}
              {filteredRoutes.length ? (
                <>
                  {filteredRoutes[0].recommended && (
                    <div className="recommended-label">
                      <Star size={12} />
                      <span>Recommended</span>
                    </div>
                  )}
                  {filteredRoutes.map(route => (
                    <RouteCard key={route.id} route={route} />
                  ))}
                </>
              ) : (
                <div className="no-results-msg">No routes found.</div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Home;
