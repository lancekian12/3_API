import React from "react";
import gymImage from "../assets/gym.png";
import { useNavigate } from "react-router-dom";


function ChooseExercise() {
    const navigate = useNavigate();

    // Example list of exercises (could be fetched from an API or passed as props)
    const exercises = [
        { name: "Machine Bench Press", category: "Legs" },
        { name: "Machine Seated Calf Raise", category: "Lower Legs" },
        { name: "PushUp", category: "Chest" },
        { name: "Dumbbell Shoulder Shrug", category: "Back" },
        { name: "Machine Hip Abduction", category: "Upper Legs" },
        { name: "Machine Reverse Fly", category: "Shoulders" },
        // Add as many exercises as you want here
    ];

    const handleNext = () => {
        // Navigate to the Routine page (or wherever your next step is)
        navigate("/routine");
    };

    return (
        <div className="flex h-screen font-sans">
            {/* Left Section */}
            <div className="flex-1 p-8 flex flex-col justify-center items-center">
                <h1 className="text-2xl font-bold mb-2 text-center">Let’s Get Started</h1>
                <h2 className="text-lg text-gray-600 mb-8 text-center">Choose Your Exercise</h2>

                {/* Scrollable List of Exercises */}
                <div className="w-full max-w-sm h-80 overflow-y-auto space-y-2">
                    {exercises.map((exercise, index) => (
                        <button
                            key={index}
                            className="w-full flex items-center justify-between 
                         px-4 py-2 border border-gray-300 rounded-md 
                         bg-white hover:bg-gray-100 transition-colors"
                        >
                            <span className="font-semibold">{exercise.name}</span>
                            <span className="text-gray-500">{exercise.category}</span>
                        </button>
                    ))}
                </div>

                {/* Next Button */}
                <button
                    type="button"
                    onClick={handleNext}
                    className="bg-black text-white py-2 px-4 rounded-md mt-4 
                     hover:bg-gray-800 transition-colors"
                >
                    Next
                </button>
            </div>

            {/* Right Section */}
            <div className="flex-1 overflow-hidden">
                <img src={gymImage} alt="Gym" className="w-full h-full object-cover" />
            </div>
        </div>
    );
}

export default ChooseExercise;
