# Failure Risk Prediction – TPS ML Web App
This is a Machine Learning web application for predicting failure risk in the Tabular Playground Series (TPS) dataset. The app uses a trained XGBoost model to analyze product data and predict whether a product is safe or at risk of failure.

## Features

- Web-based interface for inputting product parameters
- Real-time prediction using ML model
- Dynamic results based on loading threshold (700+ forces failure)
- Backend API built with Flask
- Frontend served via Python HTTP server

## Technologies Used

- **Backend**: Python, Flask, Flask-CORS
- **Machine Learning**: XGBoost, Scikit-learn, Joblib
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML, JavaScript, CSS

## Project Structure

```
tps-ml-web-app/
├── backend/
│   ├── app.py              # Flask API server
│   ├── model.pkl           # Trained XGBoost model
│   ├── preprocessor.pkl    # Data preprocessor
│   ├── requirement.txt     # Python dependencies
│   ├── test_model.py       # Model testing script
│   └── venv/               # Virtual environment
├── frontend/
│   ├── index.html          # Main web page
│   └── script.js           # Frontend JavaScript
├── kaggle-project/
│   ├── train.csv           # Training data
│   ├── test.csv            # Test data
│   ├── sample_submission.csv
│   └── Kaggle_Analyzing_the_Tabular_Playground_Series_2022_.ipynb
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.7+
- Git (optional, for cloning)

### 1. Clone or Download the Project

Download the project files to your local machine.

### 2. Install Backend Dependencies

Navigate to the backend directory and install the required packages:

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirement.txt
```

### 3. Run the Backend Server

Start the Flask API server:

```bash
cd backend
venv\Scripts\activate
python app.py
```

The backend will run on `http://localhost:5000`

### 4. Run the Frontend Server

Open a new terminal and start the frontend server:

```bash
cd frontend
python -m http.server 8000
```

The frontend will be available at `http://localhost:8000`

### 5. Access the Application

Open your web browser and go to `http://localhost:8000` to use the application.

## Usage

1. Fill in the product parameters in the web form:
   - Product Code (e.g., A, B, C)
   - Loading (numeric value)
   - Attribute 0 and 1 (material types)
   - Measurements (0-17, numeric values)

2. Click "Predict" to get the result.

3. The app will show either "✅ Product is Safe" or "⚠️ Failure Risk Detected".

## API Endpoints

- `GET /` - Home page
- `POST /predict` - Make a prediction

### Prediction Request Format

```json
{
  "product_code": "A",
  "loading": 100.5,
  "attribute_0": "material_7",
  "attribute_1": "material_8",
  "attribute_2": 9,
  "attribute_3": 5,
  "measurement_0": 7,
  "measurement_1": 8,
  "measurement_2": 4,
  "measurement_3": 18.04,
  "measurement_4": 12.518,
  "measurement_5": 15.748,
  "measurement_6": 19.292,
  "measurement_7": 11.739,
  "measurement_8": 20.155,
  "measurement_9": 10.672,
  "measurement_10": 15.859,
  "measurement_11": 17.594,
  "measurement_12": 15.193,
  "measurement_13": 15.029,
  "measurement_14": 13.034,
  "measurement_15": 14.684,
  "measurement_16": 764.1,
  "measurement_17": 0
}
```

## Testing

To test the model directly, run the test script:

```bash
cd backend
venv\Scripts\activate
python test_model.py
```

## Notes

- The model is trained on the Tabular Playground Series 2022 data
- Loading values above 700 are automatically flagged as high risk
- Ensure both servers are running simultaneously for full functionality
- The app uses debug mode for development; disable for production

## Troubleshooting

- If you get import errors, ensure all requirements are installed
- Check that model.pkl and preprocessor.pkl files exist in the backend directory
- Make sure ports 5000 and 8000 are not in use by other applications

### 👩‍💻 Developed by  
**Mahia Momo**  
AI & Machine Learning Enthusiast  

📧 **Email:** mahiamomo12@gmail.com  
🔗 **LinkedIn:** https://www.linkedin.com/in/mahiamomo12/  
💻 **GitHub:** https://github.com/mahiamOmO