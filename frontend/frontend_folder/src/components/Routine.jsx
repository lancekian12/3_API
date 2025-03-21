import React from "react";

function Routine() {
    return (
        <div className="p-8">
            <h1 className="text-2xl font-bold mb-4">My Routine Name</h1>

            {/* Focus / Level / Day Tag */}
            <div className="flex items-center space-x-4 mb-8">
                <span className="bg-gray-200 px-2 py-1 rounded">Maintaining</span>
                <span className="bg-gray-200 px-2 py-1 rounded">Intermediate</span>
                <span className="bg-gray-200 px-2 py-1 rounded">Day of Week</span>
            </div>

            {/* Example: Two columns of exercises */}
            <div className="grid grid-cols-2 gap-4">
                {/* Exercise 1 */}
                <div className="border border-gray-300 p-4 rounded">
                    <h2 className="font-semibold mb-2">Machine Bench Press</h2>
                    <div className="flex space-x-4">
                        <div>
                            <label className="block font-semibold">Sets</label>
                            <input type="number" className="border p-1 rounded w-16" defaultValue="3" />
                        </div>
                        <div>
                            <label className="block font-semibold">Reps</label>
                            <input type="number" className="border p-1 rounded w-16" defaultValue="8" />
                        </div>
                        <div>
                            <label className="block font-semibold">Interval</label>
                            <input type="text" className="border p-1 rounded w-16" defaultValue="1:00" />
                        </div>
                        <div>
                            <label className="block font-semibold">Rest Time</label>
                            <input type="text" className="border p-1 rounded w-16" defaultValue="1:00" />
                        </div>
                    </div>
                </div>

                {/* Exercise 2 */}
                <div className="border border-gray-300 p-4 rounded">
                    <h2 className="font-semibold mb-2">Push-Up</h2>
                    <div className="flex space-x-4">
                        <div>
                            <label className="block font-semibold">Sets</label>
                            <input type="number" className="border p-1 rounded w-16" defaultValue="3" />
                        </div>
                        <div>
                            <label className="block font-semibold">Reps</label>
                            <input type="number" className="border p-1 rounded w-16" defaultValue="8" />
                        </div>
                        <div>
                            <label className="block font-semibold">Interval</label>
                            <input type="text" className="border p-1 rounded w-16" defaultValue="1:00" />
                        </div>
                        <div>
                            <label className="block font-semibold">Rest Time</label>
                            <input type="text" className="border p-1 rounded w-16" defaultValue="1:00" />
                        </div>
                    </div>
                </div>

                {/* Add more exercises as needed */}
            </div>
        </div>
    );
}

export default Routine;
