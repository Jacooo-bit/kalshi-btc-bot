import streamlit as st
import requests
import pandas as pd
import time
import datetime

st.title("BTC Kalshi Signal Bot")

target = st.number_input("Kalshi target price", value=95000.0)
refresh = st.slider("Refresh (seconds)", 5, 60, 10)
end_time = st.time_input("Market End Time")

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

    # NEW SMART LOGIC
    distance = price - target
    percent = (distance / target) * 100

    if price > target and trend > 0:
        if percent > 0.15:
            signal = "STRONG UP"
        else:
            signal = "WEAK UP"

    elif price < target and trend < 0:
        if percent < -0.15:
            signal = "STRONG DOWN"
        else:
            signal = "WEAK DOWN"
    else:
        signal = "SKIP"

    with placeholder.container():
        st.metric("BTC Price", f"{price}")
        st.metric("Target", f"{target}")
        st.write(f"Distance %: {percent:.3f}%")

        now = datetime.datetime.now().time()
        st.write(f"Current time: {now}")
        st.write(f"End time: {end_time}")

        if "STRONG UP" in signal:
            st.success(signal)
        elif "STRONG DOWN" in signal:
            st.error(signal)
        elif "WEAK" in signal:
            st.warning(signal)
        else:
            st.warning("SKIP")

        if "STRONG" in signal:
            st.success("GOOD ENTRY ZONE")
        else:
            st.warning("WAIT / RISKY")

        st.line_chart(st.session_state.prices)

    time.sleep(refresh)
