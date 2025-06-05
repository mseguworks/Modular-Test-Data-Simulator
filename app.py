import streamlit as st
import pandas as pd
from data_generator import generate_order_data
from rule_engine import apply_rules
import base64

# Initialize session state
if 'rules' not in st.session_state:
    st.session_state.rules = []

# Function to add a new rule
def add_rule(name, condition):
    st.session_state.rules.append({'name': name, 'condition': condition})

# Function to delete a rule
def delete_rule(index):
    del st.session_state.rules[index]

# Streamlit UI
st.title('Market Abuse Scenario Simulator')

# Sidebar for configuration
st.sidebar.header('Configuration')
num_orders = st.sidebar.number_input('Number of Orders', min_value=1, value=1000)
st.sidebar.write('---')

# Sidebar for rule management
st.sidebar.header('Rules')
with st.sidebar.form(key='add_rule_form'):
    rule_name = st.text_input('Rule Name')
    rule_condition = st.text_input('Rule Condition')
    add_rule_button = st.form_submit_button('Add Rule')
    if add_rule_button and rule_name and rule_condition:
        add_rule(rule_name, rule_condition)

st.sidebar.write('---')
for i, rule in enumerate(st.session_state.rules):
    st.sidebar.write(f"**{rule['name']}**: {rule['condition']}")
    if st.sidebar.button(f"Delete Rule {i+1}"):
        delete_rule(i)

# Generate order data
data = generate_order_data(num_orders)
st.write('## Generated Order Data')
st.dataframe(data)

# Apply rules
if st.session_state.rules:
    data, errors = apply_rules(data, st.session_state.rules)
    st.write('## Rule Application Results')
    st.dataframe(data)
    if errors:
        st.write('## Errors')
        for error in errors:
            st.write(error)

# Export options
st.write('## Export Data')
csv = data.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="order_data.csv">Download CSV File</a>'
st.markdown(href, unsafe_allow_html=True)
