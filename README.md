# AI-Powered Bazi Insights System

This project provides AI-generated insights based on Bazi charts using LangChain and Google's Gemini AI.

## Features

1. Generate personality insights from Bazi charts
2. Provide daily Bazi insights
3. Interactive chat functionality for Bazi-related questions

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory and add your Gemini API key:
```
GOOGLE_API_KEY=your_api_key_here
```

3. Run the application:
```bash
python main.py
```

## Project Structure

- `main.py`: Main application entry point
- `bazi_engine.py`: Core Bazi chart processing logic
- `ai_insights.py`: AI insight generation using LangChain and Gemini
- `data/`: Directory containing CSV files for daily Bazi data
- `utils.py`: Utility functions
