import React from "react";

function Routine() {
    return (
        <div className="p-8 max-w-5xl mx-auto">
            {/* Page Title */}
            <h1 className="text-2xl font-bold mb-6">My Routine Name</h1>

            {/* Focus / Level / Day Tag */}
            <div className="flex items-center space-x-4 mb-10">
                <span className="bg-black text-white px-3 py-1 rounded-full">
                    Maintaining
                </span>
                <span className="bg-black text-white px-3 py-1 rounded-full">
                    Intermediate
                </span>
                <span className="bg-black text-white px-3 py-1 rounded-full">
                    Day of Week
                </span>
            </div>

            {/* Two columns of exercises */}
            <div className="grid grid-cols-2 gap-8">
                {/* Exercise 1 */}
                <div className="border border-black rounded overflow-hidden">
                    {/* Exercise Header (Black Bar) */}
                    <div className="bg-black text-white p-2 flex justify-between items-center">
                        <h2 className="font-semibold">Machine Bench Press</h2>
                        <span className="font-medium">Legs</span>
                    </div>

                    {/* White area for sets/reps/interval/rest */}
                    <div className="bg-white p-4 text-black flex space-x-4">
                        <div>
                            <label className="block font-semibold mb-1">Sets</label>
                            <input
                                type="number"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="3"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Reps</label>
                            <input
                                type="number"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="8"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Interval</label>
                            <input
                                type="text"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="1:00"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Rest Time</label>
                            <input
                                type="text"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="1:00"
                            />
                        </div>
                    </div>
                </div>

                {/* Exercise 2 */}
                <div className="border border-black rounded overflow-hidden">
                    {/* Exercise Header (Black Bar) */}
                    <div className="bg-black text-white p-2 flex justify-between items-center">
                        <h2 className="font-semibold">Push-Up</h2>
                        <span className="font-medium">Chest</span>
                    </div>

                    {/* White area for sets/reps/interval/rest */}
                    <div className="bg-white p-4 text-black flex space-x-4">
                        <div>
                            <label className="block font-semibold mb-1">Sets</label>
                            <input
                                type="number"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="3"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Reps</label>
                            <input
                                type="number"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="8"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Interval</label>
                            <input
                                type="text"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="1:00"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Rest Time</label>
                            <input
                                type="text"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="1:00"
                            />
                        </div>
                    </div>
                </div>

                {/* Exercise 3 */}
                <div className="border border-black rounded overflow-hidden">
                    <div className="bg-black text-white p-2 flex justify-between items-center">
                        <h2 className="font-semibold">Dumbbell Shoulder Shrug</h2>
                        <span className="font-medium">Back</span>
                    </div>
                    <div className="bg-white p-4 text-black flex space-x-4">
                        <div>
                            <label className="block font-semibold mb-1">Sets</label>
                            <input
                                type="number"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="3"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Reps</label>
                            <input
                                type="number"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="8"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Interval</label>
                            <input
                                type="text"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="1:00"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Rest Time</label>
                            <input
                                type="text"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="1:00"
                            />
                        </div>
                    </div>
                </div>

                {/* Exercise 4 */}
                <div className="border border-black rounded overflow-hidden">
                    <div className="bg-black text-white p-2 flex justify-between items-center">
                        <h2 className="font-semibold">Machine Hip Abduction</h2>
                        <span className="font-medium">Upper Legs</span>
                    </div>
                    <div className="bg-white p-4 text-black flex space-x-4">
                        <div>
                            <label className="block font-semibold mb-1">Sets</label>
                            <input
                                type="number"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="3"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Reps</label>
                            <input
                                type="number"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="8"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Interval</label>
                            <input
                                type="text"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="1:00"
                            />
                        </div>
                        <div>
                            <label className="block font-semibold mb-1">Rest Time</label>
                            <input
                                type="text"
                                className="border border-gray-300 p-1 rounded w-16"
                                defaultValue="1:00"
                            />
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}

export default Routine;
