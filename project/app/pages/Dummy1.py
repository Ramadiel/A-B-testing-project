# Dummy1 Page

import streamlit as st
import requests
import os

# Get the FastAPI URL from environment variables
api_url = os.getenv("API_URL", "http://localhost:8000")

def get_product_by_id(product_id: int) -> dict:
    """Fetch product details by their ID.

    Args:
        product_id (int): The ID of the product to fetch.

    Returns:
        dict: A dictionary containing product details if successful, otherwise None.
    """
    response = requests.get(f"{api_url}/products/{product_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Product not found.")
        return None

# Get query parameters
query_params = st.experimental_get_query_params()
product_id = query_params.get("product_id", [None])[0]

if product_id:
    product = get_product_by_id(int(product_id))
    if product:
        # Display the product details in a styled format
        st.title("Dummy 1 Page")
        st.markdown(
            f"""
            <div style="text-align: center; font-family: Verdana, sans-serif;">
                <h1 style="color: #1a73e8;">{product['product_name']}</h1>
                <p style="font-size: 18px; color: #555;">{product['description']}</p>
                <p style="font-size: 16px;">Category: {product['category']}</p>
                <img src="{product['logo_url']}" alt="Product Logo" style="width:100%; border-radius: 10px;"/>
                <p style="font-size: 14px; color: gray;">Release Date: {product['release_date']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Add a "Buy Now" button with feedback
        if st.button("Buy Now"):
            st.success("Thank you for your purchase!")
    else:
        st.error("Failed to fetch product details.")
else:
    st.warning("No product ID provided. Please create a product first.")
