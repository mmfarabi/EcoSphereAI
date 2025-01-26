import streamlit as st
import pandas as pd
import joblib
import sqlite3
from openai import OpenAI
from datetime import datetime
import plotly.express as px
import folium
from streamlit_folium import folium_static
from joblib import Parallel, delayed
from datetime import datetime, time, date
from PIL import Image
import io
import base64
import os

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    
    # Create users table with full_name and avatar
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, 
                  password TEXT,
                  full_name TEXT,
                  avatar BLOB)''')
    
    # Create sessions1 table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions1
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  input_data TEXT, 
                  predictions TEXT, 
                  insights TEXT, 
                  timestamp DATETIME)''')

    # Create sessions2 table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions2
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  input_data TEXT, 
                  prediction TEXT, 
                  insights TEXT, 
                  timestamp DATETIME)''')

    # Create sessions3 table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions3
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  input_data TEXT, 
                  predictions TEXT, 
                  insights TEXT, 
                  timestamp DATETIME)''')

    # Create sessions4 table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions4
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  input_data TEXT, 
                  prediction TEXT, 
                  insights TEXT, 
                  timestamp DATETIME)''')

    # Create sessions5 table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions5
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  input_data TEXT, 
                  cost_prediction REAL, 
                  time_prediction REAL, 
                  quantity_prediction INTEGER, 
                  insights TEXT, 
                  timestamp DATETIME)''')

    # Create sessions6 table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions6
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  input_data TEXT, 
                  prediction TEXT, 
                  insights TEXT, 
                  timestamp DATETIME)''')

    # Create sessions7 table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions7
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  input_data TEXT, 
                  cost_prediction REAL, 
                  time_prediction REAL, 
                  insights TEXT, 
                  timestamp DATETIME)''')

    # Create sessions8 table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions8
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  input_data TEXT, 
                  predictions TEXT, 
                  insights TEXT, 
                  timestamp DATETIME)''')

    # Create sessions9 table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions9
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  input_data TEXT, 
                  predictions TEXT, 
                  insights TEXT, 
                  timestamp DATETIME)''')

    # Create tickets1 table
    c.execute('''CREATE TABLE IF NOT EXISTS tickets1
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  username TEXT, 
                  full_name TEXT, 
                  ticket_text TEXT, 
                  timestamp DATETIME)''')

    # Create tickets2 table
    c.execute('''CREATE TABLE IF NOT EXISTS tickets2
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  username TEXT, 
                  full_name TEXT, 
                  ticket_text TEXT, 
                  timestamp DATETIME)''')

    # Create tickets3 table
    c.execute('''CREATE TABLE IF NOT EXISTS tickets3
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  username TEXT, 
                  full_name TEXT, 
                  ticket_text TEXT, 
                  timestamp DATETIME)''')

    # Create tickets4 table
    c.execute('''CREATE TABLE IF NOT EXISTS tickets4
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  username TEXT, 
                  full_name TEXT, 
                  ticket_text TEXT, 
                  timestamp DATETIME)''')

    # Create tickets5 table
    c.execute('''CREATE TABLE IF NOT EXISTS tickets5
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  username TEXT, 
                  full_name TEXT, 
                  ticket_text TEXT, 
                  timestamp DATETIME)''')

    # Create tickets6 table
    c.execute('''CREATE TABLE IF NOT EXISTS tickets6
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  username TEXT, 
                  full_name TEXT, 
                  ticket_text TEXT, 
                  timestamp DATETIME)''')

    # Create tickets7 table
    c.execute('''CREATE TABLE IF NOT EXISTS tickets7
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  username TEXT, 
                  full_name TEXT, 
                  ticket_text TEXT, 
                  timestamp DATETIME)''')

    # Create tickets8 table
    c.execute('''CREATE TABLE IF NOT EXISTS tickets8
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  username TEXT, 
                  full_name TEXT, 
                  ticket_text TEXT, 
                  timestamp DATETIME)''')

    # Create tickets9 table
    c.execute('''CREATE TABLE IF NOT EXISTS tickets9
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, 
                  username TEXT, 
                  full_name TEXT, 
                  ticket_text TEXT, 
                  timestamp DATETIME)''')


    conn.commit()
    conn.close()

# Initialize database
init_db()

