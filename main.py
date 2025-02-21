import streamlit as st
from datetime import datetime
import random
from pathlib import Path
import json
import os
import pandas as pd

def parse_date(date_str):
    """Try to parse date string in multiple formats."""
    date_formats = [
        "%Y-%m-%d",  # 2024-02-20
        "%d-%m-%Y",  # 20-02-2024
        "%m-%d-%Y",  # 02-20-2024
        "%d/%m/%Y",  # 20/02/2024
        "%m/%d/%Y",  # 02/20/2024
        "%Y/%m/%d",  # 2024/02/20
        "%d.%m.%Y",  # 20.02.2024
        "%m.%d.%Y",  # 02.20.2024
        "%Y.%m.%d",  # 2024.02.20
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def get_random_profile():
    """Get a random profile from the profiles directory."""
    profiles_dir = Path(__file__).parent / 'profiles'
    profile_files = list(profiles_dir.glob('baziprofiledata*.md'))
    if not profile_files:
        raise FileNotFoundError("No profile files found in the profiles directory")
    return random.choice(profile_files)

def save_user_profile(user_data):
    """Save user profile to a JSON file."""
    profiles_dir = Path(__file__).parent / 'user_profiles'
    profiles_dir.mkdir(exist_ok=True)
    
    # Create a filename from user's name
    safe_name = "".join(c for c in user_data["name"] if c.isalnum())
    filename = profiles_dir / f"{safe_name}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, indent=4)
    
    return filename

def load_user_profiles():
    """Load all user profiles."""
    profiles_dir = Path(__file__).parent / 'user_profiles'
    profiles = []
    
    if profiles_dir.exists():
        for file in profiles_dir.glob('*.json'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                    profiles.append(profile)
            except:
                continue
    
    return profiles

def load_user_profile(filename):
    """Load a specific user profile."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def load_daily_bazi():
    """Load daily Bazi data from CSV file."""
    try:
        df = pd.read_csv('Feb 2025 Bazi.csv')
        df['Date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
        return df
    except Exception as e:
        st.error(f"Error loading daily Bazi data: {str(e)}")
        return None

def get_bazi_for_date(date, df):
    """Get Bazi information for a specific date."""
    try:
        row = df[df['Date'].dt.date == date.date()].iloc[0]
        return {
            'Day Pillar': row['Day Pillar'],
            'Day Pillar English': row['Day Pillar English'],
            'Month Pillar': row['Month Pillar'],
            'Month Pillar English': row['Month Pillar English'],
            'Year Pillar': row['Year Pillar'],
            'Year Pillar English': row['Year Pillar English'],
            'Day Officer': row['Day Officer']
        }
    except:
        return None

def main():
    st.set_page_config(
        page_title="BAZI Profile System",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for dark modern styling
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

    # Load daily Bazi data
    daily_bazi_df = load_daily_bazi()

    # Add session state for storing the current profile
    if 'current_profile' not in st.session_state:
        st.session_state.current_profile = None

    # Sidebar for loading existing profiles and daily Bazi
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Choose Page", ["Profile Analysis", "Daily Bazi"])
        
        if page == "Profile Analysis":
            st.title("Saved Profiles")
            profiles = load_user_profiles()
            
            if profiles:
                profile_names = ["Select a profile..."] + [p["name"] for p in profiles]
                selected_profile = st.selectbox("Load existing profile:", profile_names)
                
                if selected_profile != "Select a profile...":
                    profile = next((p for p in profiles if p["name"] == selected_profile), None)
                    if profile:
                        st.session_state.current_profile = profile
                        st.success(f"Loaded profile for {profile['name']}")
            else:
                st.info("No saved profiles found")

    if page == "Profile Analysis":
        st.title("BAZI Profile System")
        st.markdown("<p style='font-size: 1.2rem; color: #B3B3B3;'>Enter your details below to receive your BAZI analysis</p>", unsafe_allow_html=True)

        # Create a card-like container for the form
        st.markdown("""
            <div class="details-card">
        """, unsafe_allow_html=True)
        
        # Create two columns for input fields
        col1, col2 = st.columns(2)

        # Pre-fill form if profile is loaded
        profile = st.session_state.current_profile

        with col1:
            name = st.text_input("Your Name", key="name", value=profile["name"] if profile else "")
            birth_date = st.date_input(
                "Birth Date",
                value=datetime.strptime(profile["birth_date"], "%b %d, %Y") if profile else None,
                min_value=datetime(1900, 1, 1),
                max_value=datetime.now(),
                key="birth_date"
            )
            birth_time = st.time_input(
                "Birth Time",
                value=datetime.strptime(profile["birth_time"], "%I:%M %p").time() if profile else None,
                key="birth_time"
            )

        with col2:
            timezone_options = [
                "UTC-12:00", "UTC-11:00", "UTC-10:00", "UTC-09:00", "UTC-08:00",
                "UTC-07:00", "UTC-06:00", "UTC-05:00", "UTC-04:00", "UTC-03:00",
                "UTC-02:00", "UTC-01:00", "UTC+00:00", "UTC+01:00", "UTC+02:00",
                "UTC+03:00", "UTC+04:00", "UTC+05:00", "UTC+05:30", "UTC+06:00",
                "UTC+07:00", "UTC+08:00", "UTC+09:00", "UTC+10:00", "UTC+11:00",
                "UTC+12:00"
            ]
            timezone = st.selectbox(
                "Timezone",
                timezone_options,
                index=timezone_options.index(profile["timezone"]) if profile and profile["timezone"] in timezone_options else 0,
                key="timezone"
            )
            location = st.text_input(
                "Birth Location (City, Country)",
                value=profile["location"] if profile else "",
                key="location"
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # Center the submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.button("Generate BAZI Analysis", use_container_width=True)

        if submit_button:
            if not name or not location:
                st.error("Please fill in all fields")
            else:
                try:
                    # Format the date and time
                    formatted_date = birth_date.strftime("%b %d, %Y")
                    formatted_time = birth_time.strftime("%I:%M %p")
                    
                    # Create user data dictionary
                    user_data = {
                        "name": name,
                        "birth_date": formatted_date,
                        "birth_time": formatted_time,
                        "timezone": timezone,
                        "location": location
                    }
                    
                    # Save the profile
                    save_user_profile(user_data)
                    
                    # Show confirmation with custom styling
                    st.markdown("""
                        <div class="success-message">
                            Information received and saved successfully!
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display user details in a card
                    st.markdown("""
                        <div class="details-card">
                            <h3>Your Details</h3>
                    """, unsafe_allow_html=True)
                    
                    st.write(f"**Name:** {name}")
                    st.write(f"**Birth Date:** {formatted_date}")
                    st.write(f"**Birth Time:** {formatted_time}")
                    st.write(f"**Timezone:** {timezone}")
                    st.write(f"**Location:** {location}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Get and display random profile for analysis
                    profile_path = get_random_profile()
                    
                    with st.spinner("Analyzing your BAZI chart..."):
                        # Add a small delay to show the spinner
                        import time
                        time.sleep(2)
                        
                        with open(profile_path, 'r', encoding='utf-8') as f:
                            profile_content = f.read()
                        
                        # Save the BAZI analysis with the user profile
                        user_data["bazi_analysis"] = profile_content
                        save_user_profile(user_data)
                        
                        st.markdown("""
                            <div class='bazi-analysis'>
                                <h3>Your BAZI Analysis</h3>
                        """, unsafe_allow_html=True)
                        st.markdown(profile_content)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

        # Display BAZI Analysis
        if st.session_state.current_profile and 'bazi_analysis' in st.session_state.current_profile:
            st.markdown("### Your BAZI Analysis")
            with st.container():
                st.markdown("""<div class="bazi-analysis">""", unsafe_allow_html=True)
                st.markdown(st.session_state.current_profile["bazi_analysis"])
                st.markdown("</div>", unsafe_allow_html=True)

    else:  # Daily Bazi page
        st.title("Daily Bazi")
        st.markdown("<div class='details-card'>", unsafe_allow_html=True)
        
        if daily_bazi_df is not None:
            selected_date = st.date_input("Select Date", datetime.now())
            daily_bazi = get_bazi_for_date(selected_date, daily_bazi_df)
            
            if daily_bazi:
                st.subheader("Daily Bazi Information")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Day Pillar:**", daily_bazi['Day Pillar'])
                    st.write("**Month Pillar:**", daily_bazi['Month Pillar'])
                    st.write("**Year Pillar:**", daily_bazi['Year Pillar'])
                    st.write("**Day Officer:**", daily_bazi['Day Officer'])
                
                with col2:
                    st.write("**Day Pillar (English):**", daily_bazi['Day Pillar English'])
                    st.write("**Month Pillar (English):**", daily_bazi['Month Pillar English'])
                    st.write("**Year Pillar (English):**", daily_bazi['Year Pillar English'])
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Add analysis section in a new card
                st.markdown("<div class='bazi-analysis'>", unsafe_allow_html=True)
                st.subheader("Daily Bazi Analysis")
                st.write("Analysis based on today's Bazi...")
                # Add your daily Bazi analysis logic here
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No Bazi information available for the selected date")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("Could not load daily Bazi data")
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
