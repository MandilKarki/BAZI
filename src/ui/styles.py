"""
UI styles and theme configuration for the BAZI Profile System.
"""
import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app."""
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #121212;
            color: #FFFFFF;
        }
        .main {
            background-color: #282828;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .details-card {
            background-color: #1E1E1E;
            padding: 2rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        .success-message {
            background-color: #1E4620;
            color: #4CAF50;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
            text-align: center;
        }
        .bazi-analysis {
            background-color: #1E1E1E;
            padding: 2rem;
            border-radius: 8px;
            margin-top: 2rem;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            padding: 0.75rem 2rem;
            border-radius: 4px;
            border: none;
            transition: background-color 0.3s;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        h1, h2, h3 {
            color: #4CAF50;
        }
        .stSelectbox label, .stTextInput label {
            color: #B3B3B3;
        }
        </style>
    """, unsafe_allow_html=True)

def display_bazi_element(chinese: str, english: str, element_type: str):
    """
    Display a BAZI element with custom styling.
    Args:
        chinese: Chinese character
        english: English translation
        element_type: Type of element (e.g., 'Year', 'Month', 'Day')
    """
    st.markdown(f"""
        <div style='
            background-color: #1E1E1E;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border-left: 4px solid #4CAF50;
        '>
            <p style='margin: 0; color: #B3B3B3;'>{element_type}</p>
            <h3 style='margin: 0.5rem 0; color: #4CAF50;'>{chinese}</h3>
            <p style='margin: 0; color: #FFFFFF;'>{english}</p>
        </div>
    """, unsafe_allow_html=True)
