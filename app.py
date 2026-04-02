from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os

app = Flask(__name__)

# --------------------------
# Load pre-trained model
# --------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
season_encoder = joblib.load(os.path.join(BASE_DIR, "season_encoder.pkl"))
label_encoder = joblib.load(os.path.join(BASE_DIR, "label_encoder.pkl"))

# --------------------------
# Routes
# --------------------------
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

        # Prepare features
        features = np.array([[temperature, humidity, ph, water_availability, season_encoded]])

        # Prediction
        prediction_encoded = model.predict(features)[0]
        confidence = np.max(model.predict_proba(features)) * 100

        # Decode crop name
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


# --------------------------
# Main (Render compatible)
# --------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