# Initialize Gemini AI client
client = OpenAI(
    api_key="AIzaSyA6MLJkBbAHaBwjpBEGwwa5kL2WKWRFqRQ",  # Replace with your actual Gemini API key
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Function to create a rounded image
def rounded_image(image):
    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    # Create a circular mask
    rounded_image_html = f"""
    <style>
        .rounded-image {{
            border-radius: 50%;
            overflow: hidden;
            width: 100px;
            height: 100px;
            object-fit: cover;
        }}
    </style>
    <img src="data:image/png;base64,{img_str}" class="rounded-image">
    """
    return rounded_image_html

# Function to validate password
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    return True, ""

# Function to update user information
def update_user_info(user_id, full_name, username, password, avatar):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    if avatar is not None:
        c.execute('''UPDATE users SET full_name = ?, username = ?, password = ?, avatar = ? WHERE id = ?''', 
                  (full_name, username, password, avatar, user_id))
    else:
        c.execute('''UPDATE users SET full_name = ?, username = ?, password = ? WHERE id = ?''', 
                  (full_name, username, password, user_id))
    conn.commit()
    conn.close()

# Function to fetch user information
def fetch_user_info(user_id):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute('''SELECT full_name, username, password, avatar FROM users WHERE id = ?''', (user_id,))
    user_info = c.fetchone()
    conn.close()
    return user_info

# Dashboard Page
def dashboard_page():
    # Function to validate dataset columns
    def validate_dataset(dataset, required_columns):
        if not all(column in dataset.columns for column in required_columns):
            return False
        return True

    # Load default datasets
    nodes = pd.read_csv("nodes.csv")
    energy_usage = pd.read_csv("energy_usage.csv")
    environment = pd.read_csv("environment.csv")
    procurement = pd.read_csv("procurement.csv")
    traffic = pd.read_csv("traffic.csv")

    # Streamlit App Title
    st.title("EcoSphereAI Dashboard")

    # Create tabs for navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Nodes", "Energy Usage", "Environment", "Procurement", "Traffic"])

    # Nodes Tab
    with tab1:
        st.header("Nodes Data")

        # File Upload Option for Nodes
        uploaded_nodes = st.file_uploader("Upload Nodes CSV", type=["csv"], key="nodes")
        if uploaded_nodes is not None:
            try:
                nodes = pd.read_csv(uploaded_nodes)
                required_columns = ['Node_ID', 'Region', 'Population_Served', 'Connectivity_Status', 'Existing_Infrastructure', 'Latitude', 'Longitude', 'Type']
                if not validate_dataset(nodes, required_columns):
                    st.warning("Invalid dataset uploaded. Please ensure the dataset contains the required columns.")
                    nodes = pd.read_csv("nodes.csv")
            except Exception as e:
                st.warning(f"Invalid dataset uploaded. Error: {e}")
                nodes = pd.read_csv("nodes.csv")

        # Display the DataFrame
        st.write(nodes)

        # Cards for Nodes Metrics
        st.subheader("Nodes Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown("**Total Nodes**")
        col1.markdown(f"<div style='text-align: center; font-size: 24px;'>{len(nodes)}</div>", unsafe_allow_html=True)
        col2.markdown("**Total Regions**")
        col2.markdown(f"<div style='text-align: center; font-size: 24px;'>{nodes['Region'].nunique()}</div>", unsafe_allow_html=True)
        col3.markdown("**Total Population Served**")
        col3.markdown(f"<div style='text-align: center; font-size: 24px;'>{nodes['Population_Served'].sum()}</div>", unsafe_allow_html=True)
        col4.markdown("**Connected Nodes**")
        col4.markdown(f"<div style='text-align: center; font-size: 24px;'>{nodes[nodes['Connectivity_Status'] == 'Connected'].shape[0]}</div>", unsafe_allow_html=True)

        col5, col6 = st.columns(2)
        col5.markdown("**Unconnected Nodes**")
        col5.markdown(f"<div style='text-align: center; font-size: 24px;'>{nodes[nodes['Connectivity_Status'] == 'Unconnected'].shape[0]}</div>", unsafe_allow_html=True)

        # Organization Types
        st.subheader("Organization Types")
        org_types = nodes['Type'].value_counts().reset_index()
        org_types.columns = ['Type', 'Count']
        st.write(org_types)

        # Node Search Option
        st.subheader("Search for a Node")
        search_node_id = st.text_input("Enter Node ID to search:")
        searched_node = None

        if search_node_id:
            filtered_nodes = nodes[nodes['Node_ID'].astype(str).str.contains(search_node_id)]
            if not filtered_nodes.empty:
                searched_node = filtered_nodes.iloc[0]
                st.success(f"Node {searched_node['Node_ID']} found!")
            else:
                st.warning("No matching Node ID found.")

        # Node Locations on Map with Enhanced Popups
        st.subheader("Node Locations on Map")
        stamen_terrain = folium.TileLayer(
            tiles='https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png',
            attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
            name='Stamen Terrain'
        )

        if searched_node is not None:
            map_center = [searched_node['Latitude'], searched_node['Longitude']]
            zoom_level = 10
        else:
            map_center = [nodes['Latitude'].mean(), nodes['Longitude'].mean()]
            zoom_level = 2

        map = folium.Map(location=map_center, zoom_start=zoom_level)
        stamen_terrain.add_to(map)

        for idx, row in nodes.iterrows():
            if row['Connectivity_Status'] == 'Connected':
                color = 'green'
            else:
                color = 'red'

            popup_content = f"""
                <b>Node ID:</b> {row['Node_ID']}<br>
                <b>Region:</b> {row['Region']}<br>
                <b>Population Served:</b> {row['Population_Served']}<br>
                <b>Connectivity Status:</b> {row['Connectivity_Status']}<br>
                <b>Existing Infrastructure:</b> {'Yes' if row['Existing_Infrastructure'] == 1 else 'No'}<br>
                <b>Latitude:</b> {row['Latitude']}<br>
                <b>Longitude:</b> {row['Longitude']}<br>
                <b>Type:</b> {row['Type']}
            """
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color=color, icon='flag')
            ).add_to(map)

        if searched_node is not None:
            searched_popup_content = f"""
                <b>Node ID:</b> {searched_node['Node_ID']}<br>
                <b>Region:</b> {searched_node['Region']}<br>
                <b>Population Served:</b> {searched_node['Population_Served']}<br>
                <b>Connectivity Status:</b> {searched_node['Connectivity_Status']}<br>
                <b>Existing Infrastructure:</b> {'Yes' if searched_node['Existing_Infrastructure'] == 1 else 'No'}<br>
                <b>Latitude:</b> {searched_node['Latitude']}<br>
                <b>Longitude:</b> {searched_node['Longitude']}<br>
                <b>Type:</b> {searched_node['Type']}
            """
            folium.Marker(
                location=[searched_node['Latitude'], searched_node['Longitude']],
                popup=folium.Popup(searched_popup_content, max_width=300),
                icon=folium.Icon(color='blue', icon='star')
            ).add_to(map)

        folium_static(map)

        # Regional Connectivity Insights
        st.subheader("Regional Connectivity Insights")
        nodes['Existing_Infrastructure'] = nodes['Existing_Infrastructure'].map({'Yes': 1, 'No': 0})
        nodes['Connectivity_Status'] = nodes['Connectivity_Status'].map({'Connected': 1, 'Unconnected': 0})

        regional_analysis = nodes.groupby('Region').agg({
            'Connectivity_Status': 'mean',
            'Population_Served': 'sum',
            'Existing_Infrastructure': 'mean',
            'Node_ID': 'count',
        }).reset_index()

        regional_analysis.rename(columns={
            'Connectivity_Status': 'Connectivity_Rate',
            'Existing_Infrastructure': 'Infrastructure_Rate',
            'Node_ID': 'Node_Count'
        }, inplace=True)

        st.write(regional_analysis[['Region', 'Connectivity_Rate', 'Population_Served', 'Infrastructure_Rate']])

        st.subheader("Regions with the Lowest Connectivity Rates (Priority for Improvement)")
        low_connectivity_regions = regional_analysis.sort_values(by='Connectivity_Rate', ascending=True)[['Region', 'Connectivity_Rate', 'Population_Served']]
        st.write(low_connectivity_regions)

        st.subheader("Connectivity Ratio by Region")
        connectivity_ratio = nodes.groupby('Region')['Connectivity_Status'].apply(lambda x: (x == 1).mean()).reset_index()
        fig = px.bar(connectivity_ratio, x='Region', y='Connectivity_Status', labels={'Connectivity_Status': 'Connected Ratio'}, color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig)

    # Energy Usage Tab
    with tab2:
        st.header("Energy Usage Data")

        # File Upload Option for Energy Usage
        uploaded_energy_usage = st.file_uploader("Upload Energy Usage CSV", type=["csv"], key="energy_usage")
        if uploaded_energy_usage is not None:
            try:
                energy_usage = pd.read_csv(uploaded_energy_usage)
                required_columns = ['Energy_Usage_kWh', 'Carbon_Emissions_kg_CO2', 'Energy_Source', 'Peak_Usage_Time']
                if not validate_dataset(energy_usage, required_columns):
                    st.warning("Invalid dataset uploaded. Please ensure the dataset contains the required columns.")
                    energy_usage = pd.read_csv("energy_usage.csv")
            except Exception as e:
                st.warning(f"Invalid dataset uploaded. Error: {e}")
                energy_usage = pd.read_csv("energy_usage.csv")

        # Display the DataFrame
        st.write(energy_usage)

        st.header("Energy Usage Metrics")
        col1, col2, col3 = st.columns(3)
        col1.markdown("**Total Energy Used (kWh)**")
        col1.markdown(f"<div style='text-align: center; font-size: 24px;'>{energy_usage['Energy_Usage_kWh'].sum()}</div>", unsafe_allow_html=True)
        col2.markdown("**Total Carbon Emissions (kg CO2)**")
        col2.markdown(f"<div style='text-align: center; font-size: 24px;'>{energy_usage['Carbon_Emissions_kg_CO2'].sum()}</div>", unsafe_allow_html=True)
        col3.markdown("**Energy Sources**")
        col3.markdown(f"<div style='text-align: center; font-size: 24px;'>{energy_usage['Energy_Source'].nunique()}</div>", unsafe_allow_html=True)

        st.subheader("Energy Source Breakdown (Total Energy Produced)")
        energy_source_energy = energy_usage.groupby('Energy_Source')['Energy_Usage_kWh'].sum().reset_index()
        for idx, row in energy_source_energy.iterrows():
            st.markdown(f"**{row['Energy_Source']}**: {row['Energy_Usage_kWh']:.2f} kWh")

        st.subheader("Energy Source Breakdown (Total Carbon Emissions)")
        energy_source_emissions = energy_usage.groupby('Energy_Source')['Carbon_Emissions_kg_CO2'].sum().reset_index()
        for idx, row in energy_source_emissions.iterrows():
            st.markdown(f"**{row['Energy_Source']}**: {row['Carbon_Emissions_kg_CO2']:.2f} kg CO2")

        st.subheader("Carbon Emissions by Energy Source")
        fig = px.bar(energy_source_emissions, x='Energy_Source', y='Carbon_Emissions_kg_CO2', labels={'Carbon_Emissions_kg_CO2': 'Carbon Emissions (kg CO2)'}, color_discrete_sequence=['#ff7f0e'])
        st.plotly_chart(fig)

        st.subheader("Energy Sources Used")
        energy_sources = energy_usage['Energy_Source'].value_counts().reset_index()
        energy_sources.columns = ['Energy_Source', 'Count']
        fig = px.bar(energy_sources, x='Energy_Source', y='Count', labels={'Count': 'Number of Nodes'}, color_discrete_sequence=['#1f77b4'])
        st.plotly_chart(fig)

        st.subheader("Peak Usage Time")
        peak_usage = energy_usage.groupby('Peak_Usage_Time')['Energy_Usage_kWh'].sum().reset_index()
        fig = px.line(peak_usage, x='Peak_Usage_Time', y='Energy_Usage_kWh', labels={'Energy_Usage_kWh': 'Energy Usage (kWh)'}, color_discrete_sequence=['#2ca02c'])
        st.plotly_chart(fig)

    # Environment Tab
    with tab3:
        st.header("Environment Data")

        # File Upload Option for Environment
        uploaded_environment = st.file_uploader("Upload Environment CSV", type=["csv"], key="environment")
        if uploaded_environment is not None:
            try:
                environment = pd.read_csv(uploaded_environment)
                required_columns = ['Region_Name', 'Disaster_Risk_Level', 'Past_Disruptions']
                if not validate_dataset(environment, required_columns):
                    st.warning("Invalid dataset uploaded. Please ensure the dataset contains the required columns.")
                    environment = pd.read_csv("environment.csv")
            except Exception as e:
                st.warning(f"Invalid dataset uploaded. Error: {e}")
                environment = pd.read_csv("environment.csv")

        # Display the DataFrame
        st.write(environment)

        st.header("Environment Metrics")
        st.subheader("Disaster Risk Level Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown("**Total Disasters**")
        col1.markdown(f"<div style='text-align: center; font-size: 24px;'>{environment['Disaster_Risk_Level'].count()}</div>", unsafe_allow_html=True)
        col2.markdown("**Low Risk Level**")
        col2.markdown(f"<div style='text-align: center; font-size: 24px;'>{environment[environment['Disaster_Risk_Level'] == 'Low'].shape[0]}</div>", unsafe_allow_html=True)
        col3.markdown("**Medium Risk Level**")
        col3.markdown(f"<div style='text-align: center; font-size: 24px;'>{environment[environment['Disaster_Risk_Level'] == 'Medium'].shape[0]}</div>", unsafe_allow_html=True)
        col4.markdown("**High Risk Level**")
        col4.markdown(f"<div style='text-align: center; font-size: 24px;'>{environment[environment['Disaster_Risk_Level'] == 'High'].shape[0]}</div>", unsafe_allow_html=True)

        st.subheader("Total Past Disruptions")
        total_past_disruptions = environment['Past_Disruptions'].sum()
        st.markdown(f"<div style='text-align: center; font-size: 24px;'>{total_past_disruptions}</div>", unsafe_allow_html=True)

        st.subheader("Risk Level by Regions")
        risk_levels = environment.groupby(['Region_Name', 'Disaster_Risk_Level']).size().reset_index(name='Count')
        fig = px.bar(risk_levels, x='Count', y='Region_Name', color='Disaster_Risk_Level', orientation='h',
                    labels={'Count': 'Number of Regions', 'Region_Name': 'Region'},
                    color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c'])
        st.plotly_chart(fig)

    # Procurement Tab
    with tab4:
        st.header("Procurement Data")

        # File Upload Option for Procurement
        uploaded_procurement = st.file_uploader("Upload Procurement CSV", type=["csv"], key="procurement")
        if uploaded_procurement is not None:
            try:
                procurement = pd.read_csv(uploaded_procurement)
                required_columns = ['Equipment_Used', 'Cost_USD', 'Quantity']
                if not validate_dataset(procurement, required_columns):
                    st.warning("Invalid dataset uploaded. Please ensure the dataset contains the required columns.")
                    procurement = pd.read_csv("procurement.csv")
            except Exception as e:
                st.warning(f"Invalid dataset uploaded. Error: {e}")
                procurement = pd.read_csv("procurement.csv")

        # Display the DataFrame
        st.write(procurement)

        st.header("Procurement Metrics")
        st.subheader("Equipment Cost Breakdown")
        equipment_cost = procurement.groupby('Equipment_Used')['Cost_USD'].sum().reset_index()
        for idx, row in equipment_cost.iterrows():
            st.markdown(f"**{row['Equipment_Used']}**: {row['Cost_USD']:.2f} USD")

        st.subheader("Total Cost USD Spent")
        total_cost = procurement['Cost_USD'].sum()
        st.markdown(f"<div style='text-align: center; font-size: 24px;'>{total_cost:.2f} USD</div>", unsafe_allow_html=True)

        st.subheader("Total Equipment Used")
        equipment_quantity = procurement.groupby('Equipment_Used')['Quantity'].sum().reset_index()
        for idx, row in equipment_quantity.iterrows():
            st.markdown(f"**{row['Equipment_Used']}**: {row['Quantity']}")

        st.subheader("Total Equipment Used by Type")
        fig = px.bar(equipment_quantity, x='Equipment_Used', y='Quantity', labels={'Quantity': 'Total Quantity'}, color_discrete_sequence=['#d62728'])
        st.plotly_chart(fig)

        st.subheader("Total Cost Spent by Equipment Type")
        fig = px.bar(equipment_cost, x='Equipment_Used', y='Cost_USD', labels={'Cost_USD': 'Total Cost (USD)'}, color_discrete_sequence=['#9467bd'])
        st.plotly_chart(fig)

    # Traffic Tab
    with tab5:
        st.header("Traffic Data")

        # File Upload Option for Traffic
        uploaded_traffic = st.file_uploader("Upload Traffic CSV", type=["csv"], key="traffic")
        if uploaded_traffic is not None:
            try:
                traffic = pd.read_csv(uploaded_traffic)
                required_columns = ['Node_ID', 'Date', 'Time', 'Data_Usage_GB', 'Peak_Usage_GB']
                if not validate_dataset(traffic, required_columns):
                    st.warning("Invalid dataset uploaded. Please ensure the dataset contains the required columns.")
                    traffic = pd.read_csv("traffic.csv")
            except Exception as e:
                st.warning(f"Invalid dataset uploaded. Error: {e}")
                traffic = pd.read_csv("traffic.csv")

        # Display the DataFrame
        st.write(traffic)

        st.header("Traffic Metrics")
        st.subheader("Traffic Metrics")
        st.markdown("**Total Data Usage (GB)**")
        st.markdown(f"<div style='text-align: center; font-size: 24px;'>{traffic['Data_Usage_GB'].sum()}</div>", unsafe_allow_html=True)
        st.markdown("**Total Peak Usage (GB)**")
        st.markdown(f"<div style='text-align: center; font-size: 24px;'>{traffic['Peak_Usage_GB'].sum()}</div>", unsafe_allow_html=True)
        st.markdown("**Highest Data Usage Node ID**")
        st.markdown(f"<div style='text-align: center; font-size: 24px;'>{traffic.loc[traffic['Data_Usage_GB'].idxmax(), 'Node_ID']}</div>", unsafe_allow_html=True)
        st.markdown("**Highest Peak Usage Node ID**")
        st.markdown(f"<div style='text-align: center; font-size: 24px;'>{traffic.loc[traffic['Peak_Usage_GB'].idxmax(), 'Node_ID']}</div>", unsafe_allow_html=True)

        traffic['DateTime'] = pd.to_datetime(traffic['Date'] + ' ' + traffic['Time'])

        st.subheader("Data Usage Over Time (Area Chart)")
        fig_data_usage = px.area(traffic, x='DateTime', y='Data_Usage_GB', labels={'Data_Usage_GB': 'Data Usage (GB)'}, color_discrete_sequence=['#1f77b4'])
        fig_data_usage.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_data_usage, use_container_width=True)

        st.subheader("Peak Usage Over Time (Area Chart)")
        fig_peak_usage = px.area(traffic, x='DateTime', y='Peak_Usage_GB', labels={'Peak_Usage_GB': 'Peak Usage (GB)'}, color_discrete_sequence=['#ff7f0e'])
        fig_peak_usage.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_peak_usage, use_container_width=True)

# Settings Page
def settings_page():
    st.title("Settings")
    if st.session_state.user_id is not None:
        user_info = fetch_user_info(st.session_state.user_id)
        if user_info:
            full_name = st.text_input("Full Name:", value=user_info[0])
            username = st.text_input("Username:", value=user_info[1])
            password = st.text_input("Password:", type="password", value=user_info[2])
            avatar = st.file_uploader("Upload Avatar Image:", type=["jpg", "jpeg", "png"])
            
            if st.button("Update Information"):
                if avatar is not None:
                    avatar_bytes = avatar.read()
                    update_user_info(st.session_state.user_id, full_name, username, password, avatar_bytes)
                    st.session_state.avatar = avatar_bytes
                else:
                    update_user_info(st.session_state.user_id, full_name, username, password, None)
                st.success("Information updated successfully!")
        else:
            st.write("No user information found.")
    else:
        st.warning("You need to log in to view this page.")

# AI Tool 1: Energy & CO₂ Optimizer
def energy_co2_optimizer():
    st.title("Energy Optimization & Carbon Emissions Tracker")
    st.write("This tool predicts energy usage and carbon emissions based on input parameters.")

    # Load ML models
    energy_model_path = 'energy_usage_model.pkl'
    carbon_model_path = 'carbon_emissions_model.pkl'
    energy_model = joblib.load(energy_model_path)
    carbon_model = joblib.load(carbon_model_path)

    # Function to collect user input
    def collect_user_input():
        st.subheader("Provide Input for Prediction")
        user_input = {}
        
        user_input['Node_ID'] = st.text_input("Enter Node ID:")
        start_date = st.date_input("Enter Start Date (YYYY-MM-DD):")
        end_date = st.date_input("Enter End Date (YYYY-MM-DD):")
        user_input['Population_Served'] = st.number_input("Enter Population Served:", min_value=1)
        user_input['Region'] = st.text_input("Enter Region:").lower()
        
        # Energy Source with "Other" option
        energy_source_options = ["Grid", "Solar", "Generator", "Other"]
        energy_source = st.selectbox("Select the Energy Source:", energy_source_options)
        if energy_source == "Other":
            energy_source = st.text_input("Enter the Energy Source manually:")
        user_input['Energy_Source'] = energy_source
        
        peak_usage = st.selectbox("Select the Peak Usage Time:", ["Morning", "Afternoon", "Evening", "Night"])
        user_input['Peak_Usage_Time'] = peak_usage
        
        # Type with "Other" option
        type_options = ["Government Office", "Health Center", "School", "Other"]
        type_input = st.selectbox("Select the Type:", type_options)
        if type_input == "Other":
            type_input = st.text_input("Enter the Type manually:")
        user_input['Type'] = type_input
        
        infrastructure_input = st.radio("Existing Infrastructure:", ["Yes", "No"])
        user_input['Existing_Infrastructure'] = infrastructure_input
        
        return user_input, start_date, end_date

    # Function to predict energy and carbon emissions
    def predict_energy_and_carbon(input_data, start_date, end_date):
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        predictions = []
        
        for date in date_range:
            month = date.month
            day = date.day
            
            input_df = pd.DataFrame([input_data])
            input_df['Month'] = month
            input_df['Day'] = day
            
            for col in energy_model.feature_names_in_:
                if col not in input_df.columns:
                    input_df[col] = 0
            
            input_df.columns = input_df.columns.astype(str)
            input_df = input_df[energy_model.feature_names_in_]
            
            energy_pred = energy_model.predict(input_df)
            carbon_pred = carbon_model.predict(input_df)
            
            predictions.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Energy_Usage_kWh': energy_pred[0],
                'Carbon_Emissions_kg_CO2': carbon_pred[0]
            })
        
        predictions_df = pd.DataFrame(predictions)
        return predictions_df

    # Function to get Gemini AI insights
    def get_gemini_insights(user_input, predictions_df):
        input_text = f"""
        User Input:
        {user_input}

        Predicted Data:
        {predictions_df.to_string(index=False)}

        Analyze the above data and provide insights, suggestions, and notes for energy optimization and carbon emissions reduction. 
        Format your response in the following structure:
        - **Insights**: List key observations from the data in short, concise bullet points.
        - **Suggestions**: Provide actionable suggestions in short, concise bullet points.
        - **Notes**: Add any additional notes or considerations in short, concise bullet points.
        """
        
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            n=1,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in energy optimization and carbon emissions reduction. Your goal is to analyze the provided data and provide actionable insights, suggestions, and notes to optimize energy usage and reduce carbon emissions."
                },
                {
                    "role": "user",
                    "content": input_text
                }
            ]
        )
        
        return response.choices[0].message.content

    # Function to save session data
    def save_session(user_id, input_data, predictions, insights):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO sessions1 (user_id, input_data, predictions, insights, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, str(input_data), predictions.to_json(), insights, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch session data
    def fetch_sessions(user_id):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM sessions1 WHERE user_id = ?''', (user_id,))
        sessions = c.fetchall()
        conn.close()
        return sessions

    # Function to save a ticket
    def save_ticket(user_id, username, full_name, ticket_text):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO tickets1 (user_id, username, full_name, ticket_text, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, username, full_name, ticket_text, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch all tickets
    def fetch_tickets():
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM tickets1 ORDER BY timestamp DESC''')
        tickets = c.fetchall()
        conn.close()
        return tickets
    
    # Tabs for AI Tool, Session, and Ticket
    tab1, tab2, tab3 = st.tabs(["AI Tool", "Session", "Ticket"])
            
    with tab1:
        st.header("AI Tool")
        user_input, start_date, end_date = collect_user_input()
        if st.button("Predict"):
            predictions_df = predict_energy_and_carbon(user_input, start_date, end_date)
                    
            # Display predictions as a DataFrame
            st.write("Prediction Results:")
            st.dataframe(predictions_df)
                    
            insights = get_gemini_insights(user_input, predictions_df)
            st.write("Gemini AI Insights, Suggestions, and Notes:")
            st.write(insights)
                    
            save_session(st.session_state.user_id, user_input, predictions_df, insights)
            st.success("Session saved successfully!")
            
    with tab2:
        st.header("Session")
        sessions = fetch_sessions(st.session_state.user_id)
        if sessions:
            for session in sessions:
                # Use expander for each session
                with st.expander(f"Session ID: {session[0]} - {session[5]}"):
                    st.write(f"Timestamp: {session[5]}")
                    st.write("Input Data:")
                            
                    # Convert input data from string to dictionary
                    input_data = eval(session[2])
                            
                    # Display input data as bullet points
                    st.markdown("- **Node ID:** " + str(input_data.get('Node_ID', 'N/A')))
                    st.markdown("- **Population Served:** " + str(input_data.get('Population_Served', 'N/A')))
                    st.markdown("- **Region:** " + str(input_data.get('Region', 'N/A')))
                    st.markdown("- **Energy Source:** " + str(input_data.get('Energy_Source', 'N/A')))
                    st.markdown("- **Peak Usage Time:** " + str(input_data.get('Peak_Usage_Time', 'N/A')))
                    st.markdown("- **Type:** " + str(input_data.get('Type', 'N/A')))
                    st.markdown("- **Existing Infrastructure:** " + str(input_data.get('Existing_Infrastructure', 'N/A')))
                            
                    st.write("Predictions:")
                    # Convert JSON predictions back to DataFrame
                    predictions_df = pd.read_json(session[3])
                    st.dataframe(predictions_df)
                    st.write("Insights:")
                    st.write(session[4])
                            
                    # Download session data as .txt
                    session_data = f"Input Data:\n{session[2]}\n\nPredictions:\n{predictions_df.to_string(index=False)}\n\nInsights:\n{session[4]}"
                    st.download_button(
                        label=f"Download Session {session[0]}",
                        data=session_data,
                        file_name=f"tech_{st.session_state.user_id}_energy_carbon_tracker{session[0]}.txt",
                                mime="text/plain"
                    )
        else:
            st.write("No sessions found.")
            
    with tab3:
        st.header("Ticket")
        st.write("Submit a ticket to report an issue or provide feedback.")
                
        # Ticket submission form
        ticket_text = st.text_area("Describe the issue or feedback:")
        if st.button("Submit Ticket"):
            if ticket_text.strip():
                save_ticket(st.session_state.user_id, st.session_state.username, st.session_state.full_name, ticket_text)
                st.success("Ticket submitted successfully!")
            else:
                st.error("Please enter a description for the ticket.")
                
        # Display all tickets
        st.write("### All Tickets")
        tickets = fetch_tickets()
        if tickets:
            for ticket in tickets:
                st.write(f"**Ticket ID:** {ticket[0]}")
                st.write(f"**Submitted by:** {ticket[3]} (Username: {ticket[2]}, User ID: {ticket[1]})")
                st.write(f"**Timestamp:** {ticket[5]}")
                st.write(f"**Description:** {ticket[4]}")
                st.write("---")
        else:
            st.write("No tickets found.")
        
# AI Tool 2: Maintenance Forecaster
def maintenance_forecaster():
    st.title("Predictive Maintenance System")

    # Load the pre-trained model and data
    model_path = 'maintenance_model.pkl'
    model = joblib.load(model_path)

    merged_data_path = 'maintenance_merged_data.csv'
    merged_data = pd.read_csv(merged_data_path)

    # Preprocess the merged dataset
    merged_data = merged_data.drop(columns=['Log_ID', 'Technician_ID', 'Latitude', 'Longitude'])
    type_mapping = {'Government Office': 1, 'Health Center': 2, 'School': 3}
    merged_data['Type'] = merged_data['Type'].map(type_mapping)
    connectivity_mapping = {'Connected': 1, 'Unconnected': 2}
    merged_data['Connectivity_Status'] = merged_data['Connectivity_Status'].map(connectivity_mapping)
    infrastructure_mapping = {'Yes': 1, 'No': 2}
    merged_data['Existing_Infrastructure'] = merged_data['Existing_Infrastructure'].map(infrastructure_mapping)
    merged_data['Node_ID'] = merged_data['Node_ID'].str.extract('(\d+)').astype(int)
    merged_data = pd.get_dummies(merged_data, columns=['Region'], drop_first=True)
    training_columns = merged_data.drop(columns=['Issue_Type']).columns

    # Function to predict issue occurrence
    def predict_issue_occurrence(input_data):
        prediction = model.predict(input_data)
        return prediction[0]

    # Function to get Gemini AI insights
    def get_gemini_insights(user_input, prediction):
        input_text = f"""
        User Input:
        {user_input}

        Predicted Issue Type:
        {prediction}

        Analyze the above data and provide insights, suggestions, and notes for predictive maintenance.
        Format your response in the following structure:
        - **Insights**: List key observations from the data in short, concise bullet points.
        - **Suggestions**: Provide actionable suggestions in short, concise bullet points.
        - **Notes**: Add any additional notes or considerations in short, concise bullet points.
        """
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            n=1,
            messages=[
                {"role": "system", "content": "You are a predictive maintenance expert. Your task is to provide concise, actionable insights and recommendations in a structured format."},
                {"role": "user", "content": input_text}
            ]
        )
        return response.choices[0].message.content

    # Function to save session data
    def save_session(user_id, input_data, prediction, insights):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO sessions2 (user_id, input_data, prediction, insights, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, str(input_data), str(prediction), insights, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch session data
    def fetch_sessions(user_id):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM sessions2 WHERE user_id = ?''', (user_id,))
        sessions = c.fetchall()
        conn.close()
        return sessions

    # Function to save a ticket
    def save_ticket(user_id, username, full_name, ticket_text):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO tickets2 (user_id, username, full_name, ticket_text, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, username, full_name, ticket_text, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch all tickets
    def fetch_tickets():
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM tickets2 ORDER BY timestamp DESC''')
        tickets = c.fetchall()
        conn.close()
        return tickets
    
    # Tabs for AI Tool, Session, and Ticket
    tab1, tab2, tab3 = st.tabs(["AI Tool", "Session", "Ticket"])
            
    with tab1:
        st.header("AI Tool")
        st.write("Please enter the following details:")

        # Input fields
        node_id = st.text_input("Node ID (e.g., Node_1, Node_2, etc.):")
        type_options = {"Government Office": 1, "Health Center": 2, "School": 3, "Other": 4}
        type_input = st.selectbox("Type", list(type_options.keys()))
        if type_input == "Other":
            type_input = st.text_input("Enter the Type manually:")
            type_value = 4  # Assign a unique value for "Other"
        else:
            type_value = type_options[type_input]
        region = st.text_input("Region:").lower()
        population_served = st.number_input("Population Served:", min_value=0)
        connectivity_status = st.selectbox("Connectivity Status", ["Connected", "Unconnected"])
        existing_infrastructure = st.selectbox("Existing Infrastructure", ["Yes", "No"])
        resolution_time_hours = st.number_input("Resolution Time (Hours):", min_value=0.0)

        if st.button("Predict"):
            # Preprocess input data
            input_data = pd.DataFrame({
                'Node_ID': [int(node_id.split('_')[1])],
                'Type': [type_value],
                'Region': [region],
                'Population_Served': [population_served],
                'Connectivity_Status': [1 if connectivity_status == "Connected" else 2],
                'Existing_Infrastructure': [1 if existing_infrastructure == "Yes" else 2],
                'Resolution_Time_Hours': [resolution_time_hours]
            })
            input_data = pd.get_dummies(input_data, columns=['Region'], drop_first=True)
            input_data = input_data.reindex(columns=training_columns, fill_value=0)

            # Predict
            prediction = predict_issue_occurrence(input_data)
            st.write(f"Predicted Issue Type: {prediction}")

            # Get Gemini insights
            user_input = {
                'Node_ID': node_id,
                'Type': type_input,
                'Region': region,
                'Population_Served': population_served,
                'Connectivity_Status': connectivity_status,
                'Existing_Infrastructure': existing_infrastructure,
                'Resolution_Time_Hours': resolution_time_hours
            }
            insights = get_gemini_insights(user_input, prediction)
            st.write("Gemini AI Insights and Recommendations:")
            st.write(insights)

            # Save session to database
            save_session(st.session_state.user_id, user_input, prediction, insights)
            st.success("Session saved successfully!")
        
    with tab2:
        st.header("Session")
        sessions = fetch_sessions(st.session_state.user_id)
        if sessions:
            for session in sessions:
                # Use expander for each session
                with st.expander(f"Session ID: {session[0]} - {session[5]}"):
                    st.write(f"Timestamp: {session[5]}")
                    st.write("Input Data:")
                        
                    # Convert input data from string to dictionary
                    input_data = eval(session[2])
                    
                    # Display input data as bullet points
                    st.markdown("- **Node ID:** " + str(input_data.get('Node_ID', 'N/A')))
                    st.markdown("- **Type:** " + str(input_data.get('Type', 'N/A')))
                    st.markdown("- **Region:** " + str(input_data.get('Region', 'N/A')))
                    st.markdown("- **Population Served:** " + str(input_data.get('Population_Served', 'N/A')))
                    st.markdown("- **Connectivity Status:** " + str(input_data.get('Connectivity_Status', 'N/A')))
                    st.markdown("- **Existing Infrastructure:** " + str(input_data.get('Existing_Infrastructure', 'N/A')))
                    st.markdown("- **Resolution Time (Hours):** " + str(input_data.get('Resolution_Time_Hours', 'N/A')))
                    
                    st.write("Prediction:")
                    st.write(session[3])
                    st.write("Insights:")
                    st.write(session[4])
                    
                    # Download session data as .txt
                    session_data = f"Input Data:\n{session[2]}\n\nPrediction:\n{session[3]}\n\nInsights:\n{session[4]}"
                    st.download_button(
                        label=f"Download Session {session[0]}",
                        data=session_data,
                        file_name=f"tech_{st.session_state.user_id}_predictive_maintenance_{session[0]}.txt",
                        mime="text/plain"
                    )
        else:
            st.write("No sessions found.")
            
    with tab3:
        st.header("Ticket")
        st.write("Submit a ticket to report an issue or provide feedback.")
        
        # Ticket submission form
        ticket_text = st.text_area("Describe the issue or feedback:")
        if st.button("Submit Ticket"):
            if ticket_text.strip():
                save_ticket(st.session_state.user_id, st.session_state.username, st.session_state.full_name, ticket_text)
                st.success("Ticket submitted successfully!")
            else:
                st.error("Please enter a description for the ticket.")
            
        # Display all tickets
        st.write("### All Tickets")
        tickets = fetch_tickets()
        if tickets:
            for ticket in tickets:
                st.write(f"**Ticket ID:** {ticket[0]}")
                st.write(f"**Submitted by:** {ticket[3]} (Username: {ticket[2]}, User ID: {ticket[1]})")
                st.write(f"**Timestamp:** {ticket[5]}")
                st.write(f"**Description:** {ticket[4]}")
                st.write("---")
        else:
            st.write("No tickets found.")

