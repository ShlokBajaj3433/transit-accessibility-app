import { Search, MapPin } from 'lucide-react';

/**
 * SearchBar Component
 * 
 * A controlled search input component with location and search icons.
 * 
 * Props:
 * @param {string} value - Current search value (controlled)
 * @param {string} value - Current search value (controlled)
 * @param {function} onChange - Callback when search text changes
 * @param {boolean} autoFocus - Whether to focus input on mount
 */
const SearchBar = ({ value = '', onChange, autoFocus = false }) => {
    return (
        <div className="search-bar-container">
            <div className="search-bar" style={{ borderRadius: '100px', padding: '12px 20px' }}>
                <MapPin
                    color="#343A40"
                    size={20}
                />
                <input
                    type="text"
                    className="search-input"
                    placeholder="Where do you want to go?"
                    value={value}
                    onChange={(e) => onChange && onChange(e.target.value)}
                    style={{ fontWeight: '500' }}
                    autoFocus={autoFocus}
                />
                <Search
                    color="#343A40"
                    size={20}
                    style={{ cursor: 'pointer' }}
                />
            </div>
        </div>
    );
};

export default SearchBar;
