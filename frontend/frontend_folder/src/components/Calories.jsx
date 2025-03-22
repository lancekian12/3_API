import React, { useState } from "react";
import appleIcon from "../assets/apple.png";
import burgerIcon from "../assets/burger.png";
import saladIcon from "../assets/salad.png";

function Calories() {
    const [searchTerm, setSearchTerm] = useState("");
    const [foodData, setFoodData] = useState(null);  // Stores { name, calories, fat, carbs }
    const [amount, setAmount] = useState(1);
    const [error, setError] = useState("");

    // Expanded list of popular foods (queries)
    const popularFoods = [
        "1 apple",
        "2 eggs",
        "1 banana",
        "100g broccoli",
        "1 cup rice",
        "1 slice pizza",
        "1 cup coffee",
        "1 burger",
        "1 cup oatmeal",
        "1 slice cheese",
        "1 cup milk",
        "1 cup pasta",
        "100g salmon",
        "1 chocolate bar"
    ];

    // Update the search text as user types
    const handleSearchInput = (e) => {
        setSearchTerm(e.target.value);
    };

    // When user clicks a popular food button
    const handleSelectFood = (foodQuery) => {
        setSearchTerm(foodQuery);
        setFoodData(null);
        setError("");
    };

    // On "Search", POST to /calories with { query: searchTerm }
    const handleSearchFood = async () => {
        setError("");
        setFoodData(null);

        if (!searchTerm.trim()) {
            setError("Please enter a food description (e.g. '1 apple' or '2 eggs').");
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/calories", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: searchTerm }),
            });

            if (!response.ok) {
                // e.g. 404, 400, etc.
                const errData = await response.json();
                throw new Error(errData.error || errData.message || `Error: ${response.status}`);
            }

            const data = await response.json();
            // data should look like: { "foods": [ { "food_name": ..., "nf_calories": ..., etc. } ] }

            if (!data.foods || data.foods.length === 0) {
                throw new Error("No foods found in the response.");
            }

            // We'll just use the first item from the array
            const item = data.foods[0];
            // Convert it to our own structure
            const parsed = {
                name: item.food_name,
                calories: item.nf_calories,               // e.g. 143.04
                fat: item.nf_total_fat,                   // e.g. 9.53
                carbs: item.nf_total_carbohydrate,        // e.g. 1.12
            };

            setFoodData(parsed);
            setError("");
        } catch (err) {
            setError(err.message);
        }
    };

    // "Calculate" button: multiply the macros by 'amount'
    const handleCalculate = () => {
        if (!foodData) return;

        const totalCalories = (foodData.calories * amount).toFixed(2);
        const totalFat = (parseFloat(foodData.fat) * amount || 0).toFixed(2);
        const totalCarbs = (parseFloat(foodData.carbs) * amount || 0).toFixed(2);

        alert(
            `For ${amount} serving(s) of ${foodData.name}:\n` +
            `${totalCalories} Calories, ${totalFat}g Fat, ${totalCarbs}g Carbs.`
        );
    };

    // Clear everything
    const handleClear = () => {
        setSearchTerm("");
        setFoodData(null);
        setAmount(1);
        setError("");
    };

    // If we have data, compute displayed macros
    let displayCalories = 0;
    let displayFat = "0";
    let displayCarbs = "0";

    if (foodData) {
        displayCalories = (foodData.calories * amount).toFixed(2);
        displayFat = (parseFloat(foodData.fat) * amount || 0).toFixed(2);
        displayCarbs = (parseFloat(foodData.carbs) * amount || 0).toFixed(2);
    }

    return (
        <div className="p-8 max-w-3xl mx-auto">
            {/* Title */}
            <h1 className="text-2xl font-bold mb-4 text-center">Calories Checker</h1>

            {/* Icons (Apple, Burger, Salad) */}
            <div className="flex justify-center items-center space-x-8 mb-8">
                <img src={appleIcon} alt="Apple" className="w-10 h-10" />
                <img src={burgerIcon} alt="Burger" className="w-10 h-10" />
                <img src={saladIcon} alt="Salad" className="w-10 h-10" />
            </div>

            {/* Search Bar + Search Button */}
            <div className="flex flex-col items-center md:flex-row md:justify-center mb-6 space-y-2 md:space-y-0 md:space-x-2">
                <input
                    type="text"
                    value={searchTerm}
                    onChange={handleSearchInput}
                    placeholder='e.g., "1 apple" or "2 eggs"'
                    className="w-full md:w-2/3 border border-gray-300 p-2 rounded"
                />
                <button
                    onClick={handleSearchFood}
                    className="bg-black text-white py-2 px-4 rounded hover:bg-gray-800 transition-colors"
                >
                    Search
                </button>
            </div>

            {/* Show error if any */}
            {error && <div className="text-center text-red-500 mb-4">{error}</div>}

            {/* If there's no foodData and no error, show popular foods */}
            {!foodData && !error && (
                <div>
                    <p className="text-gray-500 text-center mb-4">Popular Foods</p>
                    <div className="flex flex-wrap gap-2 justify-center mb-8">
                        {popularFoods.map((food, index) => (
                            <button
                                key={index}
                                onClick={() => handleSelectFood(food)}
                                className="border border-gray-300 px-3 py-1 rounded hover:bg-gray-100 transition-colors"
                            >
                                {food}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* If we have data, show the macros */}
            {foodData && (
                <div className="text-center">
                    <div className="mb-4">
                        <p className="font-semibold text-gray-700">Your Food: {foodData.name}</p>
                        <label className="block font-semibold my-2">Amount (servings):</label>
                        <input
                            type="number"
                            min="1"
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                            className="border border-gray-300 p-1 rounded w-16"
                        />
                    </div>

                    {/* "You've consumed" area */}
                    <div className="border-t border-gray-300 my-4 pt-4">
                        <p className="mb-2 font-semibold">You’ve Consumed</p>
                        <div className="flex justify-center space-x-8 mb-4">
                            <div>
                                <p className="text-gray-700">Calories</p>
                                <p className="font-bold">{displayCalories}</p>
                            </div>
                            <div>
                                <p className="text-gray-700">Fat</p>
                                <p className="font-bold">{displayFat}g</p>
                            </div>
                            <div>
                                <p className="text-gray-700">Carbs</p>
                                <p className="font-bold">{displayCarbs}g</p>
                            </div>
                        </div>
                    </div>

                    {/* Buttons: Calculate & Clear */}
                    <div className="flex space-x-4 justify-center">
                        <button
                            onClick={handleCalculate}
                            className="bg-black text-white py-2 px-4 rounded hover:bg-gray-800 transition-colors"
                        >
                            Calculate
                        </button>
                        <button
                            onClick={handleClear}
                            className="border border-gray-400 text-gray-700 py-2 px-4 rounded hover:bg-gray-100 transition-colors"
                        >
                            Clear
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Calories;
