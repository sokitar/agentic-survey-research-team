"""
Configuration management for the Agentic Survey Research Team
"""
import os
import logging
from dotenv import load_dotenv
from crewai import LLM

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the application"""
    
    def __init__(self):
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def get_llm(self):
        """Get configured LLM instance for CrewAI"""
        return LLM(
            model="anthropic/claude-sonnet-4-20250514",
            api_key=self.anthropic_api_key
        )

def setup_logging():
    """Configure basic logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
