import streamlit as st
import requests

st.set_page_config(page_title="ESP32 Sensor Monitor", layout="centered")
st.title("🌡️ ESP32 Temperature Monitor with GPT-2 AI Description")

API_URL = "http://192.168.170.240:5000/latest"

if st.button(" Ambil Data Terbaru"):
    try:
        res = requests.get(API_URL)

        if res.status_code == 204:
            st.warning("Belum ada data dari ESP32...")
        elif res.status_code == 200:
            data = res.json()
            temp = data.get("temperature")
            desc = data.get("description")

            st.subheader("📡 Live Sensor Reading")
            st.metric(label="Temperature (°C)", value=f"{temp}°C" if temp else "N/A")
            st.subheader("🧠 AI Description")
            st.write(desc or "Waiting for data...")

        else:
            st.error(f"Server Error: {res.status_code}")

    except Exception as e:
        st.error(f"Error: {e}")
