document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const resultDiv = document.getElementById('result');
    const submitButton = e.target.querySelector('button[type="submit"]');
    resultDiv.textContent = "⏳ Processing...";
    resultDiv.style.color = "blue";
    submitButton.disabled = true;
    submitButton.textContent = "Processing...";

    const productCodeMap = { "A": 0, "B": 1, "C": 2, "D": 3, "E": 4 };

    const attributeMap = {
        material_5: 0,
        material_6: 1,
        material_7: 2,
        material_8: 3
    };

    // Get and validate input values with proper type conversion
    const loadingVal = document.getElementById('loading').value.trim();
    const measurement0Val = document.getElementById('measurement_0').value.trim();
    const measurement1Val = document.getElementById('measurement_1').value.trim();
    const measurement2Val = document.getElementById('measurement_2').value.trim();

    // Helper function to safely convert to number
    const safeParseFloat = (val) => {
        const parsed = parseFloat(val);
        return isNaN(parsed) ? 0.0 : parsed;
    };

    const safeParseInt = (val) => {
        const parsed = parseInt(val, 10);
        return isNaN(parsed) ? 0 : parsed;
    };

    const formData = {
        loading: parseFloat(document.getElementById('loading').value),
        product_code: document.getElementById('product_code').value, // এটি String থাকবে
        attribute_0: document.getElementById('attribute_0').value,   // এটি String থাকবে
        attribute_1: document.getElementById('attribute_1').value,   // এটি String থাকবে
        measurement_0: parseFloat(document.getElementById('measurement_0').value),
        measurement_1: parseFloat(document.getElementById('measurement_1').value),
        measurement_2: parseFloat(document.getElementById('measurement_2').value)
    };

    console.log("Sending data:", formData); // Debug log

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Backend error occurred!");
        }

        if (result.prediction) {
            resultDiv.textContent = result.prediction;
            resultDiv.style.color = result.status === 1 ? "red" : "green";
            resultDiv.style.fontWeight = "bold";
            resultDiv.scrollIntoView({ behavior: "smooth" });
        } else {
            throw new Error("Invalid response from server");
        }
    } catch (error) {
        resultDiv.textContent = "❌ " + error.message;
        resultDiv.style.color = "red";
        console.error("Error details:", error);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Check for Failure Risk";
    }
});
