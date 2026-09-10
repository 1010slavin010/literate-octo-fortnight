import hmac

import streamlit as st

DEMO_FALLBACK_PASSWORD = "farm2026"


def _configured_password() -> str:
    try:
        return str(st.secrets.get("APP_PASSWORD", DEMO_FALLBACK_PASSWORD))
    except Exception:
        return DEMO_FALLBACK_PASSWORD


def require_login() -> None:
    if st.session_state.get("authenticated"):
        return

    st.title("🌾 AgroSentry")
    st.subheader("Farm Operations Login")
    password = st.text_input("Password", type="password")
    if st.button("Sign in", type="primary"):
        if hmac.compare_digest(password, _configured_password()):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.caption("Set APP_PASSWORD in Streamlit secrets for deployment. The fallback password is for development only.")
    st.stop()


def logout_button() -> None:
    if st.session_state.get("authenticated") and st.button("Log out", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()