# AI Tool 3: Disaster Assessor
def disaster_assessor():
    st.title("Disaster Risk Assessment")

    # Load ML models and encoders
    model_path = 'environment_automl_model.pkl'
    label_encoder_path = 'label_encoder.pkl'
    onehot_encoder_path = 'onehot_encoder.pkl'
    model = joblib.load(model_path)
    label_encoder = joblib.load(label_encoder_path)
    onehot_encoder = joblib.load(onehot_encoder_path)

    # Function to collect user input
    def collect_user_input():
        st.subheader("Provide Input for Disaster Risk Assessment")
        user_input = {}
        
        user_input['Region'] = st.text_input("Enter Region:").strip().lower()
        user_input['Temperature_C'] = st.number_input("Enter Temperature (in Celsius):", value=25.0)
        user_input['Humidity_Percent'] = st.number_input("Enter Humidity (in Percent):", value=60.0)
        user_input['Past_Disruptions'] = st.number_input("Enter the number of Past Disruptions:", value=0)
        user_input['Population_Served'] = st.number_input("Enter Population Served:", value=1000)
        
        user_input['Connectivity_Status'] = st.selectbox("Select the Connectivity Status:", ["Connected", "Unconnected"])
        user_input['Existing_Infrastructure'] = st.selectbox("Select the Existing Infrastructure:", ["Yes", "No"])
        # Type with "Other" option
        type_options = ["Government Office", "Health Center", "School", "Other"]
        type_input = st.selectbox("Select the Type:", type_options)
        if type_input == "Other":
            type_input = st.text_input("Enter the Type manually:")
        user_input['Type'] = type_input
        
        return user_input

    # Function to predict disaster risk level
    def predict_risk_level(input_data, model, label_encoder, onehot_encoder):
        input_df = pd.DataFrame([input_data])
        categorical_columns = ['Region', 'Type', 'Connectivity_Status', 'Existing_Infrastructure']
        encoded_features = onehot_encoder.transform(input_df[categorical_columns])
        encoded_features_df = pd.DataFrame(encoded_features, columns=onehot_encoder.get_feature_names_out(categorical_columns))
        input_df = pd.concat([input_df.drop(columns=categorical_columns), encoded_features_df], axis=1)
        risk_level_encoded = model.predict(input_df)
        risk_level = label_encoder.inverse_transform(risk_level_encoded)
        return risk_level[0]

    # Function to get Gemini AI insights
    def get_gemini_insights(user_input, risk_level):
        input_text = f"""
        User Input:
        - Region: {user_input['Region']}
        - Temperature: {user_input['Temperature_C']}°C
        - Humidity: {user_input['Humidity_Percent']}%
        - Past Disruptions: {user_input['Past_Disruptions']}
        - Population Served: {user_input['Population_Served']}
        - Connectivity Status: {user_input['Connectivity_Status']}
        - Existing Infrastructure: {user_input['Existing_Infrastructure']}
        - Organization Type: {user_input['Type']}

        Predicted Disaster Risk Level: {risk_level}

        Analyze the above data and provide insights, suggestions, and notes for disaster risk mitigation.
        Format your response in the following structure:
        - **Insights**: List key observations from the data in short, concise bullet points.
        - **Suggestions**: Provide actionable suggestions for reducing disaster risk in short, concise bullet points.
        - **Notes**: Add any additional notes or considerations in short, concise bullet points.
        """
        
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": "You are a disaster risk assessment expert. Provide insights, suggestions, and notes in concise, structured bullet points. Focus on actionable steps and make the output easy to read."},
                {"role": "user", "content": input_text}
            ]
        )
        
        return response.choices[0].message.content

    # Function to save session data
    def save_session(user_id, input_data, predictions, insights):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO sessions3 (user_id, input_data, predictions, insights, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, str(input_data), predictions, insights, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch session data
    def fetch_sessions(user_id):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM sessions3 WHERE user_id = ?''', (user_id,))
        sessions = c.fetchall()
        conn.close()
        return sessions

    # Function to save a ticket
    def save_ticket(user_id, username, full_name, ticket_text):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO tickets3 (user_id, username, full_name, ticket_text, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, username, full_name, ticket_text, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch all tickets
    def fetch_tickets():
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM tickets3 ORDER BY timestamp DESC''')
        tickets = c.fetchall()
        conn.close()
        return tickets

    # Tabs for AI Tool, Session, and Ticket
    tab1, tab2, tab3 = st.tabs(["AI Tool", "Session", "Ticket"])
            
    with tab1:
        st.header("AI Tool")
        user_input = collect_user_input()
        if st.button("Predict"):
            risk_level = predict_risk_level(user_input, model, label_encoder, onehot_encoder)
            st.write(f"**Predicted Disaster Risk Level:** {risk_level}")
                    
            insights = get_gemini_insights(user_input, risk_level)
            st.write("**Gemini AI Insights, Suggestions, and Notes:**")
            st.write(insights)
                    
            save_session(st.session_state.user_id, user_input, risk_level, insights)
            st.success("Session saved successfully!")
            
    with tab2:
        st.header("Session")
        sessions = fetch_sessions(st.session_state.user_id)
        if sessions:
            for session in sessions:
                with st.expander(f"Session ID: {session[0]} - {session[5]}"):
                    st.write(f"Timestamp: {session[5]}")
                    st.write("Input Data:")
                        
                    # Convert input data from string to dictionary
                    input_data = eval(session[2])
                            
                    # Display input data as bullet points
                    st.markdown("- **Region:** " + str(input_data.get('Region', 'N/A')))
                    st.markdown("- **Temperature:** " + str(input_data.get('Temperature_C', 'N/A')) + "°C")
                    st.markdown("- **Humidity:** " + str(input_data.get('Humidity_Percent', 'N/A')) + "%")
                    st.markdown("- **Past Disruptions:** " + str(input_data.get('Past_Disruptions', 'N/A')))
                    st.markdown("- **Population Served:** " + str(input_data.get('Population_Served', 'N/A')))
                    st.markdown("- **Connectivity Status:** " + str(input_data.get('Connectivity_Status', 'N/A')))
                    st.markdown("- **Existing Infrastructure:** " + str(input_data.get('Existing_Infrastructure', 'N/A')))
                    st.markdown("- **Organization Type:** " + str(input_data.get('Type', 'N/A')))
                    
                    st.write("Prediction:")
                    st.write(session[3])
                    st.write("Insights:")
                    st.write(session[4])
                        
                    # Download session data as .txt
                    session_data = f"Input Data:\n{input_data}\n\nPrediction:\n{session[3]}\n\nInsights:\n{session[4]}"
                    st.download_button(
                    label=f"Download Session {session[0]}",
                        data=session_data,
                        file_name=f"tech_{st.session_state.user_id}_disaster_risk_assessment_{session[0]}.txt",
                        mime="text/plain"
                    )
        else:
            st.write("No sessions found.")
    
    with tab3:
        st.header("Ticket")
        ticket_text = st.text_area("Describe the issue or feedback:")
        if st.button("Submit Ticket"):
            if ticket_text.strip():
                save_ticket(st.session_state.user_id, st.session_state.username, st.session_state.full_name, ticket_text)
                st.success("Ticket submitted successfully!")
            else:
                st.error("Please enter a description for the ticket.")
            
        st.write("### All Tickets")
        tickets = fetch_tickets()
        if tickets:
            for ticket in tickets:
                st.write(f"**Ticket ID:** {ticket[0]}")
                st.write(f"**Submitted by:** {ticket[3]} (Username: {ticket[2]}, User ID: {ticket[1]})")
                st.write(f"**Timestamp:** {ticket[5]}")
                st.write(f"**Description:** {ticket[4]}")
                st.write("---")
        else:
            st.write("No tickets found.")

