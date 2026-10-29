import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform
 
# ---------- Configuración de la página ----------
st.set_page_config(page_title="Lulo Lab · Control MQTT", page_icon="🍊", layout="centered")
 
# ---------- Estilos (temática lulo: naranja + verde) ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&display=swap');
 
    html, body, [class*="css"] { font-family: 'Fredoka', sans-serif; }
 
    .stApp {
        background: linear-gradient(160deg, #fff4e0 0%, #ffe0b2 55%, #c8e6a0 100%);
    }
 
    .hero {
        background: linear-gradient(135deg, #ff8f1f, #f4511e);
        border-radius: 28px;
        padding: 28px 24px;
        text-align: center;
        color: #fff;
        box-shadow: 0 10px 24px rgba(244, 81, 30, 0.35);
        margin-bottom: 24px;
        border-bottom: 8px solid #6a9c2f;
    }
    .hero h1 { margin: 0; font-size: 2.4rem; font-weight: 700; color: #fff; }
    .hero p  { margin: 8px 0 0; font-size: 1.05rem; opacity: .95; }
 
    .card {
        background: #fffdf7;
        border: 3px solid #ffb74d;
        border-radius: 22px;
        padding: 14px 20px;
        margin: 22px 0 10px;
        color: #5d3a00;
        font-weight: 600;
        font-size: 1.15rem;
    }
 
    div.stButton > button {
        width: 100%;
        border-radius: 18px;
        border: none;
        padding: 0.8rem 1rem;
        font-size: 1.15rem;
        font-weight: 700;
        color: #fff;
        background: linear-gradient(135deg, #7cb342, #558b2f);
        box-shadow: 0 5px 0 #33691e;
        transition: all .1s ease;
    }
    div.stButton > button:hover { filter: brightness(1.08); color: #fff; }
    div.stButton > button:active { transform: translateY(4px); box-shadow: 0 1px 0 #33691e; }
 
    .footer { text-align: center; color: #6d4c00; font-size: .85rem; margin-top: 30px; }
    </style>
    """,
    unsafe_allow_html=True,
)
 
# ---------- Lógica MQTT (sin cambios) ----------
values = 0.0
act1 = "OFF"
 
 
def on_publish(client, userdata, result):  # create function for callback
    print("el dato ha sido publicado \n")
    pass
 
 
def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)
 
 
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("lulo")
client1.on_message = on_message
 
# ---------- Encabezado ----------
st.markdown(
    """
    <div class="hero">
        <h1>🍊 Lulo Lab</h1>
        <p>Panel de control IoT: enciende, apaga y ajusta tus dispositivos<br>
        con un par de toques, fresco como jugo de lulo.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
 
# ---------- Interruptor ON / OFF ----------
st.markdown('<div class="card">🔌 Interruptor del actuador</div>', unsafe_allow_html=True)
 
col_on, col_off = st.columns(2)
 
with col_on:
    if st.button("🟢 ENCENDER"):
        act1 = "ON"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("Sensor/lulo", message)
        st.success("¡Actuador encendido! 🍊")
 
with col_off:
    if st.button("🔴 APAGAR"):
        act1 = "OFF"
        client1 = paho.Client("GIT-HUB")
        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": act1})
        ret = client1.publish("cmqtt_s", message)
        st.warning("Actuador apagado 🌙")
 
# ---------- Control analógico ----------
st.markdown('<div class="card">🎚️ Dosificador analógico</div>', unsafe_allow_html=True)
 
values = st.slider("Selecciona el rango de valores", 0.0, 100.0)
st.write("Valor seleccionado:", values)
 
if st.button("🚀 Enviar valor analógico"):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    ret = client1.publish("cmqtt_a", message)
    st.success(f"Valor {values} enviado 🍃")
 
# ---------- Pie de página ----------
st.markdown(
    f'<div class="footer">🐍 Python {platform.python_version()} · Broker MQTT {broker}:{port}</div>',
    unsafe_allow_html=True,
)
 

