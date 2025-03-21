import React from "react";
import { useNavigate } from "react-router-dom";
import gymImage from "../assets/gym.png";

function Home() {
    const navigate = useNavigate();

    const handleNext = (e) => {
        e.preventDefault();
        // ...maybe save form data here...
        navigate("/choose-exercise");
    };

    return (
        <div className="flex h-screen font-sans">
            {/* Left Section */}
            <div className="flex-1 p-16 flex flex-col justify-center max-w-lg mx-auto">
                {/* Main Headings */}
                <h1 className="text-4xl font-bold mb-2 text-center">
                    Let’s Get Started
                </h1>
                <h2 className="text-xl text-gray-600 mb-10 text-center">
                    Create Your Routine
                </h2>

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
                        />
                    </div>

                    {/* Focus */}
                    <div>
                        <h3 className="text-lg font-semibold mb-2">Focus</h3>
                        <div className="flex space-x-6">
                            <label className="flex items-center space-x-1">
                                <input
                                    type="radio"
                                    name="focus"
                                    value="Maintaining"
                                    className="form-radio h-5 w-5"
                                />
                                <span>Maintaining</span>
                            </label>
                            <label className="flex items-center space-x-1">
                                <input
                                    type="radio"
                                    name="focus"
                                    value="Bulking"
                                    className="form-radio h-5 w-5"
                                />
                                <span>Bulking</span>
                            </label>
                            <label className="flex items-center space-x-1">
                                <input
                                    type="radio"
                                    name="focus"
                                    value="Cutting"
                                    className="form-radio h-5 w-5"
                                />
                                <span>Cutting</span>
                            </label>
                        </div>
                    </div>

                    {/* Level */}
                    <div>
                        <h3 className="text-lg font-semibold mb-2">Level</h3>
                        <div className="flex space-x-6">
                            <label className="flex items-center space-x-1">
                                <input
                                    type="radio"
                                    name="level"
                                    value="Beginner"
                                    className="form-radio h-5 w-5"
                                />
                                <span>Beginner</span>
                            </label>
                            <label className="flex items-center space-x-1">
                                <input
                                    type="radio"
                                    name="level"
                                    value="Intermediate"
                                    className="form-radio h-5 w-5"
                                />
                                <span>Intermediate</span>
                            </label>
                            <label className="flex items-center space-x-1">
                                <input
                                    type="radio"
                                    name="level"
                                    value="Advanced"
                                    className="form-radio h-5 w-5"
                                />
                                <span>Advanced</span>
                            </label>
                        </div>
                    </div>

                    {/* Day Tag */}
                    <div>
                        <h3 className="text-lg font-semibold mb-2">Day Tag</h3>
                        <div className="flex space-x-6">
                            <label className="flex items-center space-x-1">
                                <input
                                    type="radio"
                                    name="dayTag"
                                    value="Weekday"
                                    className="form-radio h-5 w-5"
                                />
                                <span>Weekday</span>
                            </label>
                            <label className="flex items-center space-x-1">
                                <input
                                    type="radio"
                                    name="dayTag"
                                    value="DayOfWeek"
                                    className="form-radio h-5 w-5"
                                />
                                <span>Day of Week</span>
                            </label>
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
                <img
                    src={gymImage}
                    alt="Gym"
                    className="w-full h-full object-cover"
                />
            </div>
        </div>
    );
}

export default Home;
