import streamlit as st


def _faq_reply(question: str) -> str:
    q = question.lower()
    if any(k in q for k in ["water", "irrigat", "moisture"]):
        return "Check soil moisture before watering. Irrigate when the root zone is getting dry, and avoid watering saturated soil. Prefer early morning or evening to reduce evaporation."
    if any(k in q for k in ["pest", "insect", "bug"]):
        return "Inspect the underside of leaves and new growth. If pests are confirmed, remove heavily affected leaves and use an appropriate integrated pest-management treatment for your crop."
    if any(k in q for k in ["disease", "spot", "leaf", "fungus", "blight", "rot"]):
        return "Take a clear close-up photo of an affected leaf and use Disease Detection. Isolate badly affected plant material where practical and avoid spreading contaminated tools or water."
    if any(k in q for k in ["flood", "heavy rain", "waterlog"]):
        return "Keep drainage channels clear, avoid adding irrigation before heavy rain, and inspect low-lying areas after rainfall for standing water."
    if any(k in q for k in ["drought", "dry", "no rain"]):
        return "Prioritise irrigation for plants showing water stress, mulch exposed soil where practical, and monitor soil moisture regularly."
    if any(k in q for k in ["temperature", "heat", "hot", "cold"]):
        return "During heat, reduce water loss with mulch and irrigation at cooler times. During unusual cold, monitor sensitive crops for stress and protect them where practical."
    if any(k in q for k in ["camera", "cctv", "watch", "monitor"]):
        return "Use the Camera Feed to inspect the latest field snapshot. A connected device must expose the /capture endpoint."
    if any(k in q for k in ["fertiliz", "nutrient", "npk"]):
        return "Avoid fertilising based only on leaf appearance. Consider soil testing and the crop's growth stage, then follow a crop-specific nutrient recommendation."
    return "I can help with watering, pests, disease symptoms, flood/drought risk, temperature stress, camera monitoring, and fertilizer questions. Ask me about one of these topics."


def _claude_reply(question: str, history=None):
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        api_key = None
    if not api_key:
        return None
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        messages = []
        for msg in history or []:
            if msg.get("role") in {"user", "assistant"}:
                messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": question})
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            system=("You are a helpful farming assistant embedded in a smart farming dashboard. "
                    "Answer concisely and practically for a farmer using soil moisture, humidity/temperature "
                    "sensors, rainfall alerts, and a plant-disease camera model."),
            messages=messages,
        )
        return response.content[0].text if response.content else None
    except Exception as e:
        st.session_state["ai_last_error"] = str(e)
        return None


def ai_reply(question: str, history=None) -> str:
    answer = _claude_reply(question, history=history)
    return answer or _faq_reply(question)
