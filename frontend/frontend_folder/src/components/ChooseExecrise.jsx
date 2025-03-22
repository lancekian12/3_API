import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import gymImage from "../assets/gym.png";

function ChooseExercise() {
    const navigate = useNavigate();
    const [exercises, setExercises] = useState([]);

    useEffect(() => {
        // Fetch exercises from Flask backend
        fetch("http://127.0.0.1:5000/exercises")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch exercises");
                }
                return response.json();
            })
            .then((data) => {
                // Ensure data is an array before setting it
                if (Array.isArray(data)) {
                    setExercises(data);
                } else {
                    console.error("Expected an array but got:", data);
                    setExercises([]); // Fallback to an empty array
                }
            })
            .catch((error) => {
                console.error("Error fetching exercises:", error);
                setExercises([]); // Fallback to an empty array
            });
    }, []);

    const handleNext = () => {
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
                            <div>
                                <span className="font-semibold">{exercise.name}</span>
                                <div className="text-gray-500">
                                    <span>{exercise.category_name}</span>
                                    
                                </div>
                            </div>
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