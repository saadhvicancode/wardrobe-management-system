import time
import streamlit as st
from create1 import create
from read1 import read
from update1 import update
from delete1 import delete
from connection1 import fun
import pandas as pd

# Define User class
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
        self.allowed_tables = []

# Define users with different roles and table access
admin_user = User(username="admin", password="admin", role="admin")
admin_user.allowed_tables = ["Category", "CategoryItems", "Items", "Outfits", "UserItems", "Users"]

user_user = User(username="user", password="user", role="user")
user_user.allowed_tables = ["Category", "CategoryItems", "Items", "Outfits", "UserItems", "Users"]

# Define the tables that users can manage and their corresponding available operations
admin_managed_tables = {
    "Category": ["Read", "Create", "Update", "Delete"],
    "CategoryItems": ["Read", "Create", "Delete"],
    "Items": ["Read", "Create", "Update", "Delete"],
    "Outfits": ["Read", "Create", "Update", "Delete"],
    "UserItems": ["Read", "Create", "Delete"],
    "Users": ["Read", "Create", "Update", "Delete"]
}

user_managed_tables = {
    "Category": ["Read", "Create"],
    "CategoryItems": ["Read", "Create"],
    "Items": ["Read", "Create"],
    "Outfits": ["Read", "Create"],
    "UserItems": ["Read", "Create"],
    "Users": ["Create"]
}

# Streamlit app layout
db = fun()

# Set page title and favicon
st.set_page_config(
    page_title="Virtual Wardrobe Management System",
    page_icon="👔",
    layout="wide"
)

# Set background image using custom CSS
background_image = 'your_background_image.jpg'
st.markdown(
    f"""
    <style>
        body {{
            background-image: url('{background_image}');
            background-size: cover;
        }}
        .center {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Add to the top of your script
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.login_button_clicked = False

# Check if user is not logged in
if st.session_state.user is None:
    # Login section
    st.title("Login")

    # Adding unique keys to text_input
    username_input = st.text_input("Username:", key="username_input")
    password_input = st.text_input("Password:", type="password", key="password_input")

    login_button_clicked = st.button("Login")

    if login_button_clicked:
        users = [admin_user, user_user]
        for user in users:
            if username_input == user.username and password_input == user.password:
                st.session_state.user = user  # Store the user object directly
                st.success(f"Logged in as {user.role} user.")

                # Store user role and username in session state
                st.session_state.role = user.role
                st.session_state.username = user.username

                # Rerun the app to show the main app
                st.rerun()
                break
        else:
            st.error("Invalid username or password.")
else:
    # User is logged in, show the main app
    user_role = st.session_state.user.role  # This now accesses the User object correctly
    allowed_tables = st.session_state.user.allowed_tables

    st.sidebar.subheader("Tables Managed by User")
    selected_table = st.sidebar.selectbox("Select Table", allowed_tables)

    if user_role == "admin":
        available_operations = admin_managed_tables[selected_table]
    elif user_role == "user":
        available_operations = user_managed_tables[selected_table]

    st.sidebar.subheader("Operations")
    operation = st.sidebar.selectbox("Select Operation", available_operations)

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.login_button_clicked = False
        st.rerun()  # Rerun the app to show the login page
        st.info("Logged out successfully. Please log in again.")

    # Adjust operations based on user role and specific table permissions
    if operation == "Create" and "Create" in available_operations:
        st.subheader("Enter Details for {}".format(selected_table))
        create(selected_table, db)
    elif operation == "Read" and "Read" in available_operations:
        st.subheader("View Details from {}".format(selected_table))
        read(selected_table, db)

        if selected_table == "CategoryItems":
            if st.button("Find Names"):
                st.subheader("Item and Category Names:")
                try:
                    cursor = db.cursor()
                    query = """
                    SELECT
                    (SELECT Category.category_name FROM Category WHERE Category.category_id = CategoryItems.category_id) AS category_name,
                    (SELECT Items.item_name FROM Items WHERE Items.item_id = CategoryItems.item_id) AS item_name
                    FROM CategoryItems;
                    """
                    cursor.execute(query)
                    query_result = cursor.fetchall()
                    df = pd.DataFrame(query_result, columns=[desc[0] for desc in cursor.description])
                    st.write(df)
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    cursor.close()

        # Additional query logic for other tables here...
        # ...

    elif operation == "Update" and "Update" in available_operations:
        st.subheader('Update Details in {}'.format(selected_table))
        update(selected_table, db)
    elif operation == "Delete" and "Delete" in available_operations:
        st.subheader('Delete Details in {}'.format(selected_table))
        delete(selected_table, db)
    else:
        st.subheader("About Tasks")

# Add custom footer or additional information
st.markdown("---")
st.markdown("Virtual Wardrobe")
