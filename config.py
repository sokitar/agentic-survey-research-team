"""
Configuration management for the Agentic Survey Research Team
"""
import os
import logging
from dotenv import load_dotenv
from crewai import LLM
from cost_tracker import initialize_cost_tracking, get_cost_tracker
from tracked_llm import create_tracked_llm

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the application"""
    
    def __init__(self, enable_cost_tracking=True):
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        # Cost tracking configuration
        self.enable_cost_tracking = enable_cost_tracking
        self.daily_budget = float(os.getenv('DAILY_COST_BUDGET', '10.0'))
        self.session_budget = float(os.getenv('SESSION_COST_BUDGET', '5.0'))
        self.model = "anthropic/claude-sonnet-4-20250514"
        
        # Initialize cost tracking if enabled
        if self.enable_cost_tracking:
            self.cost_tracker = initialize_cost_tracking(
                daily_budget=self.daily_budget,
                session_budget=self.session_budget
            )
    
    def get_llm(self, agent_name="Unknown"):
        """Get configured LLM instance for CrewAI with optional cost tracking"""
        if self.enable_cost_tracking:
            return create_tracked_llm(
                model=self.model,
                api_key=self.anthropic_api_key,
                agent_name=agent_name
            )
        else:
            return LLM(
                model=self.model,
                api_key=self.anthropic_api_key
            )
    
    def get_cost_summary(self):
        """Get current cost summary if tracking is enabled"""
        if self.enable_cost_tracking and hasattr(self, 'cost_tracker'):
            return self.cost_tracker.get_cost_summary()
        return None
    
    def print_cost_summary(self):
        """Print cost summary if tracking is enabled"""
        if self.enable_cost_tracking and hasattr(self, 'cost_tracker'):
            self.cost_tracker.print_cost_summary()

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
