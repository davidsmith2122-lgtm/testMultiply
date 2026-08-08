import streamlit as st

st.title("Simple Multiplier")

x = st.number_input("Enter first number", value=0.0)
y = st.number_input("Enter second number", value=0.0)

result = x * y

st.write(f"Result: {result}")