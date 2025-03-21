import React from "react";
import { NavLink } from "react-router-dom";

function Navigation() {
    const baseClasses = "px-3 py-2 rounded text-lg font-medium";

    return (
        <nav className="p-6 bg-white flex justify-between items-center">
            {/* Left: Title or Logo */}
            <div className="text-2xl font-bold">Cloud Programming</div>

            {/* Right: Links */}
            <div className="space-x-4">
                <NavLink
                    to="/routine"
                    className={({ isActive }) =>
                        isActive
                            ? `bg-black text-white ${baseClasses}`
                            : `text-gray-600 hover:text-black ${baseClasses}`
                    }
                >
                    Routine
                </NavLink>

                <NavLink
                    to="/weather"
                    className={({ isActive }) =>
                        isActive
                            ? `bg-black text-white ${baseClasses}`
                            : `text-gray-600 hover:text-black ${baseClasses}`
                    }
                >
                    Weather
                </NavLink>

                <NavLink
                    to="/calories"
                    className={({ isActive }) =>
                        isActive
                            ? `bg-black text-white ${baseClasses}`
                            : `text-gray-600 hover:text-black ${baseClasses}`
                    }
                >
                    Calories
                </NavLink>
            </div>
        </nav>
    );
}

export default Navigation;
