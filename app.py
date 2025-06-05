import streamlit as st
import pandas as pd
import random
import time
import numexpr as ne

# Define the Smoking Scenario rules and parameters
rule_templates = [
    {"name": "Near Side Notional Threshold", "condition": "BaseCcyQty >= 5000000", "configurable": "5000000"},
    {"name": "Far Side Notional Threshold", "condition": "BaseCcyQty <= 5000000", "configurable": "5000000"},
    {"name": "Open Order Lookup Window", "condition": "timestamp.diff().fillna(0) < 45", "configurable": "45"},
    {"name": "Market Depth Lookup Window", "condition": "timestamp.diff().fillna(0) < 45", "configurable": "45"},
    {"name": "Price Comparison Depth Level", "condition": "price >= best_bid", "configurable": "1"},
    {"name": "Trade Inclusion Flag", "condition": "trade_inclusion == True", "configurable": "True"},
    {"name": "Alert Severity", "condition": "severity == 'Medium'", "configurable": "Medium"}
]

# Import functions
from data_generator import generate_order_data
from rule_engine import apply_rules

# Streamlit UI
st.title("Market Abuse Scenario Simulator")

# Sidebar for rule templates
st.sidebar.subheader("Rule Templates")
template_names = [template["name"] for template in rule_templates]
selected_template = st.sidebar.selectbox("Choose a template", [""] + template_names)

if "rules" not in st.session_state:
    st.session_state["rules"] = {}

if selected_template:
    template = next(t for t in rule_templates if t["name"] == selected_template)
    st.sidebar.write(f"Condition: {template['condition']}")
    configurable_value = st.sidebar.text_input(f"Set {template['name']} value", value=template["configurable"])
    st.session_state["rules"][template["name"]] = configurable_value

# Data generation intensity
intensity = st.sidebar.slider("Data Generation Intensity", 0.0, 1.0, 0.3)

# Generate and display data
data = generate_order_data(intensity)
st.write("Generated Order Data")
st.dataframe(data)

# Apply rules and display alerts
alerts = apply_rules(data, rule_templates, st.session_state["rules"])
st.write("Alerts")
st.dataframe(alerts)

# Save alerts to CSV
if st.button("Export Alerts to CSV"):
    alerts.to_csv("alerts.csv", index=False)
    st.success("Alerts exported to alerts.csv")
