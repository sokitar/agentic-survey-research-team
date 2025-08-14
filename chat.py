"""
Simple chat interface for the Agentic Survey Research Team
"""

import logging

class ChatInterface:
    """Simple terminal-based chat interface"""
    
    def __init__(self, logger=None, config=None):
        self.logger = logger or logging.getLogger(__name__)
        self.config = config
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
        elif command in ['cost', 'costs', 'budget']:
            self.display_cost_summary()
            return 'continue'
        elif command in ['cache', 'cache-stats']:
            self.display_cache_stats()
            return 'continue'
        elif command in ['optimize', 'optimization']:
            self.display_optimization_suggestions()
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
  • cost/budget - Show current cost tracking summary
  • cache - Show query caching statistics
  • optimize - Show cost optimization suggestions
  
💡 Research Tips:
  • Be specific about your research topic
  • Ask for surveys, comparisons, or specific papers
  • Example: "Find recent papers on transformer architectures"
        """
        print(help_text)
    
    def display_cache_stats(self):
        """Display caching statistics if available"""
        try:
            from cost_optimizer import get_query_cache
            cache = get_query_cache()
            stats = cache.get_cache_stats()
            
            print("\n" + "="*50)
            print("💾 QUERY CACHE STATISTICS")
            print("="*50)
            print(f"📄 Total cached queries: {stats['total_entries']}")
            print(f"💰 Total cost saved: ${stats['total_cost_saved']:.4f}")
            print(f"🕰️ Cache duration: {stats['cache_duration_hours']} hours")
            print(f"🆕 Recent cache entries (24h): {stats['recent_entries']}")
            
            if stats['agent_stats']:
                print("\n🤖 Agent Cache Performance:")
                for agent, data in stats['agent_stats'].items():
                    print(f"  {agent}: {data['hits']} hits, ${data['saved']:.4f} saved")
            
            print("="*50)
            
        except ImportError:
            print("\n💾 Cache statistics not available - cost optimization not loaded.")
        except Exception as e:
            print(f"\n⚠️ Error loading cache stats: {e}")
    
    def display_optimization_suggestions(self):
        """Display cost optimization suggestions"""
        try:
            from cost_optimizer import get_budget_manager
            budget_manager = get_budget_manager()
            status = budget_manager.check_budget_status()
            suggestions = budget_manager.suggest_optimizations(status)
            
            print("\n" + "="*50)
            print("⚡ COST OPTIMIZATION SUGGESTIONS")
            print("="*50)
            
            print(f"📊 Budget Status:")
            print(f"  Session: {status['session']} ({status['session_usage_percent']:.1f}% used)")
            print(f"  Daily: {status['daily']} ({status['daily_usage_percent']:.1f}% used)")
            
            if status['recommendations']:
                print("\n🎯 Current Recommendations:")
                for rec in status['recommendations']:
                    print(f"  {rec}")
            
            if suggestions:
                print("\n💡 Optimization Tips:")
                for tip in suggestions:
                    print(f"  {tip}")
            
            print("\n🚀 Available Optimizations:")
            print("  • Query caching (automatic)")
            print("  • Prompt optimization (automatic)")
            print("  • Budget monitoring (active)")
            print("  • Agent-specific cost tracking")
            
            print("="*50)
            
        except ImportError:
            print("\n⚡ Optimization suggestions not available - cost optimizer not loaded.")
        except Exception as e:
            print(f"\n⚠️ Error loading optimization suggestions: {e}")
    
    def display_cost_summary(self):
        """Display cost tracking summary if available"""
        if self.config and hasattr(self.config, 'print_cost_summary'):
            self.config.print_cost_summary()
        else:
            print("\n💰 Cost tracking not available in this session.")
    
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
                        
                        # Display cost summary after research completion
                        if self.config and hasattr(self.config, 'print_cost_summary'):
                            print("\n" + "-"*30 + " COST UPDATE " + "-"*30)
                            summary = self.config.get_cost_summary()
                            if summary:
                                session_cost = summary['current_session']['cost']
                                daily_cost = summary['today']['cost']
                                print(f"💰 Session cost: ${session_cost:.4f} | Daily total: ${daily_cost:.4f}")
                            print("-"*74)
                        
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
