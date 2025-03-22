import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import gymImage from "../assets/gym.png";

function ChooseExercise() {
    const navigate = useNavigate();
    const location = useLocation();
    const [exercises, setExercises] = useState([]);
    const [selectedExercises, setSelectedExercises] = useState([]);

    // Get routine details from the Home screen
    const { routineName, focus, level, dayTag } = location.state || {};

    useEffect(() => {
        // Fetch exercises from Flask backend
        fetch("http://127.0.0.1:5000/exercises")
            .then((response) => response.json())
            .then((data) => setExercises(data))
            .catch((error) => console.error("Error fetching exercises:", error));
    }, []);

    const handleExerciseClick = (exercise) => {
        // Toggle exercise selection
        if (selectedExercises.some((e) => e.id === exercise.id)) {
            // If already selected, remove it
            setSelectedExercises(selectedExercises.filter((e) => e.id !== exercise.id));
        } else {
            // If not selected, add it
            setSelectedExercises([...selectedExercises, exercise]);
        }
    };

    const handleNext = () => {
        // Pass selected exercises and routine details to the Routine screen
        navigate("/routine", {
            state: {
                routineName,
                focus,
                level,
                dayTag,
                selectedExercises,
            },
        });
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
                            className={`w-full flex items-center justify-between 
                         px-4 py-2 border border-gray-300 rounded-md 
                         ${
                             selectedExercises.some((e) => e.id === exercise.id)
                                 ? "bg-black text-white" // Selected style
                                 : "bg-white text-black" // Default style
                         } hover:bg-gray-100 transition-colors`}
                            onClick={() => handleExerciseClick(exercise)}
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

                {/* Selected Exercises Preview */}
                <div className="w-full max-w-sm mt-4">
                    <h3 className="text-lg font-semibold mb-2">Selected Exercises</h3>
                    <div className="space-y-2">
                        {selectedExercises.map((exercise, index) => (
                            <div
                                key={index}
                                className="bg-black text-white px-4 py-2 rounded-md"
                            >
                                <span className="font-semibold">{exercise.name}</span>
                                <span className="ml-2 text-gray-300">
                                    {exercise.category_name}
                                </span>
                            </div>
                        ))}
                    </div>
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