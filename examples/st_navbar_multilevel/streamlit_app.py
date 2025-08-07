"""
Example of streamlit navigation bar with multilevel dropdown menus.

This example demonstrates how to use the new multilevel navigation feature
that supports hover dropdowns for nested menu items.
"""

import sys
import os
# Add the local development version to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set development mode to use the local Vue.js server
# os.environ["STREAMLIT_COMMUNITY_DEVELOPMENT"] = "1"

import streamlit as st
from streamlit_navigation_bar import st_navbar

# Configure the page
st.set_page_config(
    page_title="Multilevel Navigation Example",
    layout="wide"
)

# Define multilevel menu structure
pages = [
    "Home",  # Simple string page
    {
        "title": "Products",
        "icon": ":material/inventory:",
        "submenu": [
            "Laptops",
            "Smartphones",
            {"title": "Accessories", "icon": ":material/cable:"},
            "Support"
        ]
    },
    {
        "title": "Services",
        "icon": ":material/engineering:",
        "submenu": [
            "Consulting",
            {"title": "Development", "icon": ":material/code:"},
            {"title": "Maintenance", "icon": ":material/build:"}
        ]
    },
    "About",  # Simple string page
]

# Create navigation bar with multilevel menus
page = st_navbar(
    pages,
    styles={
        "nav": {
            "background-color": "rgb(123, 209, 146)",
        },
        "div": {
            "max-width": "32rem",
        },
        "span": {
            "border-radius": "0.5rem",
            "color": "rgb(49, 51, 63)",
            "margin": "0 0.125rem",
            "padding": "0.4375rem 0.625rem",
        },
        "active": {
            "background-color": "rgba(255, 255, 255, 0.25)",
        },
        "hover": {
            "background-color": "rgba(255, 255, 255, 0.35)",
        },
    }
)

# Display content based on selected page
st.title(f"Selected Page: {page}")

if page == "Home":
    st.write("Welcome to the home page!")
    st.write("This example demonstrates the multilevel navigation bar.")

elif page == "Products" or page in ["laptops", "smartphones", "accessories", "support"]:
    st.header("Products Section")
    if page == "laptops":
        st.write("Explore our laptop collection")
    elif page == "smartphones":
        st.write("Check out our smartphones")
    elif page == "accessories":
        st.write("Browse our accessories")
    elif page == "support":
        st.write("Get product support")
    else:
        st.write("Select a product category from the dropdown menu above")

elif page == "Services" or page in ["consulting", "development", "maintenance"]:
    st.header("Services Section")
    if page == "consulting":
        st.write("Learn about our consulting services")
    elif page == "development":
        st.write("Discover our development solutions")
    elif page == "maintenance":
        st.write("Explore our maintenance packages")
    else:
        st.write("Select a service from the dropdown menu above")

elif page == "About":
    st.header("About Us")
    st.write("This is the about page with company information.")

# Instructions
st.markdown("---")
st.markdown("### How to use multilevel navigation:")
st.markdown("""
1. **Hover over menu items** with dropdown arrows to see submenus
2. **Click on submenu items** to navigate to specific pages
3. **Multilevel structure** supports both simple strings and detailed dictionaries
4. **Icons** can be added to both main menu and submenu items using Material Icons

**Example structure:**
```python
pages = [
    "Simple Page",  # String for simple page
    {
        "title": "Main Menu",
        "icon": ":material/icon_name:",  # Optional
        "submenu": [
            "Sub Item 1",  # Simple string
            {"title": "Sub Item 2", "icon": ":material/icon:"}  # Dict with options
        ]
    }
]
```
""")

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    st.success("Done!")
