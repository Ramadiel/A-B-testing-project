import streamlit as st
import requests
import os
import random
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Get the FastAPI URL from environment variables
# This allows the API URL to be dynamically configured for different environments.
api_url = os.getenv("API_URL", "http://localhost:8000")

# Initialize session state variables
# These variables store data across Streamlit reruns.
if "product_data" not in st.session_state:
    st.session_state.product_data = {}

if "show_program_buttons" not in st.session_state:
    st.session_state.show_program_buttons = False

# Utility Functions

def create_product(product_name, category, description, logo_url, release_date):
    """
    Create a new product by sending a POST request to the FastAPI endpoint.

    Args:
        product_name (str): Name of the product.
        category (str): Product category.
        description (str): Description of the product.
        logo_url (str): URL of the product logo.
        release_date (str): Release date of the product.

    Returns:
        dict: Response from the FastAPI endpoint if successful, otherwise None.
    """
    payload = {
        "product_name": product_name,
        "category": category,
        "description": description,
        "logo_url": logo_url,
        "release_date": release_date,
    }
    response = requests.post(f"{api_url}/products/", json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to create product.")
        return None

def get_product_by_id(product_id: int) -> dict:
    """
    Fetch product details by product ID using a GET request.

    Args:
        product_id (int): ID of the product.

    Returns:
        dict: Product details if found, otherwise None.
    """
    response = requests.get(f"{api_url}/products/{product_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Product not found.")
        return None

def fetch_results(test_id: int):
    """
    Fetch results for a specific test ID using a GET request.

    Args:
        test_id (int): Test ID to fetch results for.

    Returns:
        list: List of results if successful, otherwise an empty list.
    """
    response = requests.get(f"{api_url}/results/?test_id={test_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch results.")
        return []

def redirect_to_page(page_name: str, product_id: int):
    """
    Redirect the user to another page using HTML meta refresh.

    Args:
        page_name (str): Target page name.
        product_id (int): ID of the product to include in the URL.
    """
    page_url = f"http://localhost:8501/{page_name}?product_id={product_id}"
    st.markdown(f'<meta http-equiv="refresh" content="0;url={page_url}">', unsafe_allow_html=True)

def render_visualizations(page_name, test_id):
    """
    Render visualizations for a specific test ID.

    Args:
        page_name (str): Name of the page for which to render visualizations.
        test_id (int): Test ID to fetch and visualize results for.
    """
    st.subheader(f"{page_name.capitalize()} Visualizations")

    results = fetch_results(test_id)

    if results:
        df = pd.DataFrame(results)

        # Seaborn visualizations for Exploratory Data Analysis (EDA)
        fig1, ax1 = plt.subplots()
        sns.countplot(data=df, x="click_through_rate", ax=ax1)
        ax1.set_title("Click Through Rate Distribution")
        ax1.tick_params(axis='x', rotation=45)
        ax1.tick_params(axis='y', which='major', labelsize=8)
        
        fig2, ax2 = plt.subplots()
        sns.boxplot(data=df, x="test_id", y="conversion_rate", ax=ax2)
        ax2.set_title("Conversion Rate by Test Group")
        ax2.tick_params(axis='y', which='major', labelsize=8)

        # Plotly histogram visualizations for interactivity
        fig_clicks = px.histogram(df, x="click_through_rate", title="Click Through Rate Distribution")
        fig_conversions = px.histogram(df, x="conversion_rate", title="Conversion Rate Distribution")
        fig_bounce = px.histogram(df, x="bounce_rate", title="Bounce Rate Distribution")

        # Layout in two rows
        col1, col2 = st.columns(2)  # First row
        with col1:
            st.pyplot(fig1)  # Seaborn plot
        with col2:
            st.pyplot(fig2)  # Seaborn plot
        
        col3, col4, col5 = st.columns(3)  # Second row (Plotly interactive charts)
        with col3:
            st.plotly_chart(fig_clicks, key=f"clicks_{test_id}")
        with col4:
            st.plotly_chart(fig_conversions, key=f"conversions_{test_id}")
        with col5:
            st.plotly_chart(fig_bounce, key=f"bounce_{test_id}")
    else:
        st.warning("No results available for this page.")

# Function to generate and send random results to FastAPI
def generate_and_create_results(test_id, num_results=50):
    """
    Generate and send random results to the FastAPI backend.

    Args:
        test_id (int): Test ID to associate the results with.
        num_results (int): Number of results to generate. Default is 50.
    """
    for _ in range(num_results):
        if test_id == 1:  # Dummy1
            result_data = {
                "click_through_rate": round(random.uniform(0.1, 0.3), 2),  # Range 0.1 to 0.3
                "conversion_rate": round(random.uniform(0.05, 0.15), 2),  # Range 0.05 to 0.15
                "bounce_rate": round(random.uniform(0.2, 0.5), 2),        # Range 0.2 to 0.5
                "test_id": test_id
            }
        elif test_id == 2:  # Dummy2
            result_data = {
                "click_through_rate": round(random.uniform(0.3, 0.5), 2),  # Range 0.3 to 0.5
                "conversion_rate": round(random.uniform(0.1, 0.2), 2),    # Range 0.1 to 0.2
                "bounce_rate": round(random.uniform(0.4, 0.6), 2),        # Range 0.4 to 0.6
                "test_id": test_id
            }
        elif test_id == 3:  # Dummy3
            result_data = {
                "click_through_rate": round(random.uniform(0.15, 0.35), 2), # Range 0.15 to 0.35
                "conversion_rate": round(random.uniform(0.05, 0.1), 2),    # Range 0.05 to 0.1
                "bounce_rate": round(random.uniform(0.3, 0.7), 2),         # Range 0.3 to 0.7
                "test_id": test_id
            }
        response = requests.post(f"{api_url}/results/", json=result_data)

# Populate data for a page when button is pressed
def populate_data(page_name):
    """
    Populate the backend with data for a specific page.

    Args:
        page_name (str): Page name (e.g., Dummy1, Dummy2, Dummy3).
    """
    page_map = {"Dummy1": 1, "Dummy2": 2, "Dummy3": 3}
    if page_name in page_map:
        test_id = page_map[page_name]
        generate_and_create_results(test_id)
    else:
        st.error("Invalid page name")

# Check query parameters
query_params = st.experimental_get_query_params()
current_page = query_params.get("page", ["main"])[0]

if current_page == "main":
    # Main App Logic
    st.title("Customer and Product Management System")

    st.subheader("Input Details")
    product_name = st.text_input("Product Name")
    product_category = st.text_input("Product Category")
    product_description = st.text_input("Product Description")
    product_logo_url = st.text_input("Product Logo URL")
    product_release_date = st.text_input("Product Release Date")

    if st.button("Create"):
        if product_name and product_category and product_description and product_logo_url and product_release_date:
            product = create_product(product_name, product_category, product_description, product_logo_url, product_release_date)
            if product:
                st.session_state.product_data = product
                st.session_state.show_program_buttons = True
                st.success("Product created successfully!")

                # Populate data for all three dummy pages immediately
                populate_data("Dummy1")
                populate_data("Dummy2")
                populate_data("Dummy3")
            else:
                st.error("Product creation failed.")
        else:
            st.warning("Please fill in all product details.")

    if st.session_state.show_program_buttons:
        st.subheader("Select a Program Page")
        cols = st.columns(3)
        with cols[0]:
            if st.button("Go to Dummy 1"):
                redirect_to_page("Dummy1", st.session_state.product_data["product_id"])
        with cols[1]:
            if st.button("Go to Dummy 2"):
                redirect_to_page("Dummy2", st.session_state.product_data["product_id"])
        with cols[2]:
            if st.button("Go to Dummy 3"):
                redirect_to_page("Dummy3", st.session_state.product_data["product_id"])

    # Show visualizations directly on the main page after creating the product
    if st.session_state.show_program_buttons:
        st.subheader("Visualizations")
        test_ids = [1, 2, 3]
        for test_id in test_ids:
            render_visualizations(f"Dummy{test_id}", test_id)

else:
    product_id = int(query_params.get("product_id", [0])[0])
    product_data = get_product_by_id(product_id)

    if product_data:
        st.title(f"{current_page.capitalize()} Page")
        st.write(f"Product Name: {product_data['product_name']}")
        st.write(f"Category: {product_data['category']}")
        st.write(f"Description: {product_data['description']}")
        st.image(product_data['logo_url'])
        st.write(f"Release Date: {product_data['release_date']}")

        # Render visualizations based on page and test ID
        if current_page == "Dummy1":
            render_visualizations("Dummy1", test_id=1)
        elif current_page == "Dummy2":
            render_visualizations("Dummy2", test_id=2)
        elif current_page == "Dummy3":
            render_visualizations("Dummy3", test_id=3)
    else:
        st.error("No product data available. Please return to the main page and create a product.")
