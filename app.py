from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

app = Flask(__name__)

# --------------------------
# Always retrain fresh model
# --------------------------
def load_and_train():
    df = pd.read_csv('crop_prediction.csv')

    # Encode categorical variables
    season_encoder = LabelEncoder()
    label_encoder = LabelEncoder()

    df['season_encoded'] = season_encoder.fit_transform(df['season'])
    df['label_encoded'] = label_encoder.fit_transform(df['label'])

    # Features and target
    X = df[['temperature', 'humidity', 'ph', 'water availability', 'season_encoded']]
    y = df['label_encoded']

    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return season_encoder, label_encoder, model

# ⚡ Train model fresh on every run
season_encoder, label_encoder, model = load_and_train()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        water_availability = float(data['water_availability'])
        season = data['season']

        # Encode season
        season_encoded = season_encoder.transform([season])[0]

        # Features
        features = np.array([[temperature, humidity, ph, water_availability, season_encoded]])

        # Prediction
        prediction_encoded = model.predict(features)[0]
        confidence = np.max(model.predict_proba(features)) * 100

        # Decode
        crop = label_encoder.inverse_transform([prediction_encoded])[0]

        return jsonify({
            'success': True,
            'crop': crop,
            'confidence': round(confidence, 2)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/season_info/<season>')
def season_info(season):
    info = {
        'rainy': 'Rainy season typically has high rainfall, ideal for crops like rice, maize, and pulses.',
        'winter': 'Winter season is cooler, suitable for crops like chickpeas, lentils, and other Rabi crops.',
        'summer': 'Summer season is hot and dry, ideal for crops like watermelon, muskmelon, and cotton.',
        'spring': 'Spring season has moderate temperatures, good for kidney beans and balanced-climate crops.'
    }
    return jsonify({
        'season': season,
        'info': info.get(season, 'No information available for this season.')
    })

if __name__ == '__main__':
    app.run(debug=True)
