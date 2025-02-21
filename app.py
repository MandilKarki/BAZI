"""
BAZI Profile System - Main Application
"""
import streamlit as st
from datetime import datetime
import pytz
from typing import Dict, Any

from src.bazi.profile import BaziProfileManager
from src.bazi.daily_reading import DailyBaziReader
from src.bazi.elements import get_element_relationship, get_element_properties
from src.utils.date_utils import parse_date, validate_birth_datetime
from src.ui.styles import apply_custom_styles, display_bazi_element
from bazi_chat import BaziChatbot

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'profile_manager' not in st.session_state:
        st.session_state.profile_manager = BaziProfileManager()
    
    if 'daily_reader' not in st.session_state:
        st.session_state.daily_reader = DailyBaziReader('data/daily_bazi.csv')
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="BAZI Profile System",
        page_icon="🔮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom styling
    apply_custom_styles()
    
    # Initialize session state
    initialize_session_state()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Profile", "Daily Reading", "Chat"])
    
    with tab1:
        render_profile_tab()
    
    with tab2:
        render_daily_reading_tab()
    
    with tab3:
        render_chat_tab()

def render_profile_tab():
    """Render the profile management tab."""
    st.markdown("<div class='details-card'>", unsafe_allow_html=True)
    st.subheader("BAZI Profile Management")
    
    # Profile creation form
    with st.form("profile_form"):
        name = st.text_input("Name")
        birth_date = st.text_input("Birth Date (YYYY-MM-DD)")
        birth_time = st.text_input("Birth Time (HH:MM)")
        timezone = st.selectbox("Timezone", options=pytz.all_timezones)
        
        if st.form_submit_button("Create Profile"):
            is_valid, error_msg = validate_birth_datetime(birth_date, birth_time, timezone)
            
            if is_valid:
                profile_data = {
                    "name": name,
                    "birth_date": birth_date,
                    "birth_time": birth_time,
                    "timezone": timezone
                }
                
                filename = st.session_state.profile_manager.save_profile(profile_data)
                st.success(f"Profile saved successfully: {filename}")
            else:
                st.error(error_msg)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_daily_reading_tab():
    """Render the daily BAZI reading tab."""
    st.markdown("<div class='bazi-analysis'>", unsafe_allow_html=True)
    st.subheader("Daily BAZI Reading")
    
    # Date selection
    selected_date = st.date_input("Select Date", datetime.now())
    
    if daily_reading := st.session_state.daily_reader.get_daily_reading(str(selected_date)):
        # Display BAZI elements
        col1, col2, col3 = st.columns(3)
        
        with col1:
            display_bazi_element(
                daily_reading['Year Pillar Chinese'],
                daily_reading['Year Pillar English'],
                'Year Pillar'
            )
        
        with col2:
            display_bazi_element(
                daily_reading['Month Pillar Chinese'],
                daily_reading['Month Pillar English'],
                'Month Pillar'
            )
        
        with col3:
            display_bazi_element(
                daily_reading['Day Pillar Chinese'],
                daily_reading['Day Pillar English'],
                'Day Pillar'
            )
        
        # Display element relationships
        st.markdown("### Element Relationships")
        day_element = daily_reading['Day Pillar English'].split()[0]
        month_element = daily_reading['Month Pillar English'].split()[0]
        year_element = daily_reading['Year Pillar English'].split()[0]
        
        st.write(f"Day-Month: {get_element_relationship(day_element, month_element)}")
        st.write(f"Day-Year: {get_element_relationship(day_element, year_element)}")
    else:
        st.warning("No BAZI reading available for selected date")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_chat_tab():
    """Render the chat interface tab."""
    st.markdown("<div class='bazi-analysis'>", unsafe_allow_html=True)
    st.subheader("Chat with Your BAZI Advisor")
    
    # Initialize or update chatbot
    if 'chatbot' not in st.session_state:
        profile = st.session_state.profile_manager.get_random_profile()
        daily_reading = st.session_state.daily_reader.get_daily_reading(
            str(datetime.now().date())
        )
        
        st.session_state.chatbot = BaziChatbot(
            profile_data=profile,
            daily_bazi=daily_reading
        )
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your BAZI reading..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display response
        response = st.session_state.chatbot.get_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
