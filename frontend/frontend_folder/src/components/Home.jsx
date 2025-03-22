import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import gymImage from "../assets/gym.png";

function Home() {
    const navigate = useNavigate();
    const [routineName, setRoutineName] = useState("");
    const [focus, setFocus] = useState("");
    const [level, setLevel] = useState("");
    const [dayTag, setDayTag] = useState("");

    const handleNext = (e) => {
        e.preventDefault();
        // Pass routine details to the ChooseExercise screen
        navigate("/choose-exercise", {
            state: {
                routineName,
                focus,
                level,
                dayTag,
            },
        });
    };

    return (
        <div className="flex h-screen font-sans">
            {/* Left Section */}
            <div className="flex-1 p-16 flex flex-col justify-center max-w-lg mx-auto">
                <h1 className="text-4xl font-bold mb-2 text-center">Let’s Get Started</h1>
                <h2 className="text-xl text-gray-600 mb-10 text-center">Create Your Routine</h2>

                <form className="flex flex-col space-y-6">
                    {/* Routine Name */}
                    <div>
                        <label htmlFor="routineName" className="block text-lg font-semibold mb-1">
                            Routine Plan
                        </label>
                        <input
                            type="text"
                            id="routineName"
                            placeholder="Name of the fitness routine"
                            className="w-full border border-gray-300 p-3 rounded-md"
                            value={routineName}
                            onChange={(e) => setRoutineName(e.target.value)}
                        />
                    </div>

                    {/* Focus */}
                    <div>
                        <h3 className="text-lg font-semibold mb-2">Focus</h3>
                        <div className="flex space-x-4">
                            {["Maintaining", "Bulking", "Cutting"].map((option) => (
                                <button
                                    key={option}
                                    type="button"
                                    className={`px-4 py-2 rounded-md transition-colors
                                    ${
                                        focus === option
                                            ? "bg-black text-white" // Selected style
                                            : "bg-white text-black border border-gray-300" // Default style
                                    }`}
                                    onClick={() => setFocus(option)}
                                >
                                    {option}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Level */}
                    <div>
                        <h3 className="text-lg font-semibold mb-2">Level</h3>
                        <div className="flex space-x-4">
                            {["Beginner", "Intermediate", "Advanced"].map((option) => (
                                <button
                                    key={option}
                                    type="button"
                                    className={`px-4 py-2 rounded-md transition-colors
                                    ${
                                        level === option
                                            ? "bg-black text-white" // Selected style
                                            : "bg-white text-black border border-gray-300" // Default style
                                    }`}
                                    onClick={() => setLevel(option)}
                                >
                                    {option}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Day Tag */}
                    <div>
                        <h3 className="text-lg font-semibold mb-2">Day Tag</h3>
                        <div className="flex space-x-4">
                            {["Weekday", "DayOfWeek"].map((option) => (
                                <button
                                    key={option}
                                    type="button"
                                    className={`px-4 py-2 rounded-md transition-colors
                                    ${
                                        dayTag === option
                                            ? "bg-black text-white" // Selected style
                                            : "bg-white text-black border border-gray-300" // Default style
                                    }`}
                                    onClick={() => setDayTag(option)}
                                >
                                    {option}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        onClick={handleNext}
                        className="bg-black text-white py-3 px-6 rounded-md mt-2 
                       hover:bg-gray-800 transition-colors text-lg"
                    >
                        Next
                    </button>
                </form>
            </div>

            {/* Right Section */}
            <div className="flex-1 overflow-hidden">
                <img src={gymImage} alt="Gym" className="w-full h-full object-cover" />
            </div>
        </div>
    );
}

export default Home;