import streamlit as st

# Dummy data for the program and company
program_name = "SuperApp Pro"
creator_name = "John Doe"
company_name = "SuperTech Solutions"
company_description = (
    "SuperTech Solutions is a cutting-edge technology company dedicated to creating innovative products "
    "that empower users to achieve more in less time."
)
st.title("Dummy 3 Page")

description = (
    "SuperApp Pro is an innovative application designed to enhance productivity, streamline workflows, "
    "and empower users to achieve more in less time."
)
price = "$49.99"

# Page Layout and Styling
st.markdown(
    """
    <style>
    .header {
        font-family: 'Verdana', sans-serif;
        font-size: 40px;
        text-align: center;
        color: #e63946;
        background-color: #f1faee;
        padding: 20px;
        border-radius: 8px;
    }
    .description {
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        color: #555;
        padding: 10px;
    }
    .price {
        font-family: 'Georgia', serif;
        font-size: 24px;
        color: #e63946;
        font-weight: bold;
    }
    .button {
        background-color: #2d9cdb;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        font-size: 18px;
        cursor: pointer;
    }
    .button:hover {
        background-color: #1a73e8;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Centered layout with additional styling
st.markdown(
    f"""
    <div style="text-align: center;">
        <h1>{program_name}</h1>
        <p style="font-size: 18px;">{description}</p>
        <h3 style="color: green;">Price: {price}</h3>
        <button style="
            padding: 10px 20px; 
            font-size: 16px; 
            background-color: #007BFF; 
            color: white; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer;">
            Buy Now
        </button>
    </div>
    """,
    unsafe_allow_html=True
)

# About the creator and company
st.markdown(
    f"""
    <div class="description">
        <h4>About the Creator:</h4>
        <p>{creator_name} is a seasoned software engineer passionate about productivity tools and enhancing user experience.</p>
        <h4>About {company_name}:</h4>
        <p>{company_description}</p>
    </div>
    """,
    unsafe_allow_html=True
)
