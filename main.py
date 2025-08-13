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
    print("💰 Cost tracking is enabled - monitoring API usage.")
    
    try:
        # Initialize configuration with cost tracking enabled
        config = Config(enable_cost_tracking=True)
        logger.info("Configuration loaded successfully with cost tracking")
        print("✅ Configuration loaded with cost tracking enabled")
        
        # Display initial cost summary
        config.print_cost_summary()
        
        # Initialize AI research team with cost-tracked LLM
        # The config.get_llm() method will automatically use tracked LLMs for each agent
        research_team = ResearchTeam(config.get_llm(), logger)
        
        # Start chat interface with research team and config for cost tracking
        chat = ChatInterface(logger, config)
        chat.run_chat_loop(research_team)
        
        # Display final cost summary
        print("\n" + "="*50)
        print("📊 FINAL SESSION SUMMARY")
        print("="*50)
        config.print_cost_summary()
        
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        print(f"❌ Error: {e}")
        print("Please check your .env file and API keys")

if __name__ == "__main__":
    main()
