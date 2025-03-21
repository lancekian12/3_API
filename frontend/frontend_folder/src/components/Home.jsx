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
            <div className="flex-1 p-8 flex flex-col justify-center">
                <h1 className="text-2xl font-bold mb-2 text-center">Let’s Get Started</h1>
                <h2 className="text-lg text-gray-600 mb-8 text-center">Create Your Routine</h2>

                <form className="flex flex-col space-y-4">
                    {/* Routine Name */}
                    <label htmlFor="routineName" className="font-semibold">
                        Routine Plan
                    </label>
                    <input
                        type="text"
                        id="routineName"
                        placeholder="Name of the fitness routine"
                        className="border border-gray-300 p-2 rounded-md"
                    />

                    {/* Focus */}
                    <h3 className="font-semibold">Focus</h3>
                    <div className="flex space-x-4">
                        <label className="flex items-center space-x-1">
                            <input type="radio" name="focus" value="Maintaining" className="form-radio" />
                            <span>Maintaining</span>
                        </label>
                        <label className="flex items-center space-x-1">
                            <input type="radio" name="focus" value="Bulking" className="form-radio" />
                            <span>Bulking</span>
                        </label>
                        <label className="flex items-center space-x-1">
                            <input type="radio" name="focus" value="Cutting" className="form-radio" />
                            <span>Cutting</span>
                        </label>
                    </div>

                    {/* Level */}
                    <h3 className="font-semibold">Level</h3>
                    <div className="flex space-x-4">
                        <label className="flex items-center space-x-1">
                            <input type="radio" name="level" value="Beginner" className="form-radio" />
                            <span>Beginner</span>
                        </label>
                        <label className="flex items-center space-x-1">
                            <input type="radio" name="level" value="Intermediate" className="form-radio" />
                            <span>Intermediate</span>
                        </label>
                        <label className="flex items-center space-x-1">
                            <input type="radio" name="level" value="Advanced" className="form-radio" />
                            <span>Advanced</span>
                        </label>
                    </div>

                    {/* Day Tag */}
                    <h3 className="font-semibold">Day Tag</h3>
                    <div className="flex space-x-4">
                        <label className="flex items-center space-x-1">
                            <input type="radio" name="dayTag" value="Weekday" className="form-radio" />
                            <span>Weekday</span>
                        </label>
                        <label className="flex items-center space-x-1">
                            <input type="radio" name="dayTag" value="DayOfWeek" className="form-radio" />
                            <span>Day of Week</span>
                        </label>
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        className="bg-black text-white py-2 px-4 rounded-md mt-4 hover:bg-gray-800 transition-colors"
                        onClick={handleNext}
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
