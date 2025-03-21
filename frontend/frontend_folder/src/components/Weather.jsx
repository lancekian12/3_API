import React from "react";

function Weather() {
    return (
        <div className="p-8 text-center">
            <h1 className="text-2xl font-bold mb-4">32°C</h1>
            <p className="text-gray-600 mb-4">Wednesday - Mostly Cloudy</p>

            {/* Forecast for 5 days */}
            <div className="flex justify-center space-x-6 text-gray-600">
                <div>
                    <div>Wed</div>
                    <div>32°C / 23°C</div>
                </div>
                <div>
                    <div>Thu</div>
                    <div>31°C / 22°C</div>
                </div>
                <div>
                    <div>Fri</div>
                    <div>31°C / 22°C</div>
                </div>
                <div>
                    <div>Sat</div>
                    <div>32°C / 23°C</div>
                </div>
                <div>
                    <div>Sun</div>
                    <div>32°C / 23°C</div>
                </div>
            </div>
        </div>
    );
}

export default Weather;
