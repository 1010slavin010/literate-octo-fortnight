# KisanSense — Smart Farming Assistant

A Streamlit-based farmer operations dashboard combining environmental sensing, AI assistance, climate-risk alerts, camera monitoring, and plant-disease screening.

## Features

- Farmer-friendly Home dashboard
- Soil moisture, humidity, temperature, and light monitoring
- ESP32/Pi device API integration with demo fallback
- Flood/drought risk alerts using soil moisture and rainfall forecast
- Field camera snapshots through `/capture`
- AI farming assistant with FAQ fallback and optional Anthropic integration
- Plant disease image screening using a Keras model
- Responsive Streamlit layout and navigation

## Local setup

Use Python 3.11 for TensorFlow compatibility.

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run Home.py
```

Development login fallback: `farm2026`. For deployment, set `APP_PASSWORD` in Streamlit secrets instead.

## Device API

Set the device base URL in the Home sidebar. The device should provide `GET /data` returning JSON such as:

```json
{"soil_moisture":42.5,"humidity":61.2,"temperature":27.8,"light":70}
```

and optionally `GET /capture` returning a raw JPEG image.

## Disease model

Place the trained Keras model at `model/plant_model_v5.keras`. The application includes the model loader and 55-class PlantVillage-style label set. Binary model files must be copied separately into this path before running Disease Detection.

## Secrets

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` locally and add real keys there. Never commit real secrets.
