"""
Cost-Tracked LLM Wrapper
Wraps CrewAI LLM to automatically track API costs and token usage.
"""
import logging
from typing import Optional, Any, Dict, List
from crewai import LLM
from cost_tracker import CostTracker, get_cost_tracker
try:
    from cost_optimizer import QueryCache, PromptOptimizer, get_query_cache, get_prompt_optimizer
except ImportError:
    # Cost optimization features not available
    QueryCache = None
    PromptOptimizer = None
    get_query_cache = lambda: None
    get_prompt_optimizer = lambda: None


class TrackedLLM:
    """LLM wrapper that automatically tracks costs, enables caching, and optimizes prompts"""
    
    def __init__(self, 
                 model: str, 
                 api_key: str,
                 cost_tracker: Optional[CostTracker] = None,
                 enable_caching: bool = True,
                 enable_prompt_optimization: bool = True,
                 logger: Optional[logging.Logger] = None):
        self.model = model
        self.api_key = api_key
        self.cost_tracker = cost_tracker or get_cost_tracker()
        self.logger = logger or logging.getLogger(__name__)
        
        # Cost optimization features
        self.enable_caching = enable_caching and QueryCache is not None
        self.enable_prompt_optimization = enable_prompt_optimization and PromptOptimizer is not None
        
        if self.enable_caching:
            self.cache = get_query_cache()
        
        if self.enable_prompt_optimization:
            self.prompt_optimizer = get_prompt_optimizer()
        
        # Create the underlying CrewAI LLM
        self.llm = LLM(model=model, api_key=api_key)
        
        # Track which agent is currently using this LLM
        self.current_agent = "Unknown"
        self.current_task = "Unknown Task"
        
        optimization_features = []
        if self.enable_caching:
            optimization_features.append("caching")
        if self.enable_prompt_optimization:
            optimization_features.append("prompt optimization")
        
        features_str = ", ".join(optimization_features) if optimization_features else "cost tracking only"
        self.logger.info(f"TrackedLLM initialized for model: {model} with {features_str}")
    
    def set_context(self, agent_name: str, task_description: str = ""):
        """Set the current agent context for cost tracking"""
        self.current_agent = agent_name
        self.current_task = task_description
        self.logger.debug(f"LLM context set - Agent: {agent_name}, Task: {task_description}")
    
    def _estimate_tokens(self, text: str) -> int:
        """Better estimation of token count using Claude's tokenization patterns"""
        if not text:
            return 0
        
        # More accurate token estimation for Claude models
        # Claude typically uses ~3.5-4 characters per token on average
        # We'll use a more conservative estimate to avoid underestimating costs
        
        # Basic character count approach with some adjustments
        char_count = len(str(text))
        
        # Adjust for common patterns:
        # - Spaces and punctuation typically use fewer characters per token
        # - Technical terms and code might use more
        word_count = len(str(text).split())
        
        # Use a hybrid approach: character count with word-based adjustment
        # Average of 3.2 chars per token (slightly conservative)
        estimated_tokens = max(1, int(char_count / 3.2))
        
        # Ensure we have at least as many tokens as words (very conservative floor)
        estimated_tokens = max(estimated_tokens, word_count)
        
        self.logger.debug(f"Token estimation: {char_count} chars, {word_count} words -> {estimated_tokens} tokens")
        return estimated_tokens
    
    def _parse_response_usage(self, response: Any) -> tuple:
        """Parse token usage from API response"""
        # Try multiple approaches to extract actual token usage from response
        try:
            # Method 1: Direct usage attribute
            if hasattr(response, 'usage'):
                usage = response.usage
                if hasattr(usage, 'input_tokens') and hasattr(usage, 'output_tokens'):
                    return usage.input_tokens, usage.output_tokens
                elif hasattr(usage, 'prompt_tokens') and hasattr(usage, 'completion_tokens'):
                    return usage.prompt_tokens, usage.completion_tokens
            
            # Method 2: Token usage attribute
            if hasattr(response, 'token_usage'):
                usage = response.token_usage
                if hasattr(usage, 'input_tokens') and hasattr(usage, 'output_tokens'):
                    return usage.input_tokens, usage.output_tokens
                elif hasattr(usage, 'prompt_tokens') and hasattr(usage, 'completion_tokens'):
                    return usage.prompt_tokens, usage.completion_tokens
            
            # Method 3: Check if response is a dict with usage info
            if isinstance(response, dict):
                if 'usage' in response:
                    usage = response['usage']
                    if 'input_tokens' in usage and 'output_tokens' in usage:
                        return usage['input_tokens'], usage['output_tokens']
                    elif 'prompt_tokens' in usage and 'completion_tokens' in usage:
                        return usage['prompt_tokens'], usage['completion_tokens']
            
            # Method 4: Check response content for Claude-specific patterns
            response_str = str(response)
            if 'input_tokens' in response_str and 'output_tokens' in response_str:
                # Try to parse from string representation
                import re
                input_match = re.search(r'input_tokens["\']?:\s*(\d+)', response_str)
                output_match = re.search(r'output_tokens["\']?:\s*(\d+)', response_str)
                if input_match and output_match:
                    return int(input_match.group(1)), int(output_match.group(1))
            
            # Log response structure for debugging
            self.logger.debug(f"Response type: {type(response)}")
            self.logger.debug(f"Response attributes: {dir(response)}")
            if hasattr(response, '__dict__'):
                self.logger.debug(f"Response dict: {response.__dict__}")
                
        except Exception as e:
            self.logger.debug(f"Could not parse token usage from response: {e}")
        
        # Fallback to estimation if actual usage not available
        return None, None
    
    def call(self, messages: List[Dict], **kwargs) -> Any:
        """Make API call with cost tracking, caching, and optimization"""
        # Extract text content from messages
        input_text = ""
        original_messages = messages.copy()
        
        for message in messages:
            if isinstance(message, dict) and 'content' in message:
                input_text += str(message['content']) + " "
        
        # Check cache first if enabled
        if self.enable_caching and self.cache:
            cached_response = self.cache.get_cached_response(input_text, self.current_agent)
            if cached_response:
                return cached_response
        
        # Optimize prompts if enabled
        optimized_messages = original_messages
        tokens_saved = 0
        
        if self.enable_prompt_optimization and self.prompt_optimizer:
            optimized_messages = []
            for message in original_messages:
                if isinstance(message, dict) and 'content' in message:
                    optimized_content, saved = self.prompt_optimizer.optimize_prompt(
                        message['content'], self.current_agent
                    )
                    tokens_saved += saved
                    
                    # Create new message with optimized content
                    optimized_message = message.copy()
                    optimized_message['content'] = optimized_content
                    optimized_messages.append(optimized_message)
                else:
                    optimized_messages.append(message)
            
            if tokens_saved > 0:
                self.logger.info(f"Prompt optimization saved ~{tokens_saved} tokens for {self.current_agent}")
                print(f"✂️ Prompt optimized: ~{tokens_saved} tokens saved")
        
        # Update input text after optimization
        optimized_input_text = ""
        for message in optimized_messages:
            if isinstance(message, dict) and 'content' in message:
                optimized_input_text += str(message['content']) + " "
        
        estimated_input_tokens = self._estimate_tokens(optimized_input_text)
        
        try:
            # Make the actual API call with optimized messages
            response = self.llm.call(optimized_messages, **kwargs)
            
            # Try to get actual token usage from response
            actual_input_tokens, actual_output_tokens = self._parse_response_usage(response)
            
            # Use actual tokens if available, otherwise estimate
            if actual_input_tokens is not None and actual_output_tokens is not None:
                input_tokens = actual_input_tokens
                output_tokens = actual_output_tokens
            else:
                # Fallback to estimation
                input_tokens = estimated_input_tokens
                # Estimate output tokens from response
                if hasattr(response, 'content'):
                    output_tokens = self._estimate_tokens(str(response.content))
                elif isinstance(response, str):
                    output_tokens = self._estimate_tokens(response)
                else:
                    output_tokens = self._estimate_tokens(str(response))
            
            # Calculate cost for this call
            cost = self.cost_tracker.calculate_cost(self.model, input_tokens, output_tokens)
            
            # Cache the response if caching is enabled
            if self.enable_caching and self.cache:
                response_str = str(response)
                self.cache.cache_response(
                    query=input_text,  # Use original query for cache key consistency
                    response=response_str,
                    agent_name=self.current_agent,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost=cost
                )
            
            # Track the cost
            self.cost_tracker.track_api_call(
                agent_name=self.current_agent,
                model=self.model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                task_description=self.current_task
            )
            
            self.logger.debug(f"API call tracked - Agent: {self.current_agent}, "
                             f"Input: {input_tokens}, Output: {output_tokens}, Cost: ${cost:.6f}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in tracked LLM call: {e}")
            # Still track the input tokens even if call failed
            self.cost_tracker.track_api_call(
                agent_name=self.current_agent,
                model=self.model,
                input_tokens=estimated_input_tokens,
                output_tokens=0,
                task_description=f"FAILED: {self.current_task}"
            )
            raise
    
    # Delegate other methods to the underlying LLM
    def __getattr__(self, name):
        """Delegate unknown methods to the underlying LLM"""
        return getattr(self.llm, name)


