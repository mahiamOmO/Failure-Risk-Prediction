from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import math

app = Flask(__name__)
CORS(app)

# Load model and preprocessor
try:
    model = joblib.load('model.pkl')
    preprocessor = joblib.load('preprocessor.pkl')
    print("✅ Model and Preprocessor loaded!")
except Exception as e:
    print(f"❌ Loading Error: {e}")

def safe_convert_to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

@app.route('/')
def home():
    return "Backend is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Incoming data:", data)  # 🔍 Debug
        print("Received data types:", {k: type(v).__name__ for k, v in data.items()})  # Add this

        # Convert only numeric fields to float, keep strings for categorical
        processed_data = {}
        for key, value in data.items():
            if key in ['loading', 'measurement_0', 'measurement_1', 'measurement_2']:
                processed_data[key] = safe_convert_to_float(value)
            else:
                # Keep categorical fields as strings
                processed_data[key] = str(value) if value is not None else ''

        print("Processed data:", processed_data)  # 🔍 Debug

        query_df = pd.DataFrame([processed_data])

        # Make sure all expected columns exist
        expected_cols = preprocessor.feature_names_in_
        for col in expected_cols:
            if col not in query_df.columns:
                # For categorical columns, use empty string, for numeric use 0.0
                if col in ['product_code', 'attribute_0', 'attribute_1']:
                    query_df[col] = ''
                else:
                    query_df[col] = 0.0
        
        # Handle data types: keep strings for categorical, convert to float for numeric
        for col in query_df.columns:
            if col in ['product_code', 'attribute_0', 'attribute_1']:
                # Keep as string
                query_df[col] = query_df[col].astype(str)
            else:
                # Convert to numeric
                query_df[col] = pd.to_numeric(query_df[col], errors='coerce')
                query_df[col] = query_df[col].fillna(0.0)
                query_df[col] = query_df[col].replace([np.inf, -np.inf], 0.0)
                query_df[col] = query_df[col].astype('float64')

        # Reorder columns as model expects
        query_df = query_df[expected_cols]
        
        print("Final DataFrame dtypes:", query_df.dtypes)  # 🔍 Debug
        print("Final DataFrame values:\n", query_df)  # 🔍 Debug

        # Transform & predict
        processed_data = preprocessor.transform(query_df)
        prediction = model.predict(processed_data)
        
        # Dynamic result: Safety threshold
        if query_df['loading'].iloc[0] > 700:
            final_result = 1  # Failure
        else:
            final_result = int(prediction[0])  # Model's decision
        
        print("Prediction:", prediction, "Final Result:", final_result)  # 🔍 Debug

        result_text = "⚠️ Failure Risk Detected" if final_result == 1 else "✅ Product is Safe"

        return jsonify({
            'prediction': result_text,
            'status': final_result,
            'code': final_result
        })

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Prediction Error: {error_details}")  # 🔍 Debug
        return jsonify({'error': str(e), 'details': error_details}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
