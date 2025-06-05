import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Function to simulate smoking scenario
def simulate_smoking_scenario(trader_id, instrument, large_order_multiplier, num_cycles, cancel_threshold, trade_delay, intensity, trade_inclusion_flag, near_side_threshold, far_side_threshold, lookup_window, depth_level):
    events = []
    alerts = []
    
    for cycle in range(num_cycles):
        for _ in range(intensity):
            # Generate timestamps
            order_time = datetime.now()
            cancel_time = order_time + timedelta(seconds=random.randint(1, cancel_threshold))
            trade_time = order_time + timedelta(seconds=random.randint(1, trade_delay))
            
            # Generate large visible order
            large_order_size = random.randint(1000, 5000) * large_order_multiplier
            events.append({
                'timestamp': order_time,
                'trader_id': trader_id,
                'instrument': instrument,
                'order_size': large_order_size,
                'order_type': 'visible',
                'action': 'place'
            })
            
            # Cancel large visible order
            events.append({
                'timestamp': cancel_time,
                'trader_id': trader_id,
                'instrument': instrument,
                'order_size': large_order_size,
                'order_type': 'visible',
                'action': 'cancel'
            })
            
            # Generate smaller genuine trade
            if trade_inclusion_flag:
                trade_size = random.randint(100, 500)
                events.append({
                    'timestamp': trade_time,
                    'trader_id': trader_id,
                    'instrument': instrument,
                    'order_size': trade_size,
                    'order_type': 'genuine',
                    'action': 'execute'
                })
            
            # Check for alerts
            if large_order_size > near_side_threshold:
                far_side_orders = [event for event in events if event['order_type'] == 'visible' and event['action'] == 'place' and event['timestamp'] >= order_time - timedelta(seconds=lookup_window)]
                for far_order in far_side_orders:
                    if far_order['order_size'] <= far_side_threshold:
                        alerts.append({
                            'timestamp': order_time,
                            'trader_id': trader_id,
                            'instrument': instrument,
                            'order_size': large_order_size,
                            'order_type': 'visible',
                            'action': 'alert'
                        })
    
    return pd.DataFrame(events), pd.DataFrame(alerts)

# Streamlit UI
st.title("Modular Test Data Simulator - Smoking Scenario")

# UI Parameters
trader_id = st.text_input("Trader ID", "Trader123")
instrument = st.text_input("Instrument", "AAPL")
large_order_multiplier = st.number_input("Large Order Size Multiplier", 10)
num_cycles = st.number_input("Number of Smoking Cycles", 5)
cancel_threshold = st.number_input("Cancellation Time Threshold (seconds)", 10)
trade_delay = st.number_input("Trade Execution Delay (seconds)", 5)
intensity = st.number_input("Scenario Intensity", 3)
trade_inclusion_flag = st.checkbox("Include Trades", True)
near_side_threshold = st.number_input("Near Side Notional Threshold (GBP)", 5000000)
far_side_threshold = st.number_input("Far Side Notional Threshold (GBP)", 5000000)
lookup_window = st.number_input("Open Order Lookup Window (seconds)", 45)
depth_level = st.number_input("Price Comparison Depth Level", 1)

# Simulate scenario
if st.button("Simulate Smoking Scenario"):
    events_df, alerts_df = simulate_smoking_scenario(trader_id, instrument, large_order_multiplier, num_cycles, cancel_threshold, trade_delay, intensity, trade_inclusion_flag, near_side_threshold, far_side_threshold, lookup_window, depth_level)
    
    st.subheader("Simulated Order Data")
    st.dataframe(events_df)
    
    st.subheader("Triggered Alerts")
    st.dataframe(alerts_df)
    
    # CSV export buttons
    st.download_button(label="Download Order Data as CSV", data=events_df.to_csv(index=False), file_name="order_data.csv", mime="text/csv")
    st.download_button(label="Download Alerts as CSV", data=alerts_df.to_csv(index=False), file_name="alerts.csv", mime="text/csv")

