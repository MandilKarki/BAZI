import streamlit as st
from datetime import datetime
import random
from pathlib import Path
import json
import pandas as pd
from bazi_chat import BaziChatbot
import pytz
from typing import Dict, Any

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
        # Try to load the CSV file
        try:
            df = pd.read_csv('Feb 2025 Bazi.csv')
            
            # Clean any potential whitespace in column names and data
            df.columns = df.columns.str.strip()
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].str.strip()
            
            # Parse the date column
            def parse_date(date_str):
                try:
                    return pd.to_datetime(date_str, format='%a %m/%d/%Y')
                except:
                    # Try alternative format if the first one fails
                    return pd.to_datetime(date_str)
            
            df['Date'] = df['Date'].apply(parse_date)
            return df
            
        except Exception as e:
            st.error(f"Error loading Feb 2025 Bazi.csv: {str(e)}")
            return None
            
    except Exception as e:
        st.error(f"Error loading daily Bazi data: {str(e)}")
        return None

def get_bazi_for_date(date, df):
    """Get Bazi information for a specific date."""
    try:
        # Convert date to datetime.date for comparison
        if isinstance(date, str):
            date = pd.to_datetime(date).date()
        elif hasattr(date, 'date'):
            date = date.date()
            
        # Find matching row
        matching_rows = df[df['Date'].dt.date == date]
        if len(matching_rows) == 0:
            st.error(f"No data found for date: {date}")
            return None
            
        row = matching_rows.iloc[0]
        return {
            'Date': row['Date'],
            'Day Pillar': row['Day Pillar'],
            'Day Pillar English': row['Day Pillar English'],
            'Month Pillar': row['Month Pillar'],
            'Month Pillar English': row['Month Pillar English'],
            'Year Pillar': row['Year Pillar'],
            'Year Pillar English': row['Year Pillar English'],
            'Day Officer': row['Day Officer']
        }
    except Exception as e:
        st.error(f"Error finding Bazi for date: {str(e)}")
        return None

