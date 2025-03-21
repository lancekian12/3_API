import React from "react";
import weatherIcon from "../assets/weather.png"; // <-- Make sure the path is correct

function Weather() {
    return (
        <div className="p-8 text-center flex flex-col items-center">
            {/* Main Current Weather */}
            <div className="mb-8">
                {/* Big Weather Icon */}
                <img
                    src={weatherIcon}
                    alt="Weather icon"
                    className="w-32 h-32 mx-auto mb-4"
                />

                {/* Current Temperature */}
                <h1 className="text-5xl font-bold mb-2">32°C</h1>
                <p className="text-xl text-gray-600">Wednesday - Mostly Cloudy</p>
            </div>

            {/* Forecast for the next 5 days */}
            <div className="grid grid-cols-5 gap-6">
                {/* Day 1 */}
                <div className="flex flex-col items-center">
                    <img src={weatherIcon} alt="Weather icon" className="w-12 h-12 mb-2" />
                    <div className="font-semibold">Wed</div>
                    <div className="text-gray-600">32°C / 23°C</div>
                </div>

                {/* Day 2 */}
                <div className="flex flex-col items-center">
                    <img src={weatherIcon} alt="Weather icon" className="w-12 h-12 mb-2" />
                    <div className="font-semibold">Thu</div>
                    <div className="text-gray-600">31°C / 22°C</div>
                </div>

                {/* Day 3 */}
                <div className="flex flex-col items-center">
                    <img src={weatherIcon} alt="Weather icon" className="w-12 h-12 mb-2" />
                    <div className="font-semibold">Fri</div>
                    <div className="text-gray-600">31°C / 22°C</div>
                </div>

                {/* Day 4 */}
                <div className="flex flex-col items-center">
                    <img src={weatherIcon} alt="Weather icon" className="w-12 h-12 mb-2" />
                    <div className="font-semibold">Sat</div>
                    <div className="text-gray-600">32°C / 23°C</div>
                </div>

                {/* Day 5 */}
                <div className="flex flex-col items-center">
                    <img src={weatherIcon} alt="Weather icon" className="w-12 h-12 mb-2" />
                    <div className="font-semibold">Sun</div>
                    <div className="text-gray-600">32°C / 23°C</div>
                </div>
            </div>
        </div>
    );
}

export default Weather;
