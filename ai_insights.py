import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Load environment variables
load_dotenv()

class BaziInsights:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro")
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=False
        )
        
        # Add a separate conversation chain for general chat
        self.general_memory = ConversationBufferMemory()
        self.general_conversation = ConversationChain(
            llm=self.llm,
            memory=self.general_memory,
            verbose=False
        )

    def generate_personality_insights(self, bazi_chart: Dict[str, Any]) -> str:
        """Generate personality insights based on Bazi chart."""
        prompt = ChatPromptTemplate.from_template("""
        As a Bazi expert, analyze this Bazi chart and provide personality insights:
        
        Chart details:
        Year Pillar: {year_pillar}
        Month Pillar: {month_pillar}
        Day Pillar: {day_pillar}
        Hour Pillar: {hour_pillar}
        Day Officer: {day_officer}
        
        Please provide insights about:
        1. Core personality traits
        2. Natural talents and strengths
        3. Potential challenges
        Keep the response concise and practical.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke(bazi_chart)
        return response.content

    def generate_daily_insights(self, bazi_chart: Dict[str, Any], daily_data: Dict[str, Any]) -> str:
        """Generate daily insights based on Bazi chart and daily data."""
        prompt = ChatPromptTemplate.from_template("""
        As a Bazi expert, provide daily insights based on:
        
        Person's Bazi Chart:
        {bazi_chart}
        
        Today's Bazi Data:
        Day Officer: {day_officer}
        Favorable Elements: {favorable_elements}
        Unfavorable Elements: {unfavorable_elements}
        
        Please provide:
        1. Overall day outlook
        2. Favorable activities
        3. Activities to avoid
        Keep the response concise and practical.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({
            "bazi_chart": str(bazi_chart),
            **daily_data
        })
        return response.content

    def chat_response(self, user_question: str, bazi_chart: Dict[str, Any]) -> str:
        """Generate response to user's Bazi-related questions."""
        response = self.conversation.predict(
            input=f"""Context - User's Bazi Chart: {str(bazi_chart)}\n\nQuestion: {user_question}"""
        )
        return response

    def general_chat_response(self, user_input: str, user_context: Dict[str, Any] = None) -> str:
        """Generate response for general conversation."""
        context = ""
        if user_context:
            context = f"Context - Speaking with {user_context.get('name', 'User')}"
            if user_context.get('purpose'):
                context += f", who is here for {user_context.get('purpose')}"
            context += ".\n\n"
            
        response = self.general_conversation.predict(
            input=f"{context}User: {user_input}"
        )
        return response
