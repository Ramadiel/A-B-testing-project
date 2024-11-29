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