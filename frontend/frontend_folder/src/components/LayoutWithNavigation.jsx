// LayoutWithNavigation.jsx
import React from "react";
import Navigation from "./Navigation";
import { Outlet } from "react-router-dom";

function LayoutWithNavigation() {
    return (
        <div>
            <Navigation />
            {/* Renders the child route (Routine, Weather, Calories) below the nav */}
            <Outlet />
        </div>
    );
}

export default LayoutWithNavigation;
