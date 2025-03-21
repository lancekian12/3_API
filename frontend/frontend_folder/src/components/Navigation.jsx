// Navigation.jsx
import React from "react";
import { Link } from "react-router-dom";

function Navigation() {
    return (
        <nav className="p-4 bg-white shadow flex justify-between">
            <div className="text-xl font-bold">Cloud Programming</div>
            <div className="space-x-4">
                <Link to="/routine" className="text-gray-600 hover:text-black">
                    Routine
                </Link>
                <Link to="/weather" className="text-gray-600 hover:text-black">
                    Weather
                </Link>
                <Link to="/calories" className="text-gray-600 hover:text-black">
                    Calories
                </Link>
            </div>
        </nav>
    );
}

export default Navigation;
