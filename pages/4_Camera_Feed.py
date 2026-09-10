import time
import streamlit as st

from utils.esp_client import get_camera_snapshot, get_device_base_url
from utils.theme import inject_theme, topnav
from utils.auth import logout_button

inject_theme()
topnav("camera")

st.title("📷 Camera Feed")
st.caption("View the latest field-camera snapshot from your connected device.")

with st.sidebar:
    logout_button()

refresh = st.button("🔄 Refresh snapshot", use_container_width=True)
auto = st.checkbox("Auto-refresh every 5s")

if not get_device_base_url():
    st.info("Connect an ESP32/Pi camera using the device URL in the Home sidebar.")
else:
    if refresh or "camera_snapshot" not in st.session_state:
        st.session_state["camera_snapshot"] = get_camera_snapshot()

    snapshot = st.session_state.get("camera_snapshot")
    if snapshot:
        st.image(snapshot, caption="Latest field snapshot", use_container_width=True)
    else:
        st.warning("No camera snapshot received. Check the device URL and camera endpoint.")

if auto:
    time.sleep(5)
    st.rerun()
