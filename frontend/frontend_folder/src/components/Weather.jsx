import React, { useState, useEffect } from "react";
import weatherIcon from "../assets/weather.png"; // Ensure this path is correct

function Weather() {
    const [currentWeather, setCurrentWeather] = useState(null);
    const [error, setError] = useState(null);

    // Hard-coded location for demo
    const location = "Dagupan";

    useEffect(() => {
        const fetchWeather = async () => {
            try {
                // Directly calling the Flask server at localhost:5000
                const response = await fetch(`http://localhost:5000/weather?location=${location}`);
                if (!response.ok) {
                    throw new Error(`Failed to fetch weather data. Status: ${response.status}`);
                }

                const data = await response.json();
                setCurrentWeather(data);
            } catch (err) {
                setError(err.message);
            }
        };

        fetchWeather();
    }, [location]);

    if (error) {
        return <div className="text-center text-red-500">Error: {error}</div>;
    }

    if (!currentWeather) {
        return <div className="text-center">Loading...</div>;
    }

    // The WeatherAPI JSON typically has:
    // {
    //   current: { temp_c, condition, ... },
    //   location: { name, region, country, ... }
    // }
    const { temp_c, condition } = currentWeather.current;
    const { name } = currentWeather.location; // e.g. "Dagupan"

    return (
        <div className="p-8 text-center flex flex-col items-center">
            {/* Location Name */}
            <h2 className="text-3xl font-semibold mb-4">
                Weather in {name}
            </h2>

            {/* Main Current Weather */}
            <div className="mb-8">
                {/* Big Weather Icon */}
                <img
                    src={weatherIcon}
                    alt="Weather icon"
                    className="w-32 h-32 mx-auto mb-4"
                />

                {/* Current Temperature */}
                <h1 className="text-5xl font-bold mb-2">{temp_c}°C</h1>
                <p className="text-xl text-gray-600">
                    Today - {condition.text}
                </p>
            </div>

            {/* Static 7-day forecast (placeholder) */}
            <div className="grid grid-cols-7 gap-6">
                {/* Monday */}
                <div className="flex flex-col items-center">
                    <img src={weatherIcon} alt="Weather icon" className="w-12 h-12 mb-2" />
                    <div className="font-semibold">Mon</div>
                    <div className="text-gray-600">32°C / 23°C</div>
                </div>

                {/* Tuesday */}
                <div className="flex flex-col items-center">
                    <img src={weatherIcon} alt="Weather icon" className="w-12 h-12 mb-2" />
                    <div className="font-semibold">Tue</div>
                    <div className="text-gray-600">31°C / 22°C</div>
                </div>

                {/* Wednesday */}
                <div className="flex flex-col items-center">
                    <img src={weatherIcon} alt="Weather icon" className="w-12 h-12 mb-2" />
                    <div className="font-semibold">Wed</div>
                    <div className="text-gray-600">32°C / 23°C</div>
                </div>

                {/* Thursday */}
                <div className="flex flex-col items-center">
                    <img src={weatherIcon} alt="Weather icon" className="w-12 h-12 mb-2" />
                    <div className="font-semibold">Thu</div>
                    <div className="text-gray-600">31°C / 22°C</div>
                </div>

                {/* Friday */}
                <div className="flex flex-col items-center">
                    <img src={weatherIcon} alt="Weather icon" className="w-12 h-12 mb-2" />
                    <div className="font-semibold">Fri</div>
                    <div className="text-gray-600">31°C / 22°C</div>
                </div>

                {/* Saturday */}
                <div className="flex flex-col items-center">
                    <img src={weatherIcon} alt="Weather icon" className="w-12 h-12 mb-2" />
                    <div className="font-semibold">Sat</div>
                    <div className="text-gray-600">32°C / 23°C</div>
                </div>

                {/* Sunday */}
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
