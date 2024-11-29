import streamlit as st

# Dummy data for the program and company
program_name = "SuperApp Pro"
creator_name = "John Doe"
company_name = "SuperTech Solutions"
company_description = (
    "SuperTech Solutions is a cutting-edge technology company dedicated to creating innovative products "
    "that empower users to achieve more in less time."
)
st.title("Dummy 2 Page")

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
        color: #f4a261;
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

# Layout with two columns
col1, col2 = st.columns([2, 1])
with col1:
    st.header(program_name)
    st.write(description)

with col2:
    st.markdown(f"### Price: {price}")
    if st.button("Buy Now", key="dummy2_button", help="Click to purchase"):
        st.success("Thank you for your purchase!")

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
