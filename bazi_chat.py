from typing import Dict, List, Generator, Union
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from langchain.callbacks.base import BaseCallbackHandler
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class StreamingCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming LLM responses."""
    
    def __init__(self):
        self.streaming_func = None

    def set_streaming_func(self, func):
        self.streaming_func = func

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Stream tokens as they are generated."""
        if self.streaming_func:
            self.streaming_func(token)

class BaziChatbot:
    def __init__(self, profile_data: Dict, daily_bazi: Dict = None):
        """Initialize the BAZI chatbot with user profile and optional daily reading."""
        self.profile_data = profile_data
        self.daily_bazi = daily_bazi
        
        # Create streaming callback handler
        self.stream_handler = StreamingCallbackHandler()
        
        # Initialize the LangChain Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.6,  # Balanced temperature for natural yet consistent responses
            convert_system_message_to_human=True,
            google_api_key=os.getenv('GOOGLE_API_KEY'),
            streaming=True,
            callbacks=[self.stream_handler]
        )
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="history",
            input_key="input",
            output_key="output",
            return_messages=True
        )
        
        # Create a custom prompt template that includes BAZI context
        template = """You are a friendly and conversational BAZI advisor named Mei. Adapt your response style to the question:
- For simple queries, keep responses brief and friendly
- For questions about BAZI concepts or analysis, provide detailed explanations when needed
- Break down longer explanations into clear sections
- Always maintain a conversational tone

Context (reference only when relevant):
User Profile: {profile_data}
Daily Reading: {daily_bazi}

Chat History:
{history}

User: {input}
Mei: """
        
        self.prompt = PromptTemplate(
            input_variables=["input", "profile_data", "daily_bazi", "history"],
            template=template
        )
        
        # Create the conversation chain
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory,
            output_key="output",
            verbose=False
        )

    def get_response(self, user_input: str, stream_func=None) -> Union[str, Generator[str, None, None]]:
        """
        Get a response from the chatbot based on user input and context.
        
        Args:
            user_input: The user's question or input
            stream_func: Optional callback function to handle streaming tokens
            
        Returns:
            If stream_func is provided, returns None (streams through callback)
            Otherwise, returns the complete response as a string
        """
        try:
            # Set streaming callback if provided
            if stream_func:
                self.stream_handler.set_streaming_func(stream_func)
            
            # Format chat history
            history = self.memory.chat_memory.messages
            formatted_history = "\n".join([
                f"User: {msg.content if isinstance(msg, HumanMessage) else ''}\nAI: {msg.content if isinstance(msg, AIMessage) else ''}"
                for msg in history
            ]) if history else ""

            # Get response from the conversation chain
            response = self.conversation({
                "input": user_input,
                "profile_data": str(self.profile_data),
                "daily_bazi": str(self.daily_bazi) if self.daily_bazi else "No daily reading available",
                "history": formatted_history
            })
            
            # Return the complete response if not streaming
            return response["output"]

        except Exception as e:
            print(f"Error in get_response: {str(e)}")  # Log the error
            return f"I apologize, but I encountered an error: {str(e)}"

    def update_daily_bazi(self, daily_bazi: Dict):
        """Update the daily BAZI reading data."""
        self.daily_bazi = daily_bazi
    
    def get_chat_history(self) -> List[Dict]:
        """Retrieve the conversation history."""
        return [
            {"role": "user" if isinstance(msg, HumanMessage) else "ai", 
             "content": msg.content}
            for msg in self.memory.chat_memory.messages
        ]
