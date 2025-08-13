#!/usr/bin/env python3
"""
Agentic Survey Research Team
A simple chat interface for AI-powered research paper analysis
"""

from config import Config, setup_logging

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
        print("(Chat interface coming next...)")
        
    except Exception as e:
        logger.error(f"Configuration error: {e}")
        print(f"❌ Error: {e}")
        print("Please check your .env file and API keys")

if __name__ == "__main__":
    main()
