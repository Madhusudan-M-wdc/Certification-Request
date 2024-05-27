import sqlite3
import streamlit as st
import time as t

def create_connection(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def create_projects_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects
                      (id INTEGER PRIMARY KEY,
                       product_name TEXT,
                       oem_name TEXT,
                       sku TEXT,
                       FW_cust_ver TEXT,
                       FW_inter_ver TEXT,
                       requested_by TEXT,
                       deadline TEXT,
                       status TEXT,
                       os TEXT,
                       type TEXT,
                       url TEXT,
                       comments TEXT)
                       ''')
    conn.commit()

def add_project(conn, product_name, oem_name, sku, FW_cust_ver, FW_inter_ver, requested_by, deadline, status, os, type, url, comments):
    cursor = conn.cursor()
    os_str = ', '.join(os)
    type_str = ', '.join(type)
    cursor.execute('''INSERT INTO projects (product_name, oem_name, sku, FW_cust_ver, FW_inter_ver, requested_by, deadline, status, os, type, url, comments)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (product_name, oem_name, sku, FW_cust_ver, FW_inter_ver, requested_by, deadline, status, os_str, type_str, url, comments))
    conn.commit()

def get_sku_options(product_name, oem_name):
    conn = create_connection('sku.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SKU FROM Products WHERE Product=? AND OEM=?", (product_name, oem_name))
    sku_options = cursor.fetchall()
    conn.close()
    return [option[0] for option in sku_options]

def check_sku_exists(conn, product_name, oem_name, sku):
    cursor = conn.cursor()
    cursor.execute("SELECT SKU FROM Products WHERE Product=? AND OEM=? AND SKU=?", (product_name, oem_name, sku))
    return cursor.fetchone() is not None

def add_sku(conn, product_name, oem_name, sku):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Products (Product, OEM, SKU) VALUES (?, ?, ?)", (product_name, oem_name, sku))
    conn.commit()

def admin_page(conn):
    st.title("Admin Dashboard")
    
    product_options = ["Vivaldi", "Vulcan"] 
    oem_options = ['GOEM', "HP", "Dell", "Samsung", "MSFT", "Honor", "LG", "Huawei", "Toshiba", "Lenovo_LBG", "Lenovo_TBG", "Asus", "Acer", "MSI", "Fujitsu"]
    
    product_name = st.selectbox("Product Name", product_options, key="product_select")
    oem_name = st.selectbox("OEM Name", oem_options, key="oem_select")
    
    selected_skus = get_sku_options(product_name, oem_name)
    
    selected_skus = st.multiselect("SKUs available", selected_skus, key="sku_multiselect")
    
    FW_cust_ver = st.text_input("FW Customer Version", key="fw_cust_ver")
    FW_inter_ver = st.text_input("FW Internal Version", key="fw_inter_ver")
    requested_by = st.text_input("Requested By", key="requested_by")
    deadline = st.date_input("Deadline", key="deadline")
    status = "Posted"
    os = st.multiselect("Operating System", ["Win11 22H2", "Win11 23H2", "Win 10"], key="os_multiselect")
    type = st.multiselect("Certification Type", ["WHCK", "WU", "WHQL", "VSAN", "IOVP"], key="type_multiselect")
    comments = st.text_input("Comments", key="comments")
    
    if st.button("Submit", key="submit"):
        if product_name and oem_name and selected_skus and FW_cust_ver and FW_inter_ver and requested_by and deadline and os and type:
            create_projects_table(conn)
            for sku in selected_skus:
                add_project(conn, product_name, oem_name, sku, FW_cust_ver, FW_inter_ver, requested_by, str(deadline), status, os, type, "", comments)
            st.success("Projects added successfully!")
            t.sleep(2)
            st.session_state.is_admin_logged_in = False
            st.experimental_rerun()
        else:
            st.error("Please fill in all the mandatory fields.")

def sidebar_add_sku():
    st.sidebar.title("Add New SKU")
    
    product_options = ["Vivaldi", "Vulcan"]
    oem_options = ['GOEM', "HP", "Dell", "Samsung", "MSFT", "Honor", "LG", "Huawei", "Toshiba", "Lenovo_LBG", "Lenovo_TBG", "Asus", "Acer", "MSI", "Fujitsu"]

    product_name = st.sidebar.selectbox("Product Name", product_options, key="sidebar_product_select")
    oem_name = st.sidebar.selectbox("OEM Name", oem_options, key="sidebar_oem_select")
    new_sku = st.sidebar.text_input("New SKUs (comma separated)", key="sidebar_new_sku")

    if st.sidebar.button("Add SKU", key="sidebar_add_sku_button"):
        conn = create_connection('sku.db')
        skus = [sku.strip() for sku in new_sku.split(',')]  # Split the input string by commas and trim whitespace
        for sku in skus:
            if check_sku_exists(conn, product_name, oem_name, sku):
                st.sidebar.error(f"SKU '{sku}' already exists for the selected Product and OEM.")
            else:
                add_sku(conn, product_name, oem_name, sku)
        st.sidebar.success("SKUs added successfully!")
        t.sleep(2)
        st.rerun()


def authenticate(username, password):
    if username == "admin" and password == "qw":
        return True
    else:
        return False

def main():
    st.set_page_config(page_title="Admin", layout="wide")
    st.title("Admin Login")

    if 'is_admin_logged_in' not in st.session_state:
        st.session_state.is_admin_logged_in = False

    if not st.session_state.is_admin_logged_in:
        username = st.text_input("Username", key="admin_username")
        password = st.text_input("Password", type="password", key="admin_password")
        login_button = st.button("Login", key="login_button")
    
        if login_button:
            if authenticate(username, password):
                st.session_state.is_admin_logged_in = True
                st.empty().empty()
            else:
                st.error("Invalid username or password. Please try again.")
                
    if st.session_state.is_admin_logged_in:
        conn = create_connection('projects.db')
        admin_page(conn)
        sidebar_add_sku()

if __name__ == "__main__":
    main()
