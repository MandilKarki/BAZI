from typing import List, Dict
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from promptlayer import PromptLayer

# Load environment variables
load_dotenv()

# Configure Gemini and PromptLayer
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
promptlayer_client = PromptLayer(api_key=os.getenv('PROMPTLAYER_API_KEY'), enable_tracing=True)

class BaziChatbot:
    def __init__(self, profile_data: Dict, daily_bazi: Dict = None):
        self.profile_data = profile_data
        self.daily_bazi = daily_bazi
        
        # Initialize the Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
    
    @promptlayer_client.traceable
    def get_response(self, user_input: str) -> str:
        try:
            # Prepare input variables
            input_variables = {
                "profile": str(self.profile_data),
                "daily_bazi": str(self.daily_bazi) if self.daily_bazi else "No daily Bazi data available",
                "history": str(self.memory.chat_memory.messages),
                "user_input": user_input
            }

            # Run the prompt through PromptLayer
            response = promptlayer_client.run(
                prompt_name="bazi_chat_template",
                input_variables=input_variables,
                llm_provider="google",  # Specify we're using Google's Gemini
                llm_kwargs={
                    "model": "gemini-pro",
                    "temperature": 0.7
                },
                tags=["bazi_chat"],
                metadata={
                    "profile_name": self.profile_data.get("name", "unknown"),
                    "has_daily_bazi": bool(self.daily_bazi)
                }
            )

            # Extract the response content
            result = response["raw_response"].text

            # Update conversation memory
            self.memory.save_context({"input": user_input}, {"output": result})

            return result

        except Exception as e:
            print(f"Error in get_response: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def update_daily_bazi(self, daily_bazi: Dict):
        """Update the daily BAZI information."""
        self.daily_bazi = daily_bazi
    
    def get_chat_history(self) -> List[Dict]:
        """Get the chat history."""
        return self.memory.chat_memory.messages
