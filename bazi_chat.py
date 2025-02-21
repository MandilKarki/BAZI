from typing import List, Dict
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

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
        
        # Create a custom prompt template that includes BAZI context
        template = """You are a knowledgeable BAZI (Chinese Metaphysics) consultant and advisor.

Current Context:
- User Profile: {profile_data}
- Daily BAZI Reading: {daily_bazi}

Previous conversation:
{history}

User Question: {question}
"""
        
        self.prompt = PromptTemplate(
            input_variables=["history", "profile_data", "daily_bazi", "question"],
            template=template
        )
        
        # Create the conversation chain
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            verbose=False
        )
    
    def get_response(self, user_input: str) -> str:
        """Get a response from the chatbot."""
        try:
            # Get response from the conversation chain
            response = self.conversation.predict(
                question=user_input,
                profile_data=str(self.profile_data),
                daily_bazi=str(self.daily_bazi) if self.daily_bazi else "No daily reading available",
                history=self.memory.chat_memory.messages
            )
            
            # Update the memory with the latest message
            self.memory.save_context({"input": user_input}, {"output": response})
            return response
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def update_daily_bazi(self, daily_bazi: Dict):
        """Update the daily BAZI information."""
        self.daily_bazi = daily_bazi
    
    def get_chat_history(self) -> List[Dict]:
        """Get the chat history."""
        return self.memory.chat_memory.messages
