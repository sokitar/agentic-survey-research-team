"""
Cost-Tracked LLM Wrapper
Wraps CrewAI LLM to automatically track API costs and token usage.
"""
import logging
from typing import Optional, Any, Dict, List
from crewai import LLM
from cost_tracker import CostTracker, get_cost_tracker


class TrackedLLM:
    """LLM wrapper that automatically tracks costs and token usage"""
    
    def __init__(self, 
                 model: str, 
                 api_key: str,
                 cost_tracker: Optional[CostTracker] = None,
                 logger: Optional[logging.Logger] = None):
        self.model = model
        self.api_key = api_key
        self.cost_tracker = cost_tracker or get_cost_tracker()
        self.logger = logger or logging.getLogger(__name__)
        
        # Create the underlying CrewAI LLM
        self.llm = LLM(model=model, api_key=api_key)
        
        # Track which agent is currently using this LLM
        self.current_agent = "Unknown"
        self.current_task = "Unknown Task"
        
        self.logger.info(f"TrackedLLM initialized for model: {model}")
    
    def set_context(self, agent_name: str, task_description: str = ""):
        """Set the current agent context for cost tracking"""
        self.current_agent = agent_name
        self.current_task = task_description
        self.logger.debug(f"LLM context set - Agent: {agent_name}, Task: {task_description}")
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough estimation of token count (approximate: 4 chars = 1 token)"""
        return max(1, len(text) // 4)
    
    def _parse_response_usage(self, response: Any) -> tuple:
        """Parse token usage from API response"""
        # Try to extract actual token usage from response
        try:
            if hasattr(response, 'usage'):
                input_tokens = getattr(response.usage, 'input_tokens', 0)
                output_tokens = getattr(response.usage, 'output_tokens', 0)
                return input_tokens, output_tokens
            elif hasattr(response, 'token_usage'):
                usage = response.token_usage
                input_tokens = getattr(usage, 'prompt_tokens', 0)
                output_tokens = getattr(usage, 'completion_tokens', 0)
                return input_tokens, output_tokens
        except Exception as e:
            self.logger.debug(f"Could not parse token usage from response: {e}")
        
        # Fallback to estimation if actual usage not available
        return None, None
    
    def call(self, messages: List[Dict], **kwargs) -> Any:
        """Make API call with cost tracking"""
        # Estimate input tokens from messages
        input_text = ""
        for message in messages:
            if isinstance(message, dict) and 'content' in message:
                input_text += str(message['content']) + " "
        
        estimated_input_tokens = self._estimate_tokens(input_text)
        
        try:
            # Make the actual API call
            response = self.llm.call(messages, **kwargs)
            
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
            
            # Track the cost
            self.cost_tracker.track_api_call(
                agent_name=self.current_agent,
                model=self.model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                task_description=self.current_task
            )
            
            self.logger.debug(f"API call tracked - Agent: {self.current_agent}, "
                             f"Input: {input_tokens}, Output: {output_tokens}")
            
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
