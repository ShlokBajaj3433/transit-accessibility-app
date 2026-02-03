import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Map, Gamepad2, User } from 'lucide-react';

const Sidebar = () => {
    return (
        <div className="sidebar">
            <div className="sidebar-logo">
                <img src="/logo.jpg" alt="TransitEase Logo" className="sidebar-brand-logo" />
            </div>

            <nav className="sidebar-nav">
                <NavLink to="/home" className={({ isActive }) => `sidebar-item ${isActive ? 'active' : ''}`}>
                    <Home size={22} />
                    <span>Home</span>
                </NavLink>
                <NavLink to="/trips" className={({ isActive }) => `sidebar-item ${isActive ? 'active' : ''}`}>
                    <Map size={22} />
                    <span>My Trips</span>
                </NavLink>
                <NavLink to="/games" className={({ isActive }) => `sidebar-item ${isActive ? 'active' : ''}`}>
                    <Gamepad2 size={22} />
                    <span>Games</span>
                </NavLink>
                <NavLink to="/profile" className={({ isActive }) => `sidebar-item ${isActive ? 'active' : ''}`}>
                    <User size={22} />
                    <span>Profile</span>
                </NavLink>
            </nav>

            <div className="sidebar-footer">
                <div className="user-info">
                    <div className="user-avatar">C</div>
                    <div className="user-details">
                        <div className="user-name">Chuba</div>
                        <div className="user-role">Premium Member</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
