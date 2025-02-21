from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
import requests

# Load environment variables
load_dotenv()

# Configure Google Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
PROMPTLAYER_API_KEY = os.getenv('PROMPTLAYER_API_KEY')

def log_to_promptlayer(prompt, response, function_name="gemini_bazi_chat"):
    url = "https://api.promptlayer.com/rest/track-request"
    
    data = {
        "api_key": PROMPTLAYER_API_KEY,
        "function_name": function_name,
        "prompt": prompt,
        "response": response,
        "tags": ["test", "bazi_chat"],
    }
    
    response = requests.post(url, json=data)
    return response.json()

def test_prompt_layer():
    # Test data
    test_profile = {
        "name": "Test User",
        "birth_date": "1990-01-01",
        "birth_time": "12:00",
        "birth_timezone": "UTC",
        "elements": {
            "day_master": "Yang Wood",
            "favorable_elements": ["Fire", "Earth"],
            "unfavorable_elements": ["Metal", "Water"]
        }
    }

    test_daily_bazi = {
        "date": "2025-02-21",
        "day_pillar": {
            "heavenly_stem": "Ding",
            "earthly_branch": "Wei",
            "hidden_elements": ["Earth", "Metal", "Wood"]
        }
    }

    # Format the prompt directly since we created it in the UI
    formatted_prompt = f"""You are a Bazi expert assistant specializing in Chinese Metaphysics and destiny analysis.

Context:
User Profile: {json.dumps(test_profile, indent=2)}
Daily Bazi Information: {json.dumps(test_daily_bazi, indent=2)}

Previous conversation: []

User: What does my daily chart look like today?

Instructions:
- Analyze the user's Bazi chart in relation to their question
- Provide specific insights based on the elements, stems, and branches
- When discussing relationships between elements, explain the reasoning
- Keep responses concise but informative
- If temporal advice is needed, reference the daily Bazi data"""

    print("Testing PromptLayer Integration...")
    print("\nFormatted Prompt:")
    print(formatted_prompt)
    print("\nSending request to Gemini...")

    try:
        # Create Gemini model
        model = genai.GenerativeModel('gemini-pro')
        
        # Generate response
        response = model.generate_content(formatted_prompt)
        
        print("\nResponse from Gemini:")
        print(response.text)

        # Log to PromptLayer
        pl_response = log_to_promptlayer(formatted_prompt, response.text)

        print("\nRequest logged to PromptLayer")
        print(f"Request ID: {pl_response.get('request_id')}")
        print("You can view this request in your PromptLayer dashboard")

    except Exception as e:
        print(f"\nError during test: {str(e)}")

if __name__ == "__main__":
    test_prompt_layer()