# AI Tool 4: Traffic Forecaster
def traffic_forecaster():
    st.title("Traffic Load Prediction Tool")

    # Load the pre-trained models
    data_usage_model_path = 'data_usage_regression_model2.pkl'
    peak_usage_model_path = 'peak_usage_regression_model2.pkl'

    data_usage_model = joblib.load(data_usage_model_path)
    peak_usage_model = joblib.load(peak_usage_model_path)

    # Function to predict data and peak usage
    def predict_data_and_peak_usage(input_data, start_date, end_date):
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        predictions = []
        
        for date in date_range:
            year = date.year
            month = date.month
            day = date.day
            
            input_df = pd.DataFrame([input_data])
            input_df['Year'] = year
            input_df['Month'] = month
            input_df['Day'] = day
            input_df['Hour'] = 0
            
            categorical_columns = ['Type', 'Region', 'Connectivity_Status', 'Existing_Infrastructure']
            for col in categorical_columns:
                if col not in input_df.columns:
                    input_df[col] = 0
            
            input_df = pd.get_dummies(input_df, columns=categorical_columns, drop_first=True)
            
            for col in data_usage_model.feature_names_in_:
                if col not in input_df.columns:
                    input_df[col] = 0
            
            input_df = input_df[data_usage_model.feature_names_in_]
            
            data_usage_pred = data_usage_model.predict(input_df)
            peak_usage_pred = peak_usage_model.predict(input_df)
            
            predictions.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Data_Usage_GB': data_usage_pred[0],
                'Peak_Usage_GB': peak_usage_pred[0]
            })
        
        predictions_df = pd.DataFrame(predictions)
        return predictions_df

    # Function to get Gemini AI insights
    def get_gemini_insights(user_input, predictions_df):
        input_text = f"""
        **User Input:**
        {user_input}

        **Predicted Data:**
        {predictions_df.to_string(index=False)}

        **Task:**
        Analyze the user input and predicted data, then provide detailed insights, recommendations, and strategies for optimizing traffic load and infrastructure. 
        Format your response in the following structure:

        - **Insights**: List key observations from the data in short, concise bullet points.
        - **Recommendations**: Provide high-level recommendations to address the observed issues or opportunities.
        - **Suggestions**: Offer actionable suggestions in short, concise bullet points.
        - **Notes**: Add any additional notes or considerations in short, concise bullet points.

        **Guidelines:**
        1. Be concise and avoid lengthy explanations.
        2. Use bold bullet points for each section.
        3. Focus on actionable and practical insights.
        4. Highlight critical areas that require immediate attention.
        """

        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            n=1,
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in traffic load optimization and infrastructure planning. Provide insights and recommendations in a structured, concise, and actionable format."},
                {"role": "user", "content": input_text}
            ]
        )
        
        return response.choices[0].message.content

    # Function to save session data
    def save_session(user_id, input_data, prediction, insights):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO sessions4 (user_id, input_data, prediction, insights, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, str(input_data), str(prediction), insights, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch session data
    def fetch_sessions(user_id):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM sessions4 WHERE user_id = ?''', (user_id,))
        sessions = c.fetchall()
        conn.close()
        return sessions

    # Function to save a ticket
    def save_ticket(user_id, username, full_name, ticket_text):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO tickets4 (user_id, username, full_name, ticket_text, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, username, full_name, ticket_text, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch all tickets
    def fetch_tickets():
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM tickets4 ORDER BY timestamp DESC''')
        tickets = c.fetchall()
        conn.close()
        return tickets

    # Tabs for AI Tool, Session, and Ticket
    tab1, tab2, tab3 = st.tabs(["AI Tool", "Session", "Ticket"])
            
    with tab1:
        st.header("AI Tool")
        st.write("Please enter the following details:")

        # Input fields
        node_id = st.text_input("Node ID (e.g., Node_1, Node_2, etc.):")
        type_options = {"Government Office": 1, "Health Center": 2, "School": 3, "Other": 4}
        type_input = st.selectbox("Type", list(type_options.keys()))
        if type_input == "Other":
            type_input = st.text_input("Enter the Type manually:")
            type_value = 4  # Assign a unique value for "Other"
        else:
            type_value = type_options[type_input]
        region = st.text_input("Region:").lower()
        population_served = st.number_input("Population Served:", min_value=0)
        connectivity_status = st.selectbox("Connectivity Status", ["Connected", "Unconnected"])
        existing_infrastructure = st.selectbox("Existing Infrastructure", ["Yes", "No"])
        start_date = st.date_input("Start Date:")
        end_date = st.date_input("End Date:")

        if st.button("Predict"):
            # Preprocess input data
            input_data = {
                'Node_ID': node_id,
                'Type': type_value,
                'Region': region,
                'Population_Served': population_served,
                'Connectivity_Status': connectivity_status,
                'Existing_Infrastructure': existing_infrastructure
            }

            # Predict
            predictions_df = predict_data_and_peak_usage(input_data, start_date, end_date)
            st.write("Predicted Data Usage and Peak Usage:")
            st.write(predictions_df)

            # Get Gemini insights
            insights = get_gemini_insights(input_data, predictions_df)
            st.write("Gemini AI Insights and Recommendations:")
            st.write(insights)

            # Save session to database
            save_session(st.session_state.user_id, input_data, predictions_df.to_string(), insights)
            st.success("Session saved successfully!")
            
    with tab2:
        st.header("Session")
        sessions = fetch_sessions(st.session_state.user_id)
        if sessions:
            for session in sessions:
                # Use expander for each session
                with st.expander(f"Session ID: {session[0]} - {session[5]}"):
                    st.write(f"Timestamp: {session[5]}")
                    st.write("Input Data:")
                            
                    # Convert input data from string to dictionary
                    input_data = eval(session[2])
                            
                    # Display input data as bullet points
                    st.markdown("- **Node ID:** " + str(input_data.get('Node_ID', 'N/A')))
                    st.markdown("- **Type:** " + str(input_data.get('Type', 'N/A')))
                    st.markdown("- **Region:** " + str(input_data.get('Region', 'N/A')))
                    st.markdown("- **Population Served:** " + str(input_data.get('Population_Served', 'N/A')))
                    st.markdown("- **Connectivity Status:** " + str(input_data.get('Connectivity_Status', 'N/A')))
                    st.markdown("- **Existing Infrastructure:** " + str(input_data.get('Existing_Infrastructure', 'N/A')))
                            
                    st.write("Prediction:")
                    st.write(session[3])
                    st.write("Insights:")
                    st.write(session[4])
                            
                    # Download session data as .txt
                    session_data = f"Input Data:\n{session[2]}\n\nPrediction:\n{session[3]}\n\nInsights:\n{session[4]}"
                    st.download_button(
                        label=f"Download Session {session[0]}",
                        data=session_data,
                        file_name=f"tech_{st.session_state.user_id}_traffic_load_prediction_{session[0]}.txt",
                        mime="text/plain"
                    )
        else:
            st.write("No sessions found.")
            
    with tab3:
        st.header("Ticket")
        st.write("Submit a ticket to report an issue or provide feedback.")
                
        # Ticket submission form
        ticket_text = st.text_area("Describe the issue or feedback:")
        if st.button("Submit Ticket"):
            if ticket_text.strip():
                save_ticket(st.session_state.user_id, st.session_state.username, st.session_state.full_name, ticket_text)
                st.success("Ticket submitted successfully!")
            else:
                st.error("Please enter a description for the ticket.")
                
        # Display all tickets
        st.write("### All Tickets")
        tickets = fetch_tickets()
        if tickets:
            for ticket in tickets:
                st.write(f"**Ticket ID:** {ticket[0]}")
                st.write(f"**Submitted by:** {ticket[3]} (Username: {ticket[2]}, User ID: {ticket[1]})")
                st.write(f"**Timestamp:** {ticket[5]}")
                st.write(f"**Description:** {ticket[4]}")
                st.write("---")
        else:
            st.write("No tickets found.")

