import streamlit as st
import sqlite3
import pandas as pd
import time as t

def create_connection():
    conn = sqlite3.connect('projects.db')
    return conn

def authenticate(username, password):
    if username == "user" and password == "123":
        return True
    else:
        return False

def get_projects(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM projects''')
    projects = cursor.fetchall()
    return projects

def update_project_status(conn, project_id, new_status, certification_url=None):
    cursor = conn.cursor()
    cursor.execute('''UPDATE projects SET status = ? WHERE id = ?''', (new_status, project_id))
    if new_status == "Completed":
        cursor.execute('''UPDATE projects SET url = ? WHERE id = ?''', (certification_url, project_id))
    conn.commit()

def user_page(conn):
    st.title("Certification Requests")
    projects = get_projects(conn)
    if len(projects) > 0:
        df = pd.DataFrame(projects, columns=['ID','Product Name', 'OEM Name',"SKU/Part Number","FW Customer Version","FW Internal Version", 'Requested By', 'Deadline',"Status", 'Operating System',"Certification Type","Certification Link","Comments"])

        # Filter options
        filters = {}
        for col in df.columns:
            if col == 'Status':
                filters[col] = st.sidebar.multiselect(f"Filter {col}", df[col].unique(), default=df[col].unique())
            elif col not in ['Operating System', 'Certification Link',"Comments"]:
                filters[col] = st.sidebar.multiselect(f"Filter {col}", df[col].unique())

        # Apply filters
        filter_mask = pd.Series([True] * len(df))
        for col, value in filters.items():
            if value:
                filter_mask &= df[col].isin(value)

        df_filtered = df[filter_mask]

        # Define colors based on status
        colors = {'In Progress': '#FFCC80', 'Completed': 'lightgreen'}
        
        
        def apply_colors(row):
            return [f"background-color: {colors.get(val, '')}" for val in row]
        
        df_styled = df_filtered.style.apply(apply_colors, axis=1)
        
        st.write(df_styled)
        
        # Allow user to update status by project ID
        project_id = st.number_input("Enter Project ID to update status", min_value=1, max_value=len(df_filtered))
        new_status = st.selectbox("Select new status", [ "In Progress", "Completed"])
        certification_url = None
        if new_status == "Completed":
            certification_url = st.text_input("Enter Certification URL:")
        
        if st.button("Update Status") and project_id and new_status:
            if new_status == "Completed" and not certification_url:
                st.error("Please fill in the Certification URL.")
            else:
                update_project_status(conn, project_id, new_status, certification_url if new_status == "Completed" else None)
                st.success("Status updated successfully!")
                t.sleep(2)
                st.rerun()
        
            
    else:
        st.write("No projects found.")

def main():
    st.set_page_config(page_title="User",layout="wide")
    st.title("User Login")
    
    if 'is_user_logged_in' not in st.session_state:
        st.session_state.is_user_logged_in = False
        
        
    if not st.session_state.is_user_logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")    
    
        if login_button:
            if authenticate(username, password):
                st.session_state.is_user_logged_in = True
                st.empty()
            else:
                st.error("Invalid username or password. Please try again.")
    
    if st.session_state.is_user_logged_in:   
        conn = create_connection()
        user_page(conn)
    
if __name__ == "__main__":
    main()
