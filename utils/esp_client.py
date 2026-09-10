import random
import time
from io import BytesIO

import requests
import streamlit as st

DATA_ENDPOINT = "/data"
CAMERA_ENDPOINT = "/capture"
TIMEOUT_SECONDS = 4


def get_device_base_url() -> str:
    return st.session_state.get("esp_base_url", "").strip().rstrip("/")


def _demo_sensor_reading() -> dict:
    return {
        "soil_moisture": round(random.uniform(15, 70), 1),
        "humidity": round(random.uniform(40, 85), 1),
        "temperature": round(random.uniform(22, 35), 1),
        "light": round(random.uniform(10, 95), 1),
        "timestamp": time.strftime("%H:%M:%S"),
        "source": "demo",
    }


def get_sensor_data() -> dict:
    base_url = get_device_base_url()
    if not base_url:
        return _demo_sensor_reading()
    try:
        resp = requests.get(f"{base_url}{DATA_ENDPOINT}", timeout=TIMEOUT_SECONDS)
        resp.raise_for_status()
        payload = resp.json()
        return {
            "soil_moisture": payload.get("soil_moisture"),
            "humidity": payload.get("humidity"),
            "temperature": payload.get("temperature"),
            "light": payload.get("light"),
            "timestamp": time.strftime("%H:%M:%S"),
            "source": "device",
        }
    except Exception as e:
        st.session_state["esp_last_error"] = str(e)
        return _demo_sensor_reading()


def get_camera_snapshot():
    base_url = get_device_base_url()
    if not base_url:
        return None
    try:
        resp = requests.get(f"{base_url}{CAMERA_ENDPOINT}", timeout=TIMEOUT_SECONDS)
        resp.raise_for_status()
        return BytesIO(resp.content)
    except Exception as e:
        st.session_state["esp_last_error"] = str(e)
        return None
