import streamlit as st
import pandas as pd

st.title("Streamlit Text Input")

name = st.text_input("Enter your Name:")

age = st.slider("Select your age:",0,100,25)

options = ["Python", "Java", "C++"]

choice = st.selectbox("Choose  your programming language:", options)

if choice:
    st.write(f"You have selected{choice}")
if age:
    st.write(f" You are {age} years old")
if name:
    st.write(f"Hello, {name}")
    
    
data = {
    "Name": ["Aadarsh", "Shrushti", "Bae"],
    "Age": [25,24,25],
    "City": ["Mumbai", "Hyderabad", "Boston"]
}

df = pd.DataFrame(data)
st.write(df)


upload_file = st.file_uploader("Choose a CSV FIle", type="csv")

if upload_file is not None:
    df1 = pd.read_csv(upload_file)
    st.write(df1)