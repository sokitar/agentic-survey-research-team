"""
Simple chat interface for the Agentic Survey Research Team
"""

import logging

class ChatInterface:
    """Simple terminal-based chat interface"""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.conversation_history = []
    
    def display_welcome(self):
        """Display welcome message and instructions"""
        print("\n" + "="*60)
        print("🔬 Agentic Survey Research Team - Chat Interface")
        print("="*60)
        print("I'll help you research any academic topic using AI agents!")
        print("\nCommands:")
        print("  • Type your research question to start")
        print("  • Type 'quit' or 'exit' to leave")
        print("  • Type 'help' for more options")
        print("-"*60)
    
    def get_user_input(self):
        """Get user input with proper formatting"""
        try:
            user_input = input("\n👤 You: ").strip()
            if user_input:
                self.conversation_history.append({"role": "user", "message": user_input})
            return user_input
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            return "quit"
        except EOFError:
            return "quit"
    
    def display_response(self, response, agent_name="System"):
        """Display agent response with proper formatting"""
        print(f"\n🤖 {agent_name}: {response}")
        self.conversation_history.append({"role": agent_name.lower(), "message": response})
    
    def handle_command(self, user_input):
        """Handle special commands"""
        command = user_input.lower()
        
        if command in ['quit', 'exit']:
            return 'quit'
        elif command == 'help':
            self.display_help()
            return 'continue'
        elif command == 'history':
            self.display_history()
            return 'continue'
        else:
            return 'process'
    
    def display_help(self):
        """Display help information"""
        help_text = """
📚 Available Commands:
  • quit/exit - Leave the chat
  • help - Show this help message
  • history - Show conversation history
  
💡 Research Tips:
  • Be specific about your research topic
  • Ask for surveys, comparisons, or specific papers
  • Example: "Find recent papers on transformer architectures"
        """
        print(help_text)
    
    def display_history(self):
        """Display conversation history"""
        if not self.conversation_history:
            print("\n📝 No conversation history yet.")
            return
        
        print("\n📝 Conversation History:")
        print("-" * 40)
        for i, entry in enumerate(self.conversation_history, 1):
            role = entry['role'].title()
            message = entry['message'][:100] + "..." if len(entry['message']) > 100 else entry['message']
            print(f"{i}. {role}: {message}")
    
    def run_chat_loop(self, research_team=None):
        """Main chat loop with optional research team"""
        self.display_welcome()
        
        while True:
            user_input = self.get_user_input()
            
            if not user_input:
                continue
                
            action = self.handle_command(user_input)
            
            if action == 'quit':
                print("\n👋 Thanks for using Agentic Survey Research Team!")
                break
            elif action == 'continue':
                continue
            elif action == 'process':
                if research_team:
                    # Execute coordinated research with the team
                    try:
                        print("\n🚀 Activating multi-agent research team...")
                        result = research_team.execute_coordinated_research(user_input)
                        self.display_response(result, "Research Team")
                    except Exception as e:
                        self.logger.error(f"Research execution failed: {e}")
                        self.display_response(
                            f"Sorry, the research team encountered an error: {str(e)}",
                            "System"
                        )
                else:
                    # Fallback response if no team
                    self.display_response(
                        "I understand you want to research: '" + user_input + "'. " +
                        "The AI research team is being set up!",
                        "System"
                    )
        
        self.logger.info("Chat session ended")