# AI Tool 5: Procurement Planner
def procurement_planner():
    st.title("Procurement Optimization")

    # Load the pre-trained models
    cost_model_path = 'cost_prediction_model2.pkl'
    time_model_path = 'time_prediction_model2.pkl'
    quantity_model_path = 'quantity_prediction_model2.pkl'

    cost_model = joblib.load(cost_model_path)
    time_model = joblib.load(time_model_path)
    quantity_model = joblib.load(quantity_model_path)

    # Load the merged dataset to get the feature columns
    merged_data_path = 'procurement_merged_data.csv'
    data = pd.read_csv(merged_data_path)

    # Preprocess the merged dataset
    data = data.drop(columns=['Deployment_ID', 'Node_ID', 'Latitude', 'Longitude', 'Vendor_Details', 'Cost_USD', 'Time_Taken_Days', 'Quantity'])
    type_mapping = {'Government Office': 1, 'Health Center': 2, 'School': 3}
    data['Type'] = data['Type'].map(type_mapping)
    connectivity_mapping = {'Connected': 1, 'Unconnected': 2}
    data['Connectivity_Status'] = data['Connectivity_Status'].map(connectivity_mapping)
    infrastructure_mapping = {'Yes': 1, 'No': 2}
    data['Existing_Infrastructure'] = data['Existing_Infrastructure'].map(infrastructure_mapping)
    data = pd.get_dummies(data, columns=['Region', 'Equipment_Used'], drop_first=True)
    training_columns = data.columns

    # Function to predict cost, time, and quantity
    def predict_cost_time_and_quantity(input_data):
        input_df = pd.DataFrame([input_data])
        for col in training_columns:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[training_columns]
        cost_pred = cost_model.predict(input_df)
        time_pred = time_model.predict(input_df)
        quantity_pred = quantity_model.predict(input_df)
        return float(cost_pred[0]), float(time_pred[0]), int(quantity_pred[0])

    # Function to get Gemini AI insights
    def get_gemini_insights(user_input, cost_pred, time_pred, quantity_pred):
        input_text = f"""
        User Input:
        {user_input}

        Predicted Cost (USD): {cost_pred:.2f}
        Predicted Delivery Time (Days): {time_pred:.2f}
        Predicted Quantity (Units): {quantity_pred}

        Analyze the above data and provide insights, suggestions, and notes for procurement optimization.
        Format your response in the following structure:
        - **Insights**: List key observations from the data in short, concise bullet points.
        - **Suggestions**: Provide actionable suggestions in short, concise bullet points.
        - **Notes**: Add any additional notes or considerations in short, concise bullet points.
        """
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            n=1,
            messages=[
                {"role": "system", "content": "You are a procurement optimization expert. Your task is to provide concise, actionable insights and recommendations in a structured format."},
                {"role": "user", "content": input_text}
            ]
        )
        return response.choices[0].message.content

    # Function to save session data
    def save_session(user_id, input_data, cost_pred, time_pred, quantity_pred, insights):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO sessions5 (user_id, input_data, cost_prediction, time_prediction, quantity_prediction, insights, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                (user_id, str(input_data), float(cost_pred), float(time_pred), int(quantity_pred), insights, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch session data
    def fetch_sessions(user_id):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM sessions5 WHERE user_id = ?''', (user_id,))
        sessions = c.fetchall()
        conn.close()
        
        # Ensure proper deserialization of predictions
        processed_sessions = []
        for session in sessions:
            session_id, user_id, input_data, cost_pred, time_pred, quantity_pred, insights, timestamp = session
            
            # Convert predictions to float/int if they are bytes
            if isinstance(cost_pred, bytes):
                cost_pred = float(cost_pred.decode('utf-8'))
            if isinstance(time_pred, bytes):
                time_pred = float(time_pred.decode('utf-8'))
            if isinstance(quantity_pred, bytes):
                quantity_pred = int(quantity_pred.decode('utf-8'))
            
            processed_sessions.append((
                session_id, user_id, input_data, cost_pred, time_pred, quantity_pred, insights, timestamp
            ))
        
        return processed_sessions

    # Function to save a ticket
    def save_ticket(user_id, username, full_name, ticket_text):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO tickets5 (user_id, username, full_name, ticket_text, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, username, full_name, ticket_text, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch all tickets
    def fetch_tickets():
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM tickets5 ORDER BY timestamp DESC''')
        tickets = c.fetchall()
        conn.close()
        return tickets

    # Tabs for AI Tool, Session, and Ticket
    tab1, tab2, tab3 = st.tabs(["AI Tool", "Session", "Ticket"])
    
    with tab1:
        st.header("AI Tool")
        st.write("Please enter the following details:")

        # Input fields
        type_options = {"Government Office": 1, "Health Center": 2, "School": 3}
        type_input = st.selectbox("Type", list(type_options.keys()))
        region = st.text_input("Region:").lower()
        population_served = st.number_input("Population Served:", min_value=0)
        connectivity_status = st.selectbox("Connectivity Status", ["Connected", "Unconnected"])
        existing_infrastructure = st.selectbox("Existing Infrastructure", ["Yes", "No"])
        equipment_used = st.text_input("Equipment Needs:").lower()

        if st.button("Predict"):
            # Preprocess input data
            input_data = {
                'Type': type_options[type_input],
                'Region': region,
                'Population_Served': population_served,
                'Connectivity_Status': 1 if connectivity_status == "Connected" else 2,
                'Existing_Infrastructure': 1 if existing_infrastructure == "Yes" else 2,
                'Equipment_Used': equipment_used
            }

            # Predict
            cost_pred, time_pred, quantity_pred = predict_cost_time_and_quantity(input_data)
            st.write(f"Predicted Cost (USD): {cost_pred:.2f}")
            st.write(f"Predicted Delivery Time (Days): {time_pred:.2f}")
            st.write(f"Predicted Quantity (Units): {quantity_pred}")

            # Get Gemini insights
            insights = get_gemini_insights(input_data, cost_pred, time_pred, quantity_pred)
            st.write("Gemini AI Insights and Recommendations:")
            st.write(insights)

            # Save session to database
            save_session(st.session_state.user_id, input_data, cost_pred, time_pred, quantity_pred, insights)
            st.success("Session saved successfully!")
            
    with tab2:
        st.header("Session")
        sessions = fetch_sessions(st.session_state.user_id)
        if sessions:
            for session in sessions:
                # Use expander for each session
                with st.expander(f"Session ID: {session[0]} - {session[7]}"):
                    st.write(f"Timestamp: {session[7]}")
                    st.write("Input Data:")
                            
                    # Convert input data from string to dictionary
                    input_data = eval(session[2])
                            
                    # Display input data as bullet points
                    st.markdown("- **Type:** " + str(input_data.get('Type', 'N/A')))
                    st.markdown("- **Region:** " + str(input_data.get('Region', 'N/A')))
                    st.markdown("- **Population Served:** " + str(input_data.get('Population_Served', 'N/A')))
                    st.markdown("- **Connectivity Status:** " + str(input_data.get('Connectivity_Status', 'N/A')))
                    st.markdown("- **Existing Infrastructure:** " + str(input_data.get('Existing_Infrastructure', 'N/A')))
                    st.markdown("- **Equipment Needs:** " + str(input_data.get('Equipment_Used', 'N/A')))
                    
                    st.write("Predictions:")
                    st.write(f"- Cost (USD): {float(session[3]):.2f}")
                    st.write(f"- Delivery Time (Days): {float(session[4]):.2f}")
                    st.write(f"- Quantity (Units): {int(session[5])}")
                            
                    st.write("Insights:")
                    st.write(session[6])
                            
                    # Download session data as .txt
                    session_data = f"Input Data:\n{session[2]}\n\nPredictions:\nCost: {float(session[3]):.2f} USD\nDelivery Time: {float(session[4]):.2f} Days\nQuantity: {int(session[5])} Units\n\nInsights:\n{session[6]}"
                    st.download_button(
                        label=f"Download Session {session[0]}",
                        data=session_data,
                        file_name=f"tech_{st.session_state.user_id}_procurement_optimization_{session[0]}.txt",
                        mime="text/plain"
                    )
        else:
            st.write("No sessions found.")
            
    with tab3:
        st.header("Ticket")
        st.write("Submit a ticket to report an issue or provide feedback.")
                
        # Ticket submission form
        ticket_text = st.text_area("Describe the issue or feedback:")
        if st.button("Submit Ticket"):
            if ticket_text.strip():
                save_ticket(st.session_state.user_id, st.session_state.username, st.session_state.full_name, ticket_text)
                st.success("Ticket submitted successfully!")
            else:
                st.error("Please enter a description for the ticket.")
                
        # Display all tickets
        st.write("### All Tickets")
        tickets = fetch_tickets()
        if tickets:
            for ticket in tickets:
                st.write(f"**Ticket ID:** {ticket[0]}")
                st.write(f"**Submitted by:** {ticket[3]} (Username: {ticket[2]}, User ID: {ticket[1]})")
                st.write(f"**Timestamp:** {ticket[5]}")
                st.write(f"**Description:** {ticket[4]}")
                st.write("---")
        else:
            st.write("No tickets found.")

# AI Tool 6: Connectivity Insights
def connectivity_insights():
    st.title("Region Specific Connectivity Insights")

    # Load the pre-trained model and data
    model_path = 'connectivity_regression_model.pkl'
    model = joblib.load(model_path)

    regional_insights_path = 'regional_insights.csv'
    regional_insights = pd.read_csv(regional_insights_path)

    # Function to predict connectivity percentage ratio
    def predict_connectivity_percentage_ratio(input_data, model, X_columns):
        input_df = pd.DataFrame([input_data])
        for col in X_columns:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[X_columns]
        connectivity_percentage_ratio = model.predict(input_df)[0]
        return connectivity_percentage_ratio

    # Function to get Gemini AI insights
    def get_gemini_insights(regional_insights, user_input, predicted_connectivity):
        data_to_send = {
            "regional_insights": regional_insights.to_dict(),
            "user_input": user_input,
            "predicted_connectivity": predicted_connectivity
        }
        prompt = f"""
        You are an expert in regional connectivity analysis. Based on the following data, provide concise and actionable insights, recommendations, suggestions, and notes in the following format:

        - **Insights**: List key observations from the data in short, concise bullet points.
        - **Recommendations**: Provide actionable recommendations in short, concise bullet points.
        - **Suggestions**: Provide actionable suggestions in short, concise bullet points.
        - **Notes**: Add any additional notes or considerations in short, concise bullet points.

        Data:
        - Regional Insights: {data_to_send['regional_insights']}
        - User Input: {data_to_send['user_input']}
        - Predicted Connectivity Percentage Ratio: {data_to_send['predicted_connectivity']}
        """
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            n=1,
            messages=[
                {"role": "system", "content": "You are an expert in regional connectivity analysis. Provide concise and actionable insights in bullet points."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    # Function to save session data
    def save_session(user_id, input_data, prediction, insights):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO sessions6 (user_id, input_data, prediction, insights, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, str(input_data), str(prediction), insights, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch session data
    def fetch_sessions(user_id):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM sessions6 WHERE user_id = ?''', (user_id,))
        sessions = c.fetchall()
        conn.close()
        return sessions

    # Function to save a ticket
    def save_ticket(user_id, username, full_name, ticket_text):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO tickets6 (user_id, username, full_name, ticket_text, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, username, full_name, ticket_text, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch all tickets
    def fetch_tickets():
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM tickets6 ORDER BY timestamp DESC''')
        tickets = c.fetchall()
        conn.close()
        return tickets

    # Tabs for AI Tool, Session, and Ticket
    tab1, tab2, tab3 = st.tabs(["AI Tool", "Session", "Ticket"])
            
    with tab1:
        st.header("AI Tool")
        st.write("Please enter the following details:")
                
        region = st.text_input("Region:").strip().lower()
        type_options = {"Government Office": 1, "Health Center": 2, "School": 3}
        type_input = st.selectbox("Organization Type", list(type_options.keys()))
        population_served = st.number_input("Population Served:", min_value=0)
        include_infrastructure = st.selectbox("Do you know the existing infrastructure status?", ["No", "Yes"])
        if include_infrastructure == "Yes":
            infrastructure_input = st.selectbox("Existing Infrastructure", ["Yes", "No"])
        else:
            infrastructure_input = "No"
                
        if st.button("Predict"):
            user_input = {
                'Region': region,
                'Type': type_input.lower(),
                'Population_Served': population_served,
                'Existing_Infrastructure': infrastructure_input.lower()
            }
                    
            connectivity_percentage_ratio = predict_connectivity_percentage_ratio(
                user_input,
                model,
                regional_insights.drop(columns=['Connectivity_Rate']).columns
            )
                    
            st.write(f"Predicted Connectivity Percentage Ratio: {connectivity_percentage_ratio:.2f}%")
                    
            insights = get_gemini_insights(regional_insights, user_input, connectivity_percentage_ratio)
            st.write("Gemini AI Insights and Recommendations:")
            st.write(insights)
                    
            # Save session to database
            save_session(st.session_state.user_id, user_input, connectivity_percentage_ratio, insights)
            st.success("Session saved successfully!")
            
    with tab2:
        st.header("Session")
        sessions = fetch_sessions(st.session_state.user_id)
        if sessions:
            for session in sessions:
                with st.expander(f"Session ID: {session[0]} - {session[5]}"):
                    st.write(f"Timestamp: {session[5]}")
                    st.write("Input Data:")
                    input_data = eval(session[2])
                    st.markdown("- **Region:** " + str(input_data.get('Region', 'N/A')))
                    st.markdown("- **Organization Type:** " + str(input_data.get('Type', 'N/A')))
                    st.markdown("- **Population Served:** " + str(input_data.get('Population_Served', 'N/A')))
                    st.markdown("- **Existing Infrastructure:** " + str(input_data.get('Existing_Infrastructure', 'N/A')))
                    st.write("Prediction:")
                    st.write(session[3])
                    st.write("Insights:")
                    st.write(session[4])
                            
                    # Download session data as .txt
                    session_data = f"Input Data:\n{session[2]}\n\nPrediction:\n{session[3]}\n\nInsights:\n{session[4]}"
                    st.download_button(
                        label=f"Download Session {session[0]}",
                        data=session_data,
                        file_name=f"tech_{st.session_state.user_id}_connectivity_insights_{session[0]}.txt",
                        mime="text/plain"
                    )
        else:
            st.write("No sessions found.")
            
    with tab3:
        st.header("Ticket")
        st.write("Submit a ticket to report an issue or provide feedback.")
                
        ticket_text = st.text_area("Describe the issue or feedback:")
        if st.button("Submit Ticket"):
            if ticket_text.strip():
                save_ticket(st.session_state.user_id, st.session_state.username, st.session_state.full_name, ticket_text)
                st.success("Ticket submitted successfully!")
            else:
                st.error("Please enter a description for the ticket.")
                
        st.write("### All Tickets")
        tickets = fetch_tickets()
        if tickets:
            for ticket in tickets:
                st.write(f"**Ticket ID:** {ticket[0]}")
                st.write(f"**Submitted by:** {ticket[3]} (Username: {ticket[2]}, User ID: {ticket[1]})")
                st.write(f"**Timestamp:** {ticket[5]}")
                st.write(f"**Description:** {ticket[4]}")
                st.write("---")
        else:
            st.write("No tickets found.")

# AI Tool 7: Deployment Strategist
def deployment_strategist():
    st.title("Network Deployment Planner")

    # Load the pre-trained models
    cost_model = joblib.load('cost_prediction_model.pkl')
    time_model = joblib.load('time_prediction_model.pkl')

    # Load the dataset for feature columns
    data = pd.read_csv("procurement_merged_data.csv")
    data = data.drop(columns=['Deployment_ID', 'Latitude', 'Longitude', 'Vendor_Details', 'Connectivity_Status', 'Existing_Infrastructure', 'Quantity'])
    data['Type'] = data['Type'].map({'Government Office': 1, 'Health Center': 2, 'School': 3})
    data = pd.get_dummies(data, columns=['Region', 'Equipment_Used'], drop_first=True)
    X = data.drop(columns=['Cost_USD', 'Time_Taken_Days'])

    # Function to predict cost and time
    def predict_cost_and_time(input_data):
        input_df = pd.DataFrame([input_data])
        for col in X.columns:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[X.columns]
        cost_pred = float(cost_model.predict(input_df)[0])  # Ensure float type
        time_pred = float(time_model.predict(input_df)[0])  # Ensure float type
        return cost_pred, time_pred

    # Function to get Gemini AI insights
    def get_gemini_insights(user_input, cost_pred, time_pred, equipment):
        prompt = f"""
        User Input Data:
        - Node_ID: {user_input['Node_ID']}
        - Population_Served: {user_input['Population_Served']}
        - Region: {user_input['Region']}
        - Type: {user_input['Type']}
        - Equipment: {equipment}
        - Quantity: {user_input['Quantity']}
        
        Traditional AI Predictions:
        - Predicted Cost (USD): {cost_pred:.2f}
        - Predicted Time (Days): {time_pred:.2f}
        
        Provide detailed insights, recommendations, suggestions, and notes for this network deployment plan. Format the output as follows:
        
        - **Insights**: List key observations from the data in short, concise bullet points.
        - **Recommendations**: Provide actionable recommendations in short, concise bullet points.
        - **Suggestions**: Provide actionable suggestions in short, concise bullet points.
        - **Notes**: Add any additional notes or considerations in short, concise bullet points.
        """
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            n=1,
            messages=[
                {"role": "system", "content": "You are a network deployment expert. Provide insights, recommendations, suggestions, and notes in short, concise bullet points. Format the output exactly as specified."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    # Function to save session data
    def save_session(user_id, input_data, cost_pred, time_pred, insights):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO sessions7 (user_id, input_data, cost_prediction, time_prediction, insights, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)''', 
                (user_id, str(input_data), float(cost_pred), float(time_pred), insights, datetime.now()))  # Ensure float type
        conn.commit()
        conn.close()

    # Function to fetch session data
    def fetch_sessions(user_id):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM sessions7 WHERE user_id = ?''', (user_id,))
        sessions = c.fetchall()
        conn.close()
        return sessions

    # Function to save a ticket
    def save_ticket(user_id, username, full_name, ticket_text):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO tickets7 (user_id, username, full_name, ticket_text, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, username, full_name, ticket_text, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch all tickets
    def fetch_tickets():
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM tickets7 ORDER BY timestamp DESC''')
        tickets = c.fetchall()
        conn.close()
        return tickets

    # Tabs for AI Tool, Session, and Ticket
    tab1, tab2, tab3 = st.tabs(["AI Tool", "Session", "Ticket"])
            
    with tab1:
        st.header("AI Tool")
        st.write("Please enter the following details:")

        # Input fields
        node_id = st.text_input("Node ID (e.g., Node_1, Node_2, etc.):")
        population_served = st.number_input("Population Served:", min_value=0)
        region = st.text_input("Region:").lower()
        type_options = {"Government Office": 1, "Health Center": 2, "School": 3}
        type_input = st.selectbox("Type", list(type_options.keys()))
        type_value = type_options[type_input]
        equipment = st.selectbox("Equipment", ["Cable", "Switch", "Antenna", "Router"])
        quantity = st.number_input("Quantity for Equipment:", min_value=1)

        if st.button("Predict"):
            # Preprocess input data
            user_input = {
                'Node_ID': node_id,
                'Population_Served': population_served,
                'Region': region,
                'Type': type_value,
                'Quantity': quantity
            }
            for col in X.columns:
                if col.startswith("Equipment_Used_"):
                    user_input[col] = 1 if col == f"Equipment_Used_{equipment.lower()}" else 0

            # Predict
            cost_pred, time_pred = predict_cost_and_time(user_input)
            st.write(f"Predicted Cost (USD): {cost_pred:.2f}")
            st.write(f"Predicted Time (Days): {time_pred:.2f}")

            # Get Gemini insights
            insights = get_gemini_insights(user_input, cost_pred, time_pred, equipment)
            st.write("Gemini AI Insights and Recommendations:")
            st.write(insights)

            # Save session to database
            save_session(st.session_state.user_id, user_input, cost_pred, time_pred, insights)
            st.success("Session saved successfully!")
            
    with tab2:
        st.header("Session")
        sessions = fetch_sessions(st.session_state.user_id)
        if sessions:
            for session in sessions:
                with st.expander(f"Session ID: {session[0]} - {session[6]}"):
                    st.write(f"Timestamp: {session[6]}")
                    st.write("Input Data:")
                    input_data = eval(session[2])
                    st.markdown("- **Node ID:** " + str(input_data.get('Node_ID', 'N/A')))
                    st.markdown("- **Population Served:** " + str(input_data.get('Population_Served', 'N/A')))
                    st.markdown("- **Region:** " + str(input_data.get('Region', 'N/A')))
                    st.markdown("- **Type:** " + str(input_data.get('Type', 'N/A')))
                    st.markdown("- **Equipment:** " + str(input_data.get('Equipment', 'N/A')))
                    st.markdown("- **Quantity:** " + str(input_data.get('Quantity', 'N/A')))
                    st.write("Predictions:")
                    st.write(f"Cost (USD): {float(session[3]):.2f}")  # Ensure float type
                    st.write(f"Time (Days): {float(session[4]):.2f}")  # Ensure float type
                    st.write("Insights:")
                    st.write(session[5])
                
                    # Download session data as .txt
                    session_data = f"Input Data:\n{session[2]}\n\nPredictions:\nCost (USD): {float(session[3]):.2f}\nTime (Days): {float(session[4]):.2f}\n\nInsights:\n{session[5]}"
                    st.download_button(
                        label=f"Download Session {session[0]}",
                        data=session_data,
                        file_name=f"tech_{st.session_state.user_id}_network_deployment_{session[0]}.txt",
                        mime="text/plain"
                    )
        else:
            st.write("No sessions found.")
    
    with tab3:
        st.header("Ticket")
        st.write("Submit a ticket to report an issue or provide feedback.")
                
        # Ticket submission form
        ticket_text = st.text_area("Describe the issue or feedback:")
        if st.button("Submit Ticket"):
            if ticket_text.strip():
                save_ticket(st.session_state.user_id, st.session_state.username, st.session_state.full_name, ticket_text)
                st.success("Ticket submitted successfully!")
            else:
                st.error("Please enter a description for the ticket.")
                
        # Display all tickets
        st.write("### All Tickets")
        tickets = fetch_tickets()
        if tickets:
            for ticket in tickets:
                st.write(f"**Ticket ID:** {ticket[0]}")
                st.write(f"**Submitted by:** {ticket[3]} (Username: {ticket[2]}, User ID: {ticket[1]})")
                st.write(f"**Timestamp:** {ticket[5]}")
                st.write(f"**Description:** {ticket[4]}")
                st.write("---")
        else:
            st.write("No tickets found.")

# AI Tool 8: Network Node Monitor
def network_node_monitor():
    st.title("Node Performance Monitoring System")

    # Load ML models
    DATA_USAGE_MODEL_PATH = 'data_usage_regression_model.pkl'
    PEAK_USAGE_MODEL_PATH = 'peak_usage_regression_model.pkl'
    DOWNTIME_EVENTS_MODEL_PATH = 'downtime_events_regression_model.pkl'

    data_usage_model = joblib.load(DATA_USAGE_MODEL_PATH)
    peak_usage_model = joblib.load(PEAK_USAGE_MODEL_PATH)
    downtime_events_model = joblib.load(DOWNTIME_EVENTS_MODEL_PATH)

    # Load node data
    NODES_DATA_PATH = "nodes.csv"  # Path to nodes.csv
    nodes = pd.read_csv(NODES_DATA_PATH)

    # Function to predict for a single node
    def predict_for_node(node_data, date, start_hour, end_hour, data_usage_model, peak_usage_model, downtime_events_model, X_columns):
        predictions = []
        for hour in range(start_hour, end_hour + 1):
            input_df = pd.DataFrame([{
                'Year': date.year,
                'Month': date.month,
                'Day': date.day,
                'Hour': hour,
                **node_data
            }])
            
            # One-hot encode categorical variables
            input_df = pd.get_dummies(input_df, columns=['Type', 'Region', 'Connectivity_Status', 'Existing_Infrastructure'], drop_first=True)
            
            # Ensure the input DataFrame has the same columns as the training data
            for col in X_columns:
                if col not in input_df.columns:
                    input_df[col] = 0
            input_df = input_df[X_columns]
            
            # Predict
            data_usage_pred = data_usage_model.predict(input_df)[0]
            peak_usage_pred = peak_usage_model.predict(input_df)[0]
            downtime_events_pred = int(round(downtime_events_model.predict(input_df)[0]))
            
            predictions.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Time': f"{hour:02d}:00:00",
                'Node_ID': node_data['Node_ID'],
                'Data_Usage_GB': data_usage_pred,
                'Peak_Usage_GB': peak_usage_pred,
                'Downtime_Events': downtime_events_pred
            })
        return predictions

    # Function to predict for all nodes
    def predict_data_peak_downtime_for_all_nodes(date, start_time, end_time):
        start_hour = start_time.hour
        end_hour = end_time.hour
        
        nodes_data = nodes.to_dict('records')
        X_columns = data_usage_model.feature_names_in_
        
        results = Parallel(n_jobs=-1)(
            delayed(predict_for_node)(node, date, start_hour, end_hour, data_usage_model, peak_usage_model, downtime_events_model, X_columns)
            for node in nodes_data
        )
        
        all_predictions = [pred for sublist in results for pred in sublist]
        return pd.DataFrame(all_predictions)

    # Function to get Gemini AI insights
    def get_gemini_insights(user_input, predictions_df):
        prompt = f"""
        **User Input:**
        - Date: {user_input[0].strftime('%Y-%m-%d')}
        - Start Time: {user_input[1].strftime('%H:%M:%S')}
        - End Time: {user_input[2].strftime('%H:%M:%S')}

        **Predictions:**
        {predictions_df.to_string()}

        **Task:**
        Based on the above user input and predictions, provide the following in **short, concise bullet points**:

        - **Insights**: List key observations from the data.
        - **Recommendations**: Provide actionable recommendations.
        - **Suggestions**: Offer practical suggestions for improvement.
        - **Notes**: Add any additional notes or considerations.
        """
        
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            n=1,
            messages=[
                {"role": "system", "content": "You are a performance optimization assistant. Provide insights, recommendations, suggestions, and notes in short, concise bullet points. Keep the response clear and actionable."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

    # Function to serialize input data
    def serialize_input_data(input_data):
        serialized_data = {
            "date": input_data[0].strftime('%Y-%m-%d'),
            "start_time": input_data[1].strftime('%H:%M:%S'),
            "end_time": input_data[2].strftime('%H:%M:%S')
        }
        return str(serialized_data)

    # Function to deserialize input data
    def deserialize_input_data(input_data_str):
        input_data_dict = eval(input_data_str)  # Safely evaluate the string as a dictionary
        return (
            datetime.strptime(input_data_dict["date"], '%Y-%m-%d').date(),
            datetime.strptime(input_data_dict["start_time"], '%H:%M:%S').time(),
            datetime.strptime(input_data_dict["end_time"], '%H:%M:%S').time()
        )

    # Function to save session data
    def save_session(user_id, input_data, predictions, insights):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO sessions8 (user_id, input_data, predictions, insights, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, serialize_input_data(input_data), predictions.to_csv(index=False), insights, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch session data
    def fetch_sessions(user_id):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM sessions8 WHERE user_id = ?''', (user_id,))
        sessions = c.fetchall()
        conn.close()
        return sessions

    # Function to save a ticket
    def save_ticket(user_id, username, full_name, ticket_text):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO tickets8 (user_id, username, full_name, ticket_text, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, username, full_name, ticket_text, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch all tickets
    def fetch_tickets():
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM tickets8 ORDER BY timestamp DESC''')
        tickets = c.fetchall()
        conn.close()
        return tickets

    # Tabs for AI Tool, Session, and Ticket
    tab1, tab2, tab3 = st.tabs(["AI Tool", "Session", "Ticket"])
            
    with tab1:
        st.header("AI Tool")
        date = st.date_input("Enter Date (YYYY-MM-DD):")
        start_time = st.time_input("Enter Start Time:", value=time(1, 0, 0))  # Include seconds
        end_time = st.time_input("Enter End Time:", value=time(2, 0, 0))  # Include seconds
                
        if st.button("Predict"):
            user_input = (date, start_time, end_time)
            predictions_df = predict_data_peak_downtime_for_all_nodes(date, start_time, end_time)
                    
            st.write("Prediction Results:")
            st.dataframe(predictions_df)
                    
            insights = get_gemini_insights(user_input, predictions_df)
            st.write("Gemini AI Insights and Recommendations:")
            st.write(insights)
                    
            save_session(st.session_state.user_id, user_input, predictions_df, insights)
            st.success("Session saved successfully!")
            
    with tab2:
        st.header("Session")
        sessions = fetch_sessions(st.session_state.user_id)
        if sessions:
            for session in sessions:
                with st.expander(f"Session ID: {session[0]} - {session[5]}"):
                    st.write(f"Timestamp: {session[5]}")
                    st.write("Input Data:")
                    input_data = deserialize_input_data(session[2])  # Deserialize input data
                    st.write(input_data)
                            
                    st.write("Predictions:")
                    predictions_df = pd.read_csv(io.StringIO(session[3]))  # Read CSV data
                    st.dataframe(predictions_df)
                            
                    st.write("Insights:")
                    st.write(session[4])
                            
                    session_data = f"Input Data:\n{session[2]}\n\nPredictions:\n{predictions_df.to_string(index=False)}\n\nInsights:\n{session[4]}"
                    st.download_button(
                        label=f"Download Session {session[0]}",
                        data=session_data,
                        file_name=f"node_performance_session_{session[0]}.txt",
                        mime="text/plain"
                    )
        else:
            st.write("No sessions found.")
            
    with tab3:
        st.header("Ticket")
        st.write("Submit a ticket to report an issue or provide feedback.")
                
        ticket_text = st.text_area("Describe the issue or feedback:")
        if st.button("Submit Ticket"):
            if ticket_text.strip():
                save_ticket(st.session_state.user_id, st.session_state.username, st.session_state.full_name, ticket_text)
                st.success("Ticket submitted successfully!")
            else:
                st.error("Please enter a description for the ticket.")
                
        st.write("### All Tickets")
        tickets = fetch_tickets()
        if tickets:
            for ticket in tickets:
                st.write(f"**Ticket ID:** {ticket[0]}")
                st.write(f"**Submitted by:** {ticket[3]} (Username: {ticket[2]}, User ID: {ticket[1]})")
                st.write(f"**Timestamp:** {ticket[5]}")
                st.write(f"**Description:** {ticket[4]}")
                st.write("---")
        else:
            st.write("No tickets found.")

# AI Tool 9: Sustainability Tracker
def sustainability_tracker():
    st.title("Sustainability Reporting System")

    # Load the sustainability dataset
    data = pd.read_csv("sustainability_merged_data.csv")

    # Feature Engineering
    data['Date'] = pd.to_datetime(data['Date'])
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    data = data.drop(columns=['Region_Name', 'Region_ID', 'Log_ID', 'Deployment_ID', 'Recommendation_ID', 'Date'])
    data = pd.get_dummies(data, columns=['Energy_Source', 'Region', 'Existing_Infrastructure', 'Type', 
                                        'Issue_Type', 'Equipment_Used', 'Vendor_Details', 'Action_Type', 
                                        'Peak_Usage_Time'], drop_first=True)

    # Define Impact Scores
    data['Energy_Impact_Score'] = data['Energy_Usage_kWh'] / data['Population_Served']
    data['Emissions_Impact_Score'] = data['Carbon_Emissions_kg_CO2'] / data['Population_Served']
    data['Infrastructure_Impact_Score'] = data['Resolution_Time_Hours'] * data['Downtime_Events']

    # Split into Features (X) and Targets (y)
    X = data.drop(columns=['Energy_Usage_kWh', 'Carbon_Emissions_kg_CO2', 'Energy_Impact_Score', 
                        'Emissions_Impact_Score', 'Infrastructure_Impact_Score'])

    # Load the pre-trained models
    energy_model = joblib.load('energy_impact_model.pkl')
    emissions_model = joblib.load('emissions_impact_model.pkl')
    infrastructure_model = joblib.load('infrastructure_impact_model.pkl')

    # Function to predict impact scores
    def predict_impact_scores(input_data, start_date, end_date):
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        predictions = []
        
        for date in date_range:
            month = date.month
            day = date.day
            input_df = pd.DataFrame([input_data])
            input_df['Month'] = month
            input_df['Day'] = day
            
            # Ensure all columns are present
            for col in X.columns:
                if col not in input_df.columns:
                    input_df[col] = 0
            
            input_df = input_df[X.columns]
            
            energy_score = energy_model.predict(input_df)
            emissions_score = emissions_model.predict(input_df)
            infrastructure_score = infrastructure_model.predict(input_df)
            
            predictions.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Energy_Impact_Score': energy_score[0],
                'Emissions_Impact_Score': emissions_score[0],
                'Infrastructure_Impact_Score': infrastructure_score[0]
            })
        
        return pd.DataFrame(predictions)

    # Function to generate ML reports
    def generate_ml_report(predictions_df):
        report = {
            "Summary Statistics": {
                "Average Energy Impact Score": f"{predictions_df['Energy_Impact_Score'].mean():.2f} kWh/person",
                "Average Emissions Impact Score": f"{predictions_df['Emissions_Impact_Score'].mean():.2f} kg CO₂/person",
                "Average Infrastructure Impact Score": f"{predictions_df['Infrastructure_Impact_Score'].mean():.2f}"
            },
            "Actionable Insights": {
                "Energy": "Consider implementing energy-saving measures or switching to renewable energy sources."
                if predictions_df['Energy_Impact_Score'].mean() > 1.0
                else "Energy usage is relatively efficient. Maintain current practices and monitor for changes.",
                "CO₂ Emissions": "Explore carbon offset programs or transition to low-emission energy sources."
                if predictions_df['Emissions_Impact_Score'].mean() > 0.5
                else "CO₂ emissions are relatively low. Continue monitoring and aim for further reductions.",
                "Infrastructure": "Prioritize infrastructure maintenance and consider upgrading critical systems."
                if predictions_df['Infrastructure_Impact_Score'].mean() > 5.0
                else "Infrastructure is relatively stable. Continue regular maintenance and monitoring."
            }
        }
        return report

    # Function to get Gemini AI insights
    def get_gemini_insights(user_input, predictions_df):
        input_text = f"""
        User Input:
        {user_input}

        Predictions:
        {predictions_df.to_string()}

        Based on the above user input and predictions, provide insights and recommendations in the following structured format:

        **Insights**:
        - List key observations from the data in short, concise bullet points.

        **Recommendations**:
        - Provide high-level recommendations to address the observed issues or opportunities.

        **Suggestions**:
        - Offer actionable suggestions in short, concise bullet points.

        **Notes**:
        - Add any additional notes or considerations in short, concise bullet points.
        """
        
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[
                {"role": "system", "content": "You are a sustainability expert. Your role is to provide concise, actionable, and structured insights in bullet points."},
                {"role": "user", "content": input_text}
            ]
        )
        return response.choices[0].message.content

    # Function to save session data
    def save_session(user_id, input_data, predictions, insights):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO sessions9 (user_id, input_data, predictions, insights, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, str(input_data), str(predictions), insights, datetime.now()))
        conn.commit()
        conn.close()

    # Function to fetch session data
    def fetch_sessions(user_id):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM sessions9 WHERE user_id = ?''', (user_id,))
        sessions = c.fetchall()
        conn.close()
        return sessions

    # Function to save a ticket
    def save_ticket(user_id, username, full_name, ticket_text):
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''INSERT INTO tickets9 (user_id, username, full_name, ticket_text, timestamp)
                    VALUES (?, ?, ?, ?, ?)''', 
                (user_id, username, full_name, ticket_text, datetime.now()))
        conn.commit()
        conn.close()
    
    # Function to fetch all tickets
    def fetch_tickets():
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute('''SELECT * FROM tickets9 ORDER BY timestamp DESC''')
        tickets = c.fetchall()
        conn.close()
        return tickets

    # Tabs for AI Tool, Session, and Ticket
    tab1, tab2, tab3 = st.tabs(["AI Tool", "Session", "Ticket"])
            
    with tab1:
        st.header("AI Tool")
        st.write("Please enter the following details:")

        # Input fields
        node_id = st.text_input("Node ID:")
        population_served = st.number_input("Population Served:", min_value=0)
        region = st.text_input("Region:").lower()
                
        energy_source = st.selectbox("Energy Source:", ["Grid", "Solar", "Generator"])
        peak_usage_time = st.selectbox("Peak Usage Time:", ["Morning", "Afternoon", "Evening", "Night"])
        # Type with "Other" option
        type_options = ["Government Office", "Health Center", "School", "Other"]
        type_input = st.selectbox("Select the Type:", type_options)
        if type_input == "Other":
            type_input = st.text_input("Enter the Type manually:")
        type_input = type_input
        existing_infrastructure = st.selectbox("Existing Infrastructure:", ["Yes", "No"])
                
        start_date = st.date_input("Start Date:")
        end_date = st.date_input("End Date:")

        if st.button("Predict"):
            # Preprocess input data
            user_input = {
                'Node_ID': node_id,
                'Population_Served': population_served,
                'Region': region,
                'Energy_Source': energy_source,
                'Peak_Usage_Time': peak_usage_time,
                'Type': type_input,
                'Existing_Infrastructure': existing_infrastructure
            }
                    
            # Predict impact scores
            predictions_df = predict_impact_scores(user_input, start_date, end_date)
            st.write("Predictions:")
            st.write(predictions_df)

            # Generate ML report
            ml_report = generate_ml_report(predictions_df)
            st.write("### ML Report")
            st.write("#### Summary Statistics")
            for key, value in ml_report["Summary Statistics"].items():
                st.markdown(f"- **{key}**: {value}")
                    
            st.write("#### Actionable Insights")
            for key, value in ml_report["Actionable Insights"].items():
                st.markdown(f"- **{key}**: {value}")

            # Get Gemini insights
            insights = get_gemini_insights(user_input, predictions_df)
            st.write("### Gemini AI Insights and Recommendations:")
            st.write(insights)

            # Save session to database
            save_session(st.session_state.user_id, user_input, predictions_df.to_dict(), insights)
            st.success("Session saved successfully!")
            
    with tab2:
        st.header("Session")
        sessions = fetch_sessions(st.session_state.user_id)
        if sessions:
            for session in sessions:
                # Use expander for each session
                with st.expander(f"Session ID: {session[0]} - {session[5]}"):
                    st.write(f"Timestamp: {session[5]}")
                    st.write("Input Data:")
                            
                    # Convert input data from string to dictionary
                    input_data = eval(session[2])
                            
                    # Display input data as bullet points
                    st.markdown("- **Node ID:** " + str(input_data.get('Node_ID', 'N/A')))
                    st.markdown("- **Population Served:** " + str(input_data.get('Population_Served', 'N/A')))
                    st.markdown("- **Region:** " + str(input_data.get('Region', 'N/A')))
                    st.markdown("- **Energy Source:** " + str(input_data.get('Energy_Source', 'N/A')))
                    st.markdown("- **Peak Usage Time:** " + str(input_data.get('Peak_Usage_Time', 'N/A')))
                    st.markdown("- **Type:** " + str(input_data.get('Type', 'N/A')))
                    st.markdown("- **Existing Infrastructure:** " + str(input_data.get('Existing_Infrastructure', 'N/A')))
                            
                    st.write("Predictions:")
                    st.write(eval(session[3]))
                    st.write("Insights:")
                    st.write(session[4])
                            
                    # Download session data as .txt
                    session_data = f"Input Data:\n{session[2]}\n\nPredictions:\n{session[3]}\n\nInsights:\n{session[4]}"
                    st.download_button(
                        label=f"Download Session {session[0]}",
                        data=session_data,
                        file_name=f"user_{st.session_state.user_id}_sustainability_{session[0]}.txt",
                        mime="text/plain"
                    )
        else:
            st.write("No sessions found.")
            
    with tab3:
        st.header("Ticket")
        st.write("Submit a ticket to report an issue or provide feedback.")
                
        # Ticket submission form
        ticket_text = st.text_area("Describe the issue or feedback:")
        if st.button("Submit Ticket"):
            if ticket_text.strip():
                save_ticket(st.session_state.user_id, st.session_state.username, st.session_state.full_name, ticket_text)
                st.success("Ticket submitted successfully!")
            else:
                st.error("Please enter a description for the ticket.")
                
        # Display all tickets
        st.write("### All Tickets")
        tickets = fetch_tickets()
        if tickets:
            for ticket in tickets:
                st.write(f"**Ticket ID:** {ticket[0]}")
                st.write(f"**Submitted by:** {ticket[3]} (Username: {ticket[2]}, User ID: {ticket[1]})")
                st.write(f"**Timestamp:** {ticket[5]}")
                st.write(f"**Description:** {ticket[4]}")
                st.write("---")
        else:
            st.write("No tickets found.")

# Main App
def main():    
    # User authentication
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if st.session_state.user_id is None:
        # Centered title
        st.markdown(
            """
            <h1 style='text-align: center;'>EcoSphereAI</h1>
            """,
            unsafe_allow_html=True
            )
            
        st.header("Login / Signup")
        choice = st.selectbox("Choose an option:", ["Login", "Signup"])
        
        if choice == "Login":
            # Pre-fill username and password for demonstration
            username = st.text_input("Username:", value="tech_1")
            password = st.text_input("Password:", type="password", value="12345678")
            if st.button("Login"):
                conn = sqlite3.connect("app.db")
                c = conn.cursor()
                c.execute('''SELECT id, full_name, password, avatar FROM users WHERE username = ?''', (username,))
                user = c.fetchone()
                conn.close()
                if user:
                    if user[2] == password:
                        st.session_state.user_id = user[0]
                        st.session_state.username = username
                        st.session_state.full_name = user[1]
                        st.session_state.avatar = user[3]
                        st.success("Logged in successfully!")
                    else:
                        st.error("Invalid password.")
                else:
                    st.error("Username does not exist.")
        
        elif choice == "Signup":
            full_name = st.text_input("Enter your Full Name:")
            username = st.text_input("Choose a Username:")
            password = st.text_input("Choose a Password:", type="password")
            if st.button("Signup"):
                if not full_name or not username or not password:
                    st.error("All fields are required.")
                else:
                    is_valid, message = validate_password(password)
                    if not is_valid:
                        st.error(message)
                    else:
                        conn = sqlite3.connect("app.db")
                        c = conn.cursor()
                        try:
                            c.execute('''INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)''', 
                                      (username, password, full_name))
                            conn.commit()
                            st.success("Signup successful! Please login.")
                        except sqlite3.IntegrityError:
                            st.error("Username already exists.")
                        conn.close()
    
    if st.session_state.user_id is not None:
        # Sidebar for navigation and user info
        st.sidebar.title("EcoSphereAI")
        
        # Show user avatar, full name, and user ID
        if st.session_state.avatar:
            avatar_image = Image.open(io.BytesIO(st.session_state.avatar))
            rounded_img_html = rounded_image(avatar_image)
            st.sidebar.markdown(rounded_img_html, unsafe_allow_html=True)
        st.sidebar.write(f"**{st.session_state.full_name}**")
        st.sidebar.write(f"Logged in as User ID: {st.session_state.user_id}")
        
        # Show only the logout button after login
        if st.sidebar.button("Logout"):
            st.session_state.user_id = None
            st.sidebar.success("Logged out successfully!")
        
        # Main navigation buttons
        st.sidebar.header("Navigation")
        if st.sidebar.button("Dashboard"):
            st.session_state.current_page = "Dashboard"
        if st.sidebar.button("Settings"):
            st.session_state.current_page = "Settings"

        # AI Tools buttons
        st.sidebar.header("AI Tools")
        if st.sidebar.button("Energy & CO₂ Optimizer"):
            st.session_state.current_page = "Energy & CO₂ Optimizer"
        if st.sidebar.button("Maintenance Forecaster"):
            st.session_state.current_page = "Maintenance Forecaster"
        if st.sidebar.button("Disaster Assessor"):
            st.session_state.current_page = "Disaster Assessor"
        if st.sidebar.button("Traffic Forecaster"):
            st.session_state.current_page = "Traffic Forecaster"
        if st.sidebar.button("Procurement Planner"):
            st.session_state.current_page = "Procurement Planner"
        if st.sidebar.button("Connectivity Insights"):
            st.session_state.current_page = "Connectivity Insights"
        if st.sidebar.button("Deployment Strategist"):
            st.session_state.current_page = "Deployment Strategist"
        if st.sidebar.button("Network Node Monitor"):
            st.session_state.current_page = "Network Node Monitor"
        if st.sidebar.button("Sustainability Tracker"):
            st.session_state.current_page = "Sustainability Tracker"

        # Default page if no page is selected
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Dashboard"

        # Render the selected page
        if st.session_state.current_page == "Dashboard":
            dashboard_page()
        elif st.session_state.current_page == "Settings":
            settings_page()
        elif st.session_state.current_page == "Energy & CO₂ Optimizer":
            energy_co2_optimizer()
        elif st.session_state.current_page == "Maintenance Forecaster":
            maintenance_forecaster()
        elif st.session_state.current_page == "Disaster Assessor":
            disaster_assessor()
        elif st.session_state.current_page == "Traffic Forecaster":
            traffic_forecaster()
        elif st.session_state.current_page == "Procurement Planner":
            procurement_planner()
        elif st.session_state.current_page == "Connectivity Insights":
            connectivity_insights()
        elif st.session_state.current_page == "Deployment Strategist":
            deployment_strategist()
        elif st.session_state.current_page == "Network Node Monitor":
            network_node_monitor()
        elif st.session_state.current_page == "Sustainability Tracker":
            sustainability_tracker()

if __name__ == "__main__":
    main()
