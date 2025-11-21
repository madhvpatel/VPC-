"""
Configuration for AI provider and model settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the AI Relationship Manager"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Model Configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-pro")
    
    # Server Configuration
    PORT = int(os.getenv("PORT", 8000))
    
    # Determine which AI provider to use
    @staticmethod
    def get_ai_provider():
        """Determine which AI provider to use based on available API keys"""
        if Config.GOOGLE_API_KEY:
            return "google"
        elif Config.OPENAI_API_KEY:
            return "openai"
        elif Config.ANTHROPIC_API_KEY:
            return "anthropic"
        else:
            raise ValueError(
                "No API key found. Please set GOOGLE_API_KEY, OPENAI_API_KEY, "
                "or ANTHROPIC_API_KEY in your .env file"
            )
    
    @staticmethod
    def get_llm():
        """Get the appropriate LLM based on configuration"""
        provider = Config.get_ai_provider()
        
        if provider == "google":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                model=Config.MODEL_NAME,
                google_api_key=Config.GOOGLE_API_KEY,
                temperature=0.7,
                convert_system_message_to_human=True
            )
        elif provider == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=Config.MODEL_NAME,
                openai_api_key=Config.OPENAI_API_KEY,
                temperature=0.7
            )
        elif provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=Config.MODEL_NAME,
                anthropic_api_key=Config.ANTHROPIC_API_KEY,
                temperature=0.7
            )
