import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_connection():
    return sqlite3.connect('projects.db')

# Fetch projects from the database
def get_projects(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM projects''')
    return cursor.fetchall()

def visualize_data(df):
    st.title("Project Data Visualization Dashboard")

    # Add a section for the owner's information
    with st.container():
        st.markdown("""
        ### Contact Details
        **Name:** Madhusudan M \n
        **Email:** madhusudan.m@wdc.com   
        """)
    
    # Add a sidebar for filters
    st.sidebar.header("Filter Projects")
    oem_filter = st.sidebar.multiselect("Select OEM(s)", df['OEM Name'].unique())
    status_filter = st.sidebar.multiselect("Select Status", df['Status'].unique())
    
    # Apply filters
    if oem_filter:
        df = df[df['OEM Name'].isin(oem_filter)]
    if status_filter:
        df = df[df['Status'].isin(status_filter)]

    # Create columns for layout
    col1, col2 = st.columns(2)
    
    # Status distribution
    with col1:
        st.subheader("Project Status Distribution")
        status_counts = df['Status'].value_counts()
        fig_status = px.pie(df, names=status_counts.index, values=status_counts.values, title="Project Status Distribution", hole=0.4)
        st.plotly_chart(fig_status, use_container_width=True)

    # Projects per OEM
    with col2:
        st.subheader("Projects per OEM")
        oem_counts = df['OEM Name'].value_counts()
        fig_oem = px.bar(df, x=oem_counts.index, y=oem_counts.values, labels={'x': 'OEM Name', 'y': 'Number of Projects'}, title="Projects per OEM", color=oem_counts.index)
        st.plotly_chart(fig_oem, use_container_width=True)

    # Certification Types
    st.subheader("Certification Types")
    cert_type_counts = df['Certification Type'].value_counts()
    fig_cert_type = px.bar(df, x=cert_type_counts.index, y=cert_type_counts.values, labels={'x': 'Certification Type', 'y': 'Number of Projects'}, title="Certification Types", color=cert_type_counts.index, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_cert_type, use_container_width=True)

    # Projects Deadline Timeline
    st.subheader("Projects Deadline Timeline")
    df['Deadline'] = pd.to_datetime(df['Deadline'], errors='coerce')
    df_deadline = df.dropna(subset=['Deadline'])
    fig_deadline = px.scatter(df_deadline, x='Deadline', y='Product Name', color='Status', title="Projects Deadline Timeline", size='ID', size_max=10, hover_name='Product Name', color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig_deadline, use_container_width=True)

    # Summary Metrics
    st.subheader("Summary Metrics")
    total_projects = len(df)
    completed_projects = len(df[df['Status'] == 'Completed'])
    in_progress_projects = len(df[df['Status'] == 'In Progress'])
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        fig_total = go.Figure(go.Indicator(
            mode = "number",
            value = total_projects,
            title = {"text": "Total Projects"},
        ))
        st.plotly_chart(fig_total, use_container_width=True)
    
    with col4:
        fig_completed = go.Figure(go.Indicator(
            mode = "number",
            value = completed_projects,
            title = {"text": "Completed Projects"},
        ))
        st.plotly_chart(fig_completed, use_container_width=True)
    
    with col5:
        fig_in_progress = go.Figure(go.Indicator(
            mode = "number",
            value = in_progress_projects,
            title = {"text": "In Progress Projects"},
        ))
        st.plotly_chart(fig_in_progress, use_container_width=True)

def main():
    st.set_page_config(page_title="Project Dashboard", layout="wide", initial_sidebar_state="expanded")
    conn = create_connection()
    projects = get_projects(conn)
    
    if projects:
        df = pd.DataFrame(projects, columns=['ID','Product Name', 'OEM Name',"SKU/Part Number","FW Customer Version","FW Internal Version", 'Requested By', 'Deadline',"Status", 'Operating System',"Certification Type","Certification Link","Comments"])
        visualize_data(df)
    else:
        st.write("No projects found.")

if __name__ == "__main__":
    main()
