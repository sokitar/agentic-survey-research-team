#!/usr/bin/env python3
"""
Agentic Survey Research Team
A simple chat interface for AI-powered research paper analysis
"""

from config import Config, setup_logging
from chat import ChatInterface
from agents import ResearchTeam

def main():
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Agentic Survey Research Team")
    
    print("🔬 Agentic Survey Research Team")
    print("Welcome! I'll help you research any topic using AI agents.")
    
    try:
        # Initialize configuration
        config = Config()
        logger.info("Configuration loaded successfully")
        print("✅ Configuration loaded")
        
        # Initialize AI research team
        llm = config.get_llm()
        research_team = ResearchTeam(llm, logger)
        
        # Start chat interface with research team
        chat = ChatInterface(logger)
        chat.run_chat_loop(research_team)
        
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        print(f"❌ Error: {e}")
        print("Please check your .env file and API keys")

if __name__ == "__main__":
    main()