def display_bazi_element(chinese, english, element_type):
    """Display a Bazi element with styling."""
    st.markdown(f"""
        <div style="
            background-color: #1E1E1E;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border: 1px solid #333;
        ">
            <h4 style="color: #4CAF50; margin: 0;">{element_type}</h4>
            <div style="font-size: 1.2rem; margin: 0.5rem 0;">
                <span style="color: #FFD700;">{chinese}</span>
                <span style="color: #B3B3B3; margin-left: 1rem;">({english})</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def get_element_relationship(element1, element2):
    """Analyze the relationship between two elements."""
    # Define the five elements cycle
    productive_cycle = {
        'Wood': 'Fire',
        'Fire': 'Earth',
        'Earth': 'Metal',
        'Metal': 'Water',
        'Water': 'Wood'
    }
    
    controlling_cycle = {
        'Wood': 'Earth',
        'Earth': 'Water',
        'Water': 'Fire',
        'Fire': 'Metal',
        'Metal': 'Wood'
    }
    
    # Clean up element names
    element1 = element1.split()[-1]  # Get last word (e.g., "Yang Wood" -> "Wood")
    element2 = element2.split()[-1]
    
    if element2 == productive_cycle.get(element1):
        return f"{element1} produces {element2} - This is a productive and favorable relationship"
    elif element1 == productive_cycle.get(element2):
        return f"{element2} is produced by {element1} - This indicates support and nurturing"
    elif element2 == controlling_cycle.get(element1):
        return f"{element1} controls {element2} - This suggests influence and regulation"
    elif element1 == controlling_cycle.get(element2):
        return f"{element2} controls {element1} - This may indicate some challenges"
    else:
        return f"{element1} and {element2} have an indirect relationship"

def validate_birth_datetime(date_str: str, time_str: str, timezone_str: str) -> bool:
    """Validate birth date, time and timezone input."""
    try:
        # Validate date format
        datetime.strptime(date_str, "%Y-%m-%d")
        
        # Validate time format
        datetime.strptime(time_str, "%H:%M")
        
        # Validate timezone format (simple UTC offset validation)
        if not (timezone_str.startswith("UTC+") or timezone_str.startswith("UTC-")):
            return False
        int(timezone_str[4:])  # Should be a number after UTC+/-
        
        return True
    except ValueError:
        return False

def format_bazi_data(bazi_data: Dict[str, Any]) -> str:
    """Format Bazi data into a readable string."""
    return f"""
Year Pillar: {bazi_data['year_pillar']}
Month Pillar: {bazi_data['month_pillar']}
Day Pillar: {bazi_data['day_pillar']}
Hour Pillar: {bazi_data['hour_pillar']}
Day Officer: {bazi_data['day_officer']}
"""

def get_daily_bazi(date: str, daily_bazi_df: pd.DataFrame) -> Dict[str, Any]:
    """Get Bazi data for a specific date from CSV."""
    try:
        daily = daily_bazi_df[daily_bazi_df['date'] == date].iloc[0]
        return {
            "day_officer": daily["day_officer"],
            "favorable_elements": daily["favorable_elements"].split("-"),
            "unfavorable_elements": daily["unfavorable_elements"].split("-")
        }
    except (IndexError, KeyError):
        return {
            "day_officer": "Unknown",
            "favorable_elements": [],
            "unfavorable_elements": []
        }

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

    # Add session state for storing the current profile and view
    if 'current_profile' not in st.session_state:
        st.session_state.current_profile = None
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "profile_analysis"

    # Sidebar for profile selection
    with st.sidebar:
        st.title("Profile Selection")
        profiles = load_user_profiles()
        
        # New Profile Button
        if st.button("➕ Create New Profile", use_container_width=True):
            st.session_state.current_profile = None
            st.session_state.current_view = "profile_analysis"
        
        st.markdown("---")
        
        if profiles:
            st.subheader("Saved Profiles")
            for profile in profiles:
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(f"👤 {profile['name']}", key=f"profile_{profile['name']}", use_container_width=True):
                        st.session_state.current_profile = profile
                with col2:
                    if st.button("🗑️", key=f"delete_{profile['name']}", help="Delete profile"):
                        # Add delete functionality here
                        pass
        else:
            st.info("No saved profiles found")

    # Main content area
    st.title("BAZI Profile System")

    if st.session_state.current_profile is None:
        # Show new profile form
        st.markdown("<p style='font-size: 1.2rem; color: #B3B3B3;'>Enter your details below to create a new profile</p>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""<div class="details-card">""", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Your Name", key="name")
                birth_date = st.date_input(
                    "Birth Date",
                    min_value=datetime(1900, 1, 1),
                    max_value=datetime.now(),
                    key="birth_date"
                )
                birth_time = st.time_input("Birth Time", key="birth_time")

            with col2:
                timezone_options = [
                    "UTC-12:00", "UTC-11:00", "UTC-10:00", "UTC-09:00", "UTC-08:00",
                    "UTC-07:00", "UTC-06:00", "UTC-05:00", "UTC-04:00", "UTC-03:00",
                    "UTC-02:00", "UTC-01:00", "UTC+00:00", "UTC+01:00", "UTC+02:00",
                    "UTC+03:00", "UTC+04:00", "UTC+05:00", "UTC+05:30", "UTC+06:00",
                    "UTC+07:00", "UTC+08:00", "UTC+09:00", "UTC+10:00", "UTC+11:00",
                    "UTC+12:00"
                ]
                timezone = st.selectbox("Timezone", timezone_options, key="timezone")
                location = st.text_input("Birth Location (City, Country)", key="location")

            st.markdown("</div>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Create Profile", use_container_width=True):
                    if not name or not location:
                        st.error("Please fill in all fields")
                    else:
                        try:
                            formatted_date = birth_date.strftime("%b %d, %Y")
                            formatted_time = birth_time.strftime("%I:%M %p")
                            
                            user_data = {
                                "name": name,
                                "birth_date": formatted_date,
                                "birth_time": formatted_time,
                                "timezone": timezone,
                                "location": location
                            }
                            
                            # Get and generate initial BAZI analysis
                            profile_path = get_random_profile()
                            with open(profile_path, 'r', encoding='utf-8') as f:
                                profile_content = f.read()
                            user_data["bazi_analysis"] = profile_content
                            
                            save_user_profile(user_data)
                            st.session_state.current_profile = user_data
                            st.experimental_rerun()
                            
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")

    else:
        # Show profile view with tabs for analysis and daily bazi
        profile = st.session_state.current_profile
        
        # Profile header
        st.markdown(f"""
            <div class="details-card">
                <h3>Profile: {profile['name']}</h3>
                <p><strong>Birth Date:</strong> {profile['birth_date']}</p>
                <p><strong>Birth Time:</strong> {profile['birth_time']}</p>
                <p><strong>Location:</strong> {profile['location']}</p>
                <p><strong>Timezone:</strong> {profile['timezone']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # View selection tabs
        tab1, tab2, tab3 = st.tabs(["🔮 BAZI Analysis", "📅 Daily BAZI", "💬 BAZI Chat"])
        
        with tab1:
            if 'bazi_analysis' in profile:
                st.markdown("""<div class="bazi-analysis">""", unsafe_allow_html=True)
                st.markdown(profile['bazi_analysis'])
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No BAZI analysis available for this profile")
                
        with tab2:
            if daily_bazi_df is not None:
                st.markdown("<div class='details-card'>", unsafe_allow_html=True)
                
                # Date selection with prev/next buttons
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("◀️ Previous Day"):
                        if 'selected_date' in st.session_state:
                            st.session_state.selected_date = st.session_state.selected_date - pd.Timedelta(days=1)
                        else:
                            st.session_state.selected_date = pd.Timestamp.now() - pd.Timedelta(days=1)
                
                with col2:
                    if 'selected_date' not in st.session_state:
                        st.session_state.selected_date = pd.Timestamp.now()
                    selected_date = st.date_input("Select Date", st.session_state.selected_date)
                    st.session_state.selected_date = selected_date
                
                with col3:
                    if st.button("Next Day ▶️"):
                        if 'selected_date' in st.session_state:
                            st.session_state.selected_date = st.session_state.selected_date + pd.Timedelta(days=1)
                        else:
                            st.session_state.selected_date = pd.Timestamp.now() + pd.Timedelta(days=1)
                
                daily_bazi = get_bazi_for_date(st.session_state.selected_date, daily_bazi_df)
                
                if daily_bazi:
                    # Display Day Officer prominently
                    st.markdown(f"""
                        <div style="
                            background-color: #2E3B2F;
                            padding: 1rem;
                            border-radius: 8px;
                            margin: 1rem 0;
                            text-align: center;
                        ">
                            <h3 style="color: #4CAF50; margin: 0;">Day Officer: {daily_bazi['Day Officer']}</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display Pillars
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        display_bazi_element(
                            daily_bazi['Day Pillar'],
                            daily_bazi['Day Pillar English'],
                            "Day Pillar"
                        )
                    
                    with col2:
                        display_bazi_element(
                            daily_bazi['Month Pillar'],
                            daily_bazi['Month Pillar English'],
                            "Month Pillar"
                        )
                    
                    with col3:
                        display_bazi_element(
                            daily_bazi['Year Pillar'],
                            daily_bazi['Year Pillar English'],
                            "Year Pillar"
                        )
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Add personalized analysis section
                    st.markdown("<div class='bazi-analysis'>", unsafe_allow_html=True)
                    st.subheader(f"Daily BAZI Analysis for {profile['name']}")
                    
                    # Display the five elements analysis
                    st.markdown("""
                        <h4 style="color: #4CAF50;">Five Elements Analysis</h4>
                    """, unsafe_allow_html=True)
                    
                    # Extract elements from the pillars
                    day_element = daily_bazi['Day Pillar English'].split()[0]
                    month_element = daily_bazi['Month Pillar English'].split()[0]
                    year_element = daily_bazi['Year Pillar English'].split()[0]
                    
                    # Display element relationships
                    day_relationship_month = get_element_relationship(day_element, month_element)
                    day_relationship_year = get_element_relationship(day_element, year_element)
                    
                    st.write(f"""
                        **Day Element:** {day_element}
                        - Relationship with Month Element ({month_element}): {day_relationship_month}
                        - Relationship with Year Element ({year_element}): {day_relationship_year}
                    """)
                    
                    st.markdown("""
                        <h4 style="color: #4CAF50;">Personal Day Influence</h4>
                    """, unsafe_allow_html=True)
                    
                    # Add personalized analysis based on the Day Officer
                    day_officer_meanings = {
                        'Open': 'A day for new beginnings and starting projects. Good for initiating actions.',
                        'Close': 'A day for completing tasks and closing deals. Focus on finishing things.',
                        'Balance': 'A day for finding harmony and making balanced decisions.',
                        'Stable': 'A day for maintaining stability and routine tasks.',
                        'Remove': 'A day for clearing obstacles and removing negativity.',
                        'Full': 'A day of abundance and completion. Good for harvesting results.',
                        'Danger': 'A day to be cautious and avoid risky ventures.',
                        'Success': 'A day favorable for achieving goals and recognition.',
                        'Receive': 'A day for accepting and receiving benefits.',
                        'Establish': 'A day for establishing foundations and long-term plans.',
                        'Destruction': 'A day for breaking down old patterns, avoid major decisions.',
                        'Initiate': 'A day for taking initiative and leadership.'
                    }
                    
                    day_officer = daily_bazi['Day Officer']
                    day_meaning = day_officer_meanings.get(day_officer, 'A day to observe and act according to circumstances.')
                    
                    st.write(f"""
                        The Day Officer of "{day_officer}" suggests:
                        - {day_meaning}
                        - This combines with your {day_element} day element to influence your activities
                        - Consider the relationship between your day element and the current month's {month_element} energy
                    """)

                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning("No BAZI information available for the selected date")
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("Could not load daily BAZI data")

        with tab3:
            st.markdown("<div class='bazi-analysis'>", unsafe_allow_html=True)
            st.subheader("Chat with Your BAZI Advisor")
            
            # Initialize chatbot if not exists
            if 'chatbot' not in st.session_state:
                st.session_state.chatbot = BaziChatbot(
                    profile_data=profile,
                    daily_bazi=daily_bazi if daily_bazi_df is not None else None
                )
            
            # Update daily bazi in chatbot
            if daily_bazi_df is not None and daily_bazi:
                st.session_state.chatbot.update_daily_bazi(daily_bazi)
            
            # Initialize message history if not exists
            if 'messages' not in st.session_state:
                st.session_state.messages = []
            
            # Display chat history
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # Chat input
            if prompt := st.chat_input("Ask about your BAZI reading..."):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Display user message
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Get chatbot response
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing your BAZI..."):
                        try:
                            response = st.session_state.chatbot.get_response(prompt)
                            st.markdown(response)
                            # Add assistant response to chat history
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        except Exception as e:
                            error_message = f"I apologize, but I encountered an error: {str(e)}"
                            st.error(error_message)
                            st.session_state.messages.append({"role": "assistant", "content": error_message})
            
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
