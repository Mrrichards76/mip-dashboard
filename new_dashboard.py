import streamlit as st
import sqlite3

# Connect to your database
conn = sqlite3.connect("mip_live.db")
cursor = conn.cursor()

# Fetch all data
cursor.execute("SELECT * FROM mip_live")
rows = cursor.fetchall()
conn.close()

# Display in Streamlit
st.title("MIP Dashboard")
st.write("Database preview:", rows)
