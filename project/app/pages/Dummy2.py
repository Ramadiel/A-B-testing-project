# Dummy2 Page

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
        # Display the product details in a two-column layout
        st.title("Dummy 2 Page")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.header(product['product_name'])
            st.write(product['description'])
        with col2:
            st.image(product['logo_url'], use_column_width=True)
            st.markdown(f"**Category:** {product['category']}")
            st.markdown(f"**Release Date:** {product['release_date']}")
        
        # Add a "Buy Now" button with feedback
        if st.button("Buy Now"):
            st.success("Thank you for your purchase!")
    else:
        st.error("Failed to fetch product details.")
else:
    st.warning("No product ID provided. Please create a product first.")

