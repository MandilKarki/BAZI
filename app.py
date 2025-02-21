import streamlit as st
from datetime import datetime
from bazi_engine import BaziEngine
from ai_insights import BaziInsights
from utils import validate_birth_datetime, format_bazi_data

# Initialize our engines
bazi_engine = BaziEngine()
ai_engine = BaziInsights()

# Set page config
st.set_page_config(
    page_title="Bazi Insights System",
    page_icon="",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .stApp {
        background: #f8f9fa;
    }
    .main {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .chat-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input {
        background-color: white;
    }
    h1 {
        color: #2C3E50;
    }
    h2 {
        color: #34495E;
    }
    h3 {
        color: #2980B9;
    }
    .stTab {
        background-color: white;
        color: #2C3E50;
        border-radius: 5px;
        padding: 10px;
        margin: 5px;
    }
    .stMarkdown {
        color: #2C3E50;
    }
    .st-emotion-cache-1y4p8pa {
        padding: 2rem;
        border-radius: 10px;
        background-color: white;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .st-emotion-cache-1gulkj5 {
        background-color: #E8F5E9;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .st-emotion-cache-16idsys {
        font-size: 16px;
        color: #2C3E50;
    }
    .st-emotion-cache-1vbkxwb {
        color: #2C3E50;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'bazi_chart' not in st.session_state:
    st.session_state.bazi_chart = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'general_chat_history' not in st.session_state:
    st.session_state.general_chat_history = []
if 'name' not in st.session_state:
    st.session_state.name = None
if 'purpose' not in st.session_state:
    st.session_state.purpose = None

# Sidebar for user information
with st.sidebar:
    st.markdown("""
        <h1 style='color: #2C3E50; font-size: 24px;'>Welcome to Bazi Insights</h1>
    """, unsafe_allow_html=True)
    if not st.session_state.name:
        st.session_state.name = st.text_input("What's your name?")
    if not st.session_state.purpose:
        st.session_state.purpose = st.selectbox(
            "What brings you here today?",
            ["Personal Growth", "Career", "Relationships", "Health", "Other"]
        )
    
    st.markdown("---")
    st.markdown("### Your Bazi Journey")
    if st.session_state.bazi_chart:
        st.success("✅ Bazi Chart Generated")
    else:
        st.info("🔵 Start by generating your Bazi chart")

# Main content area
st.markdown("""
    <h1 style='color: #2C3E50; text-align: center; margin-bottom: 30px;'>
        AI-Powered Bazi Insights System
    </h1>
""", unsafe_allow_html=True)

# Tabs for different features
tab1, tab2, tab3, tab4 = st.tabs(["Generate Bazi Chart", "Daily Insights", "Bazi Chat", "General Chat"])

with tab1:
    st.header("Generate Your Bazi Chart")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        birth_date = st.date_input("Birth Date")
    with col2:
        birth_time = st.time_input("Birth Time")
    with col3:
        timezone = st.text_input("Timezone (e.g., UTC+8)")
    
    if st.button("Generate Bazi Chart"):
        if timezone:
            date_str = birth_date.strftime("%Y-%m-%d")
            time_str = birth_time.strftime("%H:%M")
            
            if validate_birth_datetime(date_str, time_str, timezone):
                st.session_state.bazi_chart = bazi_engine.generate_chart(date_str, time_str, timezone)
                
                st.markdown("### Your Bazi Chart")
                st.code(format_bazi_data(st.session_state.bazi_chart))
                
                st.markdown("### Personality Insights")
                with st.spinner("Generating insights..."):
                    insights = ai_engine.generate_personality_insights(st.session_state.bazi_chart)
                st.markdown(insights)
            else:
                st.error("Please check your input format")
        else:
            st.warning("Please enter your timezone")

with tab2:
    st.header("Daily Bazi Insights")
    
    if not st.session_state.bazi_chart:
        st.warning("Please generate your Bazi chart first in the 'Generate Bazi Chart' tab")
    else:
        selected_date = st.date_input("Select Date for Insights")
        
        if st.button("Get Daily Insights"):
            date_str = selected_date.strftime("%Y-%m-%d")
            daily_data = bazi_engine.get_daily_bazi(date_str)
            
            st.markdown("### Daily Bazi Elements")
            st.json(daily_data)
            
            st.markdown("### Your Daily Insights")
            with st.spinner("Generating daily insights..."):
                insights = ai_engine.generate_daily_insights(st.session_state.bazi_chart, daily_data)
            st.markdown(insights)

with tab3:
    st.header("Chat about Your Bazi Chart")
    
    if not st.session_state.bazi_chart:
        st.warning("Please generate your Bazi chart first in the 'Generate Bazi Chart' tab")
    else:
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        user_question = st.chat_input("Ask anything about your Bazi chart...")
        
        if user_question:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = ai_engine.chat_response(user_question, st.session_state.bazi_chart)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

with tab4:
    st.markdown("""
        <h2 style='color: #2C3E50; margin-bottom: 20px;'>
            Let's Chat About Anything!
        </h2>
    """, unsafe_allow_html=True)
    
    # Create a container for the chat
    chat_container = st.container()
    
    with chat_container:
        # Display general chat history with improved styling
        for message in st.session_state.general_chat_history:
            with st.chat_message(message["role"], avatar="🧑" if message["role"] == "user" else "🤖"):
                st.markdown(f"""
                    <div style='
                        background-color: {"#E3F2FD" if message["role"] == "assistant" else "#F5F5F5"};
                        padding: 15px;
                        border-radius: 15px;
                        margin: 5px 0;
                        color: #2C3E50;
                    '>
                        {message["content"]}
                    </div>
                """, unsafe_allow_html=True)
    
    # Chat input with improved styling
    st.markdown("""
        <div style='
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: white;
            padding: 20px;
            border-top: 1px solid #eee;
        '>
        </div>
    """, unsafe_allow_html=True)
    
    user_input = st.chat_input("Chat with me about anything...", key="general_chat")
    
    if user_input:
        # Add user message to chat history
        st.session_state.general_chat_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                user_context = {
                    "name": st.session_state.name,
                    "purpose": st.session_state.purpose
                }
                response = ai_engine.general_chat_response(user_input, user_context)
            st.markdown(f"""
                <div style='
                    background-color: #E3F2FD;
                    padding: 15px;
                    border-radius: 15px;
                    margin: 5px 0;
                    color: #2C3E50;
                '>
                    {response}
                </div>
            """, unsafe_allow_html=True)
            st.session_state.general_chat_history.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown("Made with by the Bazi Insights Team")