class TrackedLLMManager:
    """Manages tracked LLM instances for different agents"""
    
    def __init__(self, cost_tracker: Optional[CostTracker] = None):
        self.cost_tracker = cost_tracker or get_cost_tracker()
        self.llm_instances: Dict[str, TrackedLLM] = {}
        self.logger = logging.getLogger(__name__)
    
    def get_tracked_llm(self, model: str, api_key: str, agent_name: str) -> TrackedLLM:
        """Get or create a tracked LLM for an agent"""
        # Use model as key since agents might share the same model
        if model not in self.llm_instances:
            self.llm_instances[model] = TrackedLLM(
                model=model,
                api_key=api_key,
                cost_tracker=self.cost_tracker,
                logger=self.logger
            )
            self.logger.info(f"Created tracked LLM for model: {model}")
        
        # Set agent context
        llm = self.llm_instances[model]
        llm.set_context(agent_name)
        
        return llm
    
    def set_agent_context(self, model: str, agent_name: str, task_description: str = ""):
        """Update agent context for an existing LLM"""
        if model in self.llm_instances:
            self.llm_instances[model].set_context(agent_name, task_description)
    
    def get_all_tracked_llms(self) -> Dict[str, TrackedLLM]:
        """Get all tracked LLM instances"""
        return self.llm_instances.copy()


# Global LLM manager instance
_global_llm_manager: Optional[TrackedLLMManager] = None

def get_llm_manager() -> TrackedLLMManager:
    """Get or create global LLM manager"""
    global _global_llm_manager
    if _global_llm_manager is None:
        _global_llm_manager = TrackedLLMManager()
    return _global_llm_manager


def create_tracked_llm(model: str, api_key: str, agent_name: str = "Unknown") -> TrackedLLM:
    """Convenience function to create a tracked LLM"""
    manager = get_llm_manager()
    return manager.get_tracked_llm(model, api_key, agent_name)
