import joblib
import pandas as pd
import numpy as np

# Load model and preprocessor
model = joblib.load('model.pkl')
preprocessor = joblib.load('preprocessor.pkl')

# Test data
test_data = {
    'product_code': 'A',
    'loading': 80.1,
    'attribute_0': 'material_7',
    'attribute_1': 'material_8',
    'attribute_2': 9,
    'attribute_3': 5,
    'measurement_0': 7,
    'measurement_1': 8,
    'measurement_2': 4,
    'measurement_3': 18.04,
    'measurement_4': 12.518,
    'measurement_5': 15.748,
    'measurement_6': 19.292,
    'measurement_7': 11.739,
    'measurement_8': 20.155,
    'measurement_9': 10.672,
    'measurement_10': 15.859,
    'measurement_11': 17.594,
    'measurement_12': 15.193,
    'measurement_13': 15.029,
    'measurement_14': np.nan,
    'measurement_15': 13.034,
    'measurement_16': 14.684,
    'measurement_17': 764.1
}

query_df = pd.DataFrame([test_data])

# Fill missing columns
expected_cols = preprocessor.feature_names_in_
for col in expected_cols:
    if col not in query_df.columns:
        if col in ['product_code', 'attribute_0', 'attribute_1']:
            query_df[col] = ''
        else:
            query_df[col] = 0.0

# Handle dtypes
for col in query_df.columns:
    if col in ['product_code', 'attribute_0', 'attribute_1']:
        query_df[col] = query_df[col].astype(str)
    else:
        query_df[col] = pd.to_numeric(query_df[col], errors='coerce')
        query_df[col] = query_df[col].fillna(0.0)
        query_df[col] = query_df[col].replace([np.inf, -np.inf], 0.0)
        query_df[col] = query_df[col].astype('float64')

query_df = query_df[expected_cols]

processed_data = preprocessor.transform(query_df)
prediction = model.predict(processed_data)

print("Prediction:", prediction)
print("Result:", "Failure" if prediction[0] == 1 else "Safe")