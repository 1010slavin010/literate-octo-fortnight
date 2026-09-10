from pathlib import Path

import numpy as np
from PIL import Image
import streamlit as st

from utils.theme import inject_theme, topnav
from utils.auth import logout_button

inject_theme()
topnav("disease")

st.title("🔬 AI Disease Detection")
st.caption("Upload a crop-leaf image or use your camera to screen for plant disease.")

with st.sidebar:
    logout_button()

MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "plant_model_v5.keras"

CLASS_NAMES = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy", "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
    "Orange___Citrus_Canker", "Orange___Haunglongbing_(Citrus_greening)", "Orange___Multiple_Diseases",
    "Orange___Nutrient_Deficiency", "Orange___healthy", "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight", "Potato___Late_blight",
    "Potato___healthy", "Raspberry___healthy", "Soybean___Bacterial_Pustule", "Soybean___Brown_Spot",
    "Soybean___Crestamento", "Soybean___Ferrugen", "Soybean___Frogeye_Leaf_Spot", "Soybean___Mosaic_Virus",
    "Soybean___Powdery_Mildew", "Soybean___Rust", "Soybean___Septoria", "Soybean___Southern_Blight",
    "Soybean___Sudden_Death_Syndrome", "Soybean___Target_Leaf_Spot", "Soybean___Yellow_Mosaic",
    "Soybean___healthy", "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy",
]

@st.cache_resource
def load_model():
    try:
        import tensorflow as tf
        return tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        st.session_state["model_load_error"] = str(e)
        return None

@st.cache_data
def predict_image(image_bytes):
    model = load_model()
    if model is None:
        return None, 0.0
    image = Image.open(image_bytes).convert("RGB").resize((224, 224))
    arr = np.asarray(image, dtype=np.float32) / 255.0
    pred = model.predict(np.expand_dims(arr, axis=0), verbose=0)
    index = int(np.argmax(pred[0]))
    return CLASS_NAMES[index] if index < len(CLASS_NAMES) else f"Class {index}", float(np.max(pred[0]))

upload_tab, camera_tab = st.tabs(["📁 Upload image", "📸 Camera"])
with upload_tab:
    uploaded = st.file_uploader("Choose a leaf image", type=["jpg", "jpeg", "png", "webp"])
with camera_tab:
    camera = st.camera_input("Take a leaf photo")

image_source = uploaded or camera
if image_source:
    st.image(image_source, caption="Selected image", use_container_width=True)
    if st.button("🔎 Detect Disease", type="primary", use_container_width=True):
        with st.spinner("Analysing leaf..."):
            label, confidence = predict_image(image_source)
        if label is None:
            st.error("The disease model could not be loaded.")
            if st.session_state.get("model_load_error"):
                st.code(st.session_state["model_load_error"])
        else:
            readable = label.replace("___", " — ").replace("_", " ")
            st.success(f"Prediction: **{readable}**")
            st.metric("Confidence", f"{confidence * 100:.1f}%")
            if "healthy" in label.lower():
                st.info("The model classifies this leaf as healthy. Continue normal monitoring.")
            else:
                st.warning("Treat this as an AI screening result, not a laboratory diagnosis. Inspect the crop and consider local agricultural guidance before treatment.")
else:
    st.info("Upload a clear leaf image or take a camera photo to begin.")
