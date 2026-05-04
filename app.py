import streamlit as st
import requests
import pandas as pd
import time

st.title("BTC Kalshi Signal Bot")

target = st.number_input("Kalshi target price", value=95000.0)
refresh = st.slider("Refresh (seconds)", 5, 60, 10)

def get_btc():
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    return float(requests.get(url).json()["data"]["amount"])

if "prices" not in st.session_state:
    st.session_state.prices = []

placeholder = st.empty()

while True:
    price = get_btc()
    st.session_state.prices.append(price)

    if len(st.session_state.prices) > 20:
        st.session_state.prices.pop(0)

    if len(st.session_state.prices) >= 5:
        trend = st.session_state.prices[-1] - st.session_state.prices[-5]
    else:
        trend = 0

    if price > target and trend > 0:
        signal = "UP"
    elif price < target and trend < 0:
        signal = "DOWN"
    else:
        signal = "SKIP"

    with placeholder.container():
        st.metric("BTC Price", price)
        st.metric("Target", target)

        if signal == "UP":
            st.success("UP")
        elif signal == "DOWN":
            st.error("DOWN")
        else:
            st.warning("SKIP")

        st.line_chart(st.session_state.prices)

    time.sleep(refresh)
