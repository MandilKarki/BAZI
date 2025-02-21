Project: AI-Powered Bazi Insights System (V1 Prototype)
Purpose / Description

This project aims to develop a Bazi AI Insights system that takes a user’s birth date, time of birth, and timezone, generates their Bazi chart, and provides AI-generated insights.

This prototype will focus on three key features (Loops 1-3), using hardcoded Bazi chart data for now (instead of a full Bazi engine). For Loop 2, a CSV file will be used to look up daily Bazi data.
Key Features for V1 Prototype

    Loop 1: Given a person's birth date, time of birth, and timezone → Return a hardcoded Bazi chart and AI-generated personality insights.
    Loop 2: Given a person’s Bazi chart + a specific date's Bazi + Day Officer → Return AI-generated daily insights (using a CSV file for daily Bazi data).
    Loop 3: Allow users to chat with the AI and ask questions about their Bazi insights directly.

Instruction for the Coding Agent
Goal

    Phase 1 (Terminal-Based Prototype):
        Implement Loops 1-3 using LangChain + Gemini.
        Use hardcoded Bazi chart data.
        Use a CSV file for daily Bazi data (Loop 2).

    Phase 2 (Web-Based UI):
        Build a UI with Streamlit or Gradio.
        Extend chat functionality for user interaction.

Step-by-Step Tasks for the Coding Agent
1. Set Up Environment

    Use Python as the development language.
    Install required dependencies:
        langchain (for handling LLM prompts)
        google-generativeai (for Gemini API access)
        pandas (for handling CSV data in Loop 2)
        dotenv (for API key management)

2. Implement Input Handling

    Accept user input:
        Birth date (YYYY-MM-DD)
        Time of birth (HH:MM, 24-hour format)
        Timezone (UTC offset, e.g., UTC+8)

3. Implement Loop 1 (Basic Bazi Chart & Personality Insights)

    Use hardcoded Bazi chart data (no need for an engine yet).
    Create a structured prompt to generate personality insights from the Bazi chart using Gemini + LangChain.
    Format and print the AI-generated insights in the terminal.

4. Implement Loop 2 (Daily Bazi Insights)

    Use a CSV file to store daily Bazi data (e.g., Day Officer, favorable elements, etc.).
    Look up the Bazi data for a given date.
    Use LangChain + Gemini to generate AI insights for the day based on the person’s Bazi chart + daily data.

5. Implement Loop 3 (Chat with AI)

    Allow users to ask questions about their Bazi insights.
    Use LangChain's conversational memory to maintain context.

tech stack:
use langchain + Gemini and python to implement the AI.
