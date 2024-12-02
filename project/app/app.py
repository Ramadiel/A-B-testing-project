import streamlit as st
import requests
import os

# Get the FastAPI URL from environment variables
api_url = os.getenv("API_URL", "http://localhost:8000")

# Set up the Streamlit app title
st.title("Customer Management System")

# -----------------------------------------------------
# Utility Functions (API Interactions)
# -----------------------------------------------------

def get_customer_by_id(customer_id: int) -> dict:
    """
    Fetch customer details by their ID.
    
    Parameters:
    - customer_id (int): The ID of the customer to retrieve.

    Returns:
    - dict: The customer's details if found, or None with an error message.
    """
    response = requests.get(f"{api_url}/customers/{customer_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Customer not found.")
        return None

def create_customer(name: str, email: str) -> dict:
    """
    Create a new customer record.
    
    Parameters:
    - name (str): customer's first name.
    - email (str): customer's email address.

    Returns:
    - dict: The created customer's details or an error message if failed.
    """
    payload = {
        "name": name,
        "email": email,
    }
    response = requests.post(f"{api_url}/customers/", json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to create customer.")
        return None

def update_email(customer_id: int, new_email: str) -> dict:
    """
    Update an existing customer's email by sending the full customer payload.
    
    Parameters:
    - customer_id (int): The ID of the customer whose email will be updated.
    - new_email (str): The new email amount.

    Returns:
    - dict: Updated customer details if successful or an error message if failed.
    """
    # Step 1: Get the current details of the customer
    customer = get_customer_by_id(customer_id)
    if not customer:
        st.error("customer not found, cannot update email.")
        return None
    
    # Step 2: Prepare the full payload with the updated email
    payload = {
        "name": customer["name"],
        "email": new_email  # Update the email here
    }

    # Step 3: Send PUT request with the complete payload
    response = requests.put(f"{api_url}/customers/{customer_id}", json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to update email.")
        return None


    
def delete_customer(customer_id: int) -> dict:
    """
    Delete an customer record by ID.
    
    Parameters:
    - customer_id (int): The ID of the customer to delete.

    Returns:
    - dict: Success message if deleted or an error message if failed.
    """
    response = requests.delete(f"{api_url}/customers/{customer_id}")
    if response.status_code == 200:
        return {"message": "customer deleted successfully."}
    else:
        st.error("Failed to delete customer.")
        return None

# -----------------------------------------------------
# UI Components
# -----------------------------------------------------

# Section: Get an customer by ID
st.subheader("Get customer by ID")
customer_id_search = st.number_input("customer ID for Search", min_value=1, step=1)
if st.button("Get customer"):
    customer = get_customer_by_id(customer_id_search)
    if customer:
        st.write("customer Details:")
        st.json(customer)

# Section: Add New customer
st.subheader("Add New customer")
with st.form("customer_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Create customer")

    if submitted:
        customer = create_customer(name, email)
        if customer:
            st.success("customer created successfully!")
            st.write(customer)

# Section: Update customer email
st.subheader("Update customer email")
customer_id = st.number_input("customer ID", min_value=1, step=1)
new_email = st.text_input("New email")
if st.button("Update email"):
    updated_customer = update_email(customer_id, new_email)
    if updated_customer:
        st.success("email updated successfully!")
        st.write(updated_customer)

# Section: Remove customer
st.subheader("Remove customer")
customer_id_delete = st.number_input("customer ID for Deletion", min_value=1, step=1)
if st.button("Delete customer"):
    result = delete_customer(customer_id_delete)
    if result:
        st.success(result["message"])

import streamlit as st
import requests
import os

# Get the FastAPI URL from environment variables
api_url = os.getenv("API_URL", "http://localhost:8000")

# Set up the Streamlit app title
st.title("product Management System")

# -----------------------------------------------------
# Utility Functions (API Interactions)
# -----------------------------------------------------

def get_product_by_id(product_id: int) -> dict:
    """
    Fetch product details by their ID.
    
    Parameters:
    - product_id (int): The ID of the product to retrieve.

    Returns:
    - dict: The product's details if found, or None with an error message.
    """
    response = requests.get(f"{api_url}/products/{product_id}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("product not found.")
        return None

def create_product(product_name: str, category: str, description: str, logo_url: str, release_date: str) -> dict:
    """
    Create a new product record.
    
    Parameters:
    - product_name (str): product's name.
    - category (str): product's category.
    - description (str): product's description.
    - logo_url (str): product's logo url.
    - release_date (str): product's release date.

    Returns:
    - dict: The created product's details or an error message if failed.
    """
    payload = {
        "product_name": product_name,
        "category": category,
        "description": description,
        "logo_url": logo_url,
        "release_date": release_date
    }
    response = requests.post(f"{api_url}/products/", json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to create product.")
        return None

def update_description(product_id: int, new_description: str) -> dict:
    """
    Update an existing product's description by sending the full product payload.
    
    Parameters:
    - product_id (int): The ID of the product whose description will be updated.
    - new_description (str): The new description amount.

    Returns:
    - dict: Updated product details if successful or an error message if failed.
    """
    # Step 1: Get the current details of the product
    product = get_product_by_id(product_id)
    if not product:
        st.error("product not found, cannot update description.")
        return None
    
    # Step 2: Prepare the full payload with the updated description
    payload = {
        "product_name":product["product_name"],
        "category":product["category"],
        "description":new_description,
        "logo_url": product["logo_url"],
        "release_date":product["release_date"]
    }

    # Step 3: Send PUT request with the complete payload
    response = requests.put(f"{api_url}/products/{product_id}", json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to update description.")
        return None


    
def delete_product(product_id: int) -> dict:
    """
    Delete an product record by ID.
    
    Parameters:
    - product_id (int): The ID of the product to delete.

    Returns:
    - dict: Success message if deleted or an error message if failed.
    """
    response = requests.delete(f"{api_url}/products/{product_id}")
    if response.status_code == 200:
        return {"message": "product deleted successfully."}
    else:
        st.error("Failed to delete product.")
        return None

# -----------------------------------------------------
# UI Components
# -----------------------------------------------------

# Section: Get an product by ID
st.subheader("Get product by ID")
product_id_search = st.number_input("product ID for Search", min_value=1, step=1)
if st.button("Get product"):
    product = get_product_by_id(product_id_search)
    if product:
        st.write("product Details:")
        st.json(product)

# Section: Add New product
st.subheader("Add New product")
with st.form("product_form"):
    product_name = st.text_input("product name")
    category = st.text_input("category")
    description = st.text_input("description")
    logo_url = st.text_input("logo url")
    release_date = st.text_input("release date")
    
    submitted = st.form_submit_button("Create product")

    if submitted:
        product = create_product(product_name, category, description, logo_url, release_date)
        if product:
            st.success("product created successfully!")
            st.write(product)

# Section: Update product description
st.subheader("Update product description")
product_id = st.number_input("product ID", min_value=1, step=1)
new_description = st.text_input("New description")
if st.button("Update description"):
    updated_product = update_description(product_id, new_description)
    if updated_product:
        st.success("description updated successfully!")
        st.write(updated_product)

# Section: Remove product
st.subheader("Remove product")
product_id_delete = st.number_input("product ID for Deletion", min_value=1, step=1)
if st.button("Delete product"):
    result = delete_product(product_id_delete)
    if result:
        st.success(result["message"])

st.markdown("---")  # Horizontal line for separation

# Left-aligned headline

def redirect_to_page(page_name: str):
    """Function to redirect to a specific page URL."""
    page_url = f"http://localhost:8501/{page_name.replace(' ', '_')}"
    st.markdown(f'<meta http-equiv="refresh" content="0;url={page_url}">', unsafe_allow_html=True)

# -----------------------------------------------------
# Main App Logic
# -----------------------------------------------------

# Initialize session state variables
if "show_buttons" not in st.session_state:
    st.session_state.show_buttons = False

# Left-aligned headline for page creation
st.markdown("### Page Creation")  # Use H3 for a smaller headline

# Create button to reveal page selection
if st.button("Create", use_container_width=True):
    st.session_state.show_buttons = True  # Show buttons when "Create" is clicked

# Display buttons to navigate to pages if "Create" was clicked
if st.session_state.get("show_buttons"):
    st.subheader("Select a Program Page")

    # Create buttons for each dummy page
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Go to Dummy 1"):
            redirect_to_page("Dummy_1")  # Redirect to Dummy 1 page

    with col2:
        if st.button("Go to Dummy 2"):
            redirect_to_page("Dummy_2")  # Redirect to Dummy 2 page

    with col3:
        if st.button("Go to Dummy 3"):
            redirect_to_page("Dummy_3")  # Redirect to Dummy 3 page