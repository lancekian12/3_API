import React, { useState } from "react";

function Calories() {
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedFood, setSelectedFood] = useState("");
    const [amount, setAmount] = useState(1);

    const popularFoods = [
        "Almonds",
        "Apples",
        "Avocados",
        "Bananas",
        "Brewed Tea",
        "Broccoli",
        "Brown Rice",
        "Carrots",
        "Celery",
        "Cucumber",
        "Eggs",
        // ... add more
    ];

    const handleSearch = (e) => {
        setSearchTerm(e.target.value);
    };

    const handleSelectFood = (food) => {
        setSelectedFood(food);
        setSearchTerm(food);
    };

    const handleCalculate = () => {
        // You’d do an API call or formula to find the actual macros
        // Here we’re just mocking some data
        alert(
            `For ${amount} serving(s) of ${selectedFood}, 
      approximate: 100 Calories, 10g Fat, 10g Carbs.`
        );
    };

    return (
        <div className="p-8 text-center">
            <h1 className="text-2xl font-bold mb-4">Calories Checker</h1>

            {/* Search Bar */}
            <div className="max-w-md mx-auto">
                <input
                    type="text"
                    value={searchTerm}
                    onChange={handleSearch}
                    placeholder="e.g., apples or kiwi"
                    className="w-full border border-gray-300 p-2 rounded mb-4"
                />

                {/* Popular Foods */}
                <div className="flex flex-wrap gap-2 justify-center mb-6">
                    {popularFoods.map((food, index) => (
                        <button
                            key={index}
                            onClick={() => handleSelectFood(food)}
                            className="border border-gray-300 px-2 py-1 rounded hover:bg-gray-100"
                        >
                            {food}
                        </button>
                    ))}
                </div>

                {/* If user selected a food */}
                {selectedFood && (
                    <div className="mb-4">
                        <div className="text-left mb-2">
                            <strong>Your Food:</strong> {selectedFood}
                        </div>
                        <label className="block text-left mb-1 font-semibold">Amount (servings):</label>
                        <input
                            type="number"
                            min="1"
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                            className="border border-gray-300 p-1 rounded w-16"
                        />
                    </div>
                )}

                {/* Calculate Button */}
                <button
                    onClick={handleCalculate}
                    className="bg-black text-white py-2 px-4 rounded mt-2 hover:bg-gray-800 transition-colors"
                >
                    Calculate
                </button>
            </div>
        </div>
    );
}

export default Calories;
