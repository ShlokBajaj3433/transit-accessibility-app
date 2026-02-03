import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Map, Gamepad2, User } from 'lucide-react';

const BottomNav = () => {
    return (
        <div className="bottom-nav">
            <NavLink to="/home" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <Home size={24} />
                <span>Home</span>
            </NavLink>
            <NavLink to="/trips" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <Map size={24} />
                <span>My Trips</span>
            </NavLink>
            <NavLink to="/games" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <Gamepad2 size={24} />
                <span>Games</span>
            </NavLink>
            <NavLink to="/profile" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <User size={24} />
                <span>Profile</span>
            </NavLink>
        </div>
    );
};

export default BottomNav;
