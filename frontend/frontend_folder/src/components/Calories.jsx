import React, { useState } from "react";
import appleIcon from "../assets/apple.png";
import burgerIcon from "../assets/burger.png";
import saladIcon from "../assets/salad.png";

// Dummy data for nutritional values
const FOOD_DATA = {
    Almonds: { calories: 164, fat: "14g", carbs: "6g" },
    Apples: { calories: 95, fat: "0.3g", carbs: "25g" },
    Avocados: { calories: 234, fat: "21g", carbs: "12g" },
    Bananas: { calories: 105, fat: "0.4g", carbs: "27g" },
    "Brewed Tea": { calories: 2, fat: "0g", carbs: "0.4g" },
    Broccoli: { calories: 55, fat: "0.6g", carbs: "11g" },
    "Brown Rice": { calories: 216, fat: "1.8g", carbs: "45g" },
    Carrots: { calories: 25, fat: "0.1g", carbs: "6g" },
    Celery: { calories: 16, fat: "0.2g", carbs: "3g" },
    Cucumber: { calories: 16, fat: "0.1g", carbs: "3.8g" },
    Eggs: { calories: 72, fat: "4.8g", carbs: "0.4g" },
};

function Calories() {
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedFood, setSelectedFood] = useState("");
    const [amount, setAmount] = useState(1);

    // For popular foods buttons
    const popularFoods = Object.keys(FOOD_DATA);

    // Update the search text as user types
    const handleSearchInput = (e) => {
        setSearchTerm(e.target.value);
    };

    // When user clicks on a popular food
    const handleSelectFood = (food) => {
        setSelectedFood(food);
        setSearchTerm(food);
    };

    // Search button: try to match user input to a known food
    const handleSearchFood = () => {
        const normalizedTerm = searchTerm.trim().toLowerCase();

        // Attempt a partial match in FOOD_DATA keys
        const foundKey = Object.keys(FOOD_DATA).find((food) =>
            food.toLowerCase().includes(normalizedTerm)
        );

        if (foundKey) {
            // If found, set that as the selected food
            setSelectedFood(foundKey);
            setSearchTerm(foundKey); // show the matched name in the input
        } else {
            // If not found, clear the selectedFood (use placeholder data)
            setSelectedFood("");
        }
    };

    // Calculate: show an alert with the data * amount
    const handleCalculate = () => {
        const data = FOOD_DATA[selectedFood] || { calories: 100, fat: "10g", carbs: "10g" };
        const totalCalories = data.calories * amount;
        const totalFat = multiplyMacros(data.fat, amount);
        const totalCarbs = multiplyMacros(data.carbs, amount);

        alert(
            `For ${amount} serving(s) of ${selectedFood || "Unknown Food"}:
       ${totalCalories} Calories, ${totalFat} Fat, ${totalCarbs} Carbs.`
        );
    };

    // Helper to multiply numeric portion of a macro by "amount"
    const multiplyMacros = (macroString, multiplier) => {
        const parsed = parseFloat(macroString);
        return !isNaN(parsed) ? parsed * multiplier + "g" : macroString;
    };

    // Clear everything
    const handleClear = () => {
        setSearchTerm("");
        setSelectedFood("");
        setAmount(1);
    };

    // For the "You’ve Consumed" section
    const currentFoodData = FOOD_DATA[selectedFood] || { calories: 100, fat: "10g", carbs: "10g" };
    const displayCalories = currentFoodData.calories * amount;
    const displayFat = multiplyMacros(currentFoodData.fat, amount);
    const displayCarbs = multiplyMacros(currentFoodData.carbs, amount);

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
                    placeholder="e.g., apples or kiwi"
                    className="w-full md:w-2/3 border border-gray-300 p-2 rounded"
                />
                <button
                    onClick={handleSearchFood}
                    className="bg-black text-white py-2 px-4 rounded hover:bg-gray-800 transition-colors"
                >
                    Search
                </button>
            </div>

            {/* 
        MAIN MENU 1 (Popular Foods) 
        Only shown if there's no selected food
      */}
            {!selectedFood && (
                <div>
                    <p className="text-gray-500 text-center mb-4">Popular Foods</p>
                    <div className="flex flex-wrap gap-2 justify-center mb-8">
                        {popularFoods.map((food, index) => (
                            <button
                                key={index}
                                onClick={() => handleSelectFood(food)}
                                className="border border-gray-300 px-3 py-1 rounded 
                           hover:bg-gray-100 transition-colors"
                            >
                                {food}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* 
        MAIN MENU 2 (Selected Food) 
        Displayed when a food is selected
      */}
            {selectedFood && (
                <div className="text-center">
                    <div className="mb-4">
                        <p className="font-semibold text-gray-700">Your Food: {selectedFood}</p>
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
                                <p className="font-bold">{displayFat}</p>
                            </div>
                            <div>
                                <p className="text-gray-700">Carbs</p>
                                <p className="font-bold">{displayCarbs}</p>
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
