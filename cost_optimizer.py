"""
Cost Optimization Module for Agentic Survey Research Team
Provides intelligent cost management, caching, and prompt optimization.
"""
import hashlib
import json
import logging
import os
import sqlite3
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, asdict

from cost_tracker import get_cost_tracker, CostTracker


@dataclass
class CacheEntry:
    """Represents a cached LLM response"""
    query_hash: str
    query_text: str
    response: str
    agent_name: str
    timestamp: datetime
    cost_saved: float
    input_tokens: int
    output_tokens: int
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


class PromptOptimizer:
    """Optimizes prompts for better cost efficiency while maintaining quality"""
    
    def __init__(self):
        self.optimization_rules = {
            'remove_redundancy': True,
            'compress_examples': True,
            'optimize_structure': True,
            'reduce_verbosity': False  # Keep detailed for research quality
        }
    
    def optimize_prompt(self, prompt: str, agent_context: str = "") -> Tuple[str, int]:
        """
        Optimize a prompt for better token efficiency
        Returns: (optimized_prompt, tokens_saved)
        """
        original_length = len(prompt)
        optimized = prompt
        
        if self.optimization_rules['remove_redundancy']:
            optimized = self._remove_redundant_phrases(optimized)
        
        if self.optimization_rules['compress_examples']:
            optimized = self._compress_examples(optimized)
        
        if self.optimization_rules['optimize_structure']:
            optimized = self._optimize_structure(optimized, agent_context)
        
        # Estimate tokens saved (rough approximation: 4 chars = 1 token)
        tokens_saved = max(0, (original_length - len(optimized)) // 4)
        
        return optimized, tokens_saved
    
    def _remove_redundant_phrases(self, prompt: str) -> str:
        """Remove redundant phrases while preserving meaning"""
        # Common redundant patterns in research prompts
        redundant_patterns = [
            ('comprehensive and detailed', 'comprehensive'),
            ('analyze and examine', 'analyze'),
            ('identify and find', 'identify'),
            ('research and investigate', 'research'),
            ('please make sure to', 'ensure'),
            ('it is important to', ''),
            ('you should focus on', 'focus on'),
        ]
        
        result = prompt
        for old, new in redundant_patterns:
            result = result.replace(old, new)
        
        return result
    
    def _compress_examples(self, prompt: str) -> str:
        """Compress verbose examples while maintaining clarity"""
        # For research prompts, keep examples but make them more concise
        lines = prompt.split('\n')
        compressed_lines = []
        
        for line in lines:
            # Compress bullet point examples
            if line.strip().startswith('- ') and 'example:' in line.lower():
                # Keep the example but make it more concise
                line = line.replace('For example:', 'e.g.').replace('Such as:', 'e.g.')
            compressed_lines.append(line)
        
        return '\n'.join(compressed_lines)
    
    def _optimize_structure(self, prompt: str, agent_context: str) -> str:
        """Optimize prompt structure for specific agent context"""
        # Agent-specific optimizations
        if 'coordinator' in agent_context.lower():
            # Research coordinators need strategic focus
            prompt = prompt.replace('detailed analysis', 'strategic analysis')
            prompt = prompt.replace('comprehensive review', 'focused review')
        
        elif 'searcher' in agent_context.lower():
            # Literature searchers need precision
            prompt = prompt.replace('find all possible', 'find key')
            prompt = prompt.replace('exhaustive search', 'targeted search')
        
        elif 'analyzer' in agent_context.lower():
            # Analyzers need synthesis focus
            prompt = prompt.replace('list everything', 'synthesize key points')
        
        return prompt


class QueryCache:
    """Intelligent caching system for LLM responses to reduce costs"""
    
    def __init__(self, db_path: str = "cost_optimization.db", cache_duration_hours: int = 24):
        self.db_path = db_path
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.logger = logging.getLogger(__name__)
        self._init_cache_database()
    
    def _init_cache_database(self):
        """Initialize SQLite database for caching"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_hash TEXT UNIQUE NOT NULL,
                query_text TEXT NOT NULL,
                response TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                cost_saved REAL NOT NULL,
                input_tokens INTEGER NOT NULL,
                output_tokens INTEGER NOT NULL,
                hit_count INTEGER DEFAULT 1
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_query_hash ON query_cache(query_hash)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON query_cache(timestamp)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_agent ON query_cache(agent_name)
        """)
        
        conn.commit()
        conn.close()
        self.logger.info(f"Cache database initialized: {self.db_path}")
    
    def _generate_query_hash(self, query: str, agent_name: str) -> str:
        """Generate a hash for the query to use as cache key"""
        # Include agent name in hash to allow agent-specific caching
        cache_key = f"{agent_name}:{query.strip().lower()}"
        return hashlib.md5(cache_key.encode()).hexdigest()
    
    def get_cached_response(self, query: str, agent_name: str) -> Optional[str]:
        """Get cached response if available and not expired"""
        query_hash = self._generate_query_hash(query, agent_name)
        cutoff_time = datetime.now() - self.cache_duration
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT response, cost_saved, hit_count 
            FROM query_cache 
            WHERE query_hash = ? AND timestamp > ? AND agent_name = ?
        """, (query_hash, cutoff_time.isoformat(), agent_name))
        
        result = cursor.fetchone()
        
        if result:
            response, cost_saved, hit_count = result
            
            # Update hit count
            cursor.execute("""
                UPDATE query_cache 
                SET hit_count = hit_count + 1 
                WHERE query_hash = ? AND agent_name = ?
            """, (query_hash, agent_name))
            
            conn.commit()
            conn.close()
            
            # Track the cost savings
            cost_tracker = get_cost_tracker()
            self.logger.info(f"Cache hit for {agent_name} - Cost saved: ${cost_saved:.6f}")
            print(f"💰 Cache hit! Cost saved: ${cost_saved:.4f} (Total hits: {hit_count + 1})")
            
            return response
        
        conn.close()
        return None
    
    def cache_response(self, query: str, response: str, agent_name: str, 
                      input_tokens: int, output_tokens: int, cost: float):
        """Cache a response for future use"""
        query_hash = self._generate_query_hash(query, agent_name)
        
        cache_entry = CacheEntry(
            query_hash=query_hash,
            query_text=query[:500],  # Store truncated query for reference
            response=response,
            agent_name=agent_name,
            timestamp=datetime.now(),
            cost_saved=cost,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO query_cache 
                (query_hash, query_text, response, agent_name, timestamp, 
                 cost_saved, input_tokens, output_tokens, hit_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                cache_entry.query_hash,
                cache_entry.query_text,
                cache_entry.response,
                cache_entry.agent_name,
                cache_entry.timestamp.isoformat(),
                cache_entry.cost_saved,
                cache_entry.input_tokens,
                cache_entry.output_tokens
            ))
            
            conn.commit()
            self.logger.debug(f"Cached response for {agent_name} - Cost: ${cost:.6f}")
            
        except Exception as e:
            self.logger.error(f"Error caching response: {e}")
        finally:
            conn.close()
    
    def get_cache_stats(self) -> Dict:
        """Get caching statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total cache entries
        cursor.execute("SELECT COUNT(*) FROM query_cache")
        total_entries = cursor.fetchone()[0]
        
        # Total cost saved
        cursor.execute("SELECT SUM(cost_saved * hit_count) FROM query_cache")
        total_saved = cursor.fetchone()[0] or 0.0
        
        # Cache hits by agent
        cursor.execute("""
            SELECT agent_name, SUM(hit_count - 1) as cache_hits, SUM(cost_saved * (hit_count - 1)) as saved
            FROM query_cache 
            WHERE hit_count > 1
            GROUP BY agent_name
            ORDER BY saved DESC
        """)
        agent_stats = {row[0]: {'hits': row[1], 'saved': row[2]} for row in cursor.fetchall()}
        
        # Recent cache activity (last 24 hours)
        cutoff = datetime.now() - timedelta(hours=24)
        cursor.execute("""
            SELECT COUNT(*) FROM query_cache 
            WHERE timestamp > ?
        """, (cutoff.isoformat(),))
        recent_entries = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_entries': total_entries,
            'total_cost_saved': total_saved,
            'agent_stats': agent_stats,
            'recent_entries': recent_entries,
            'cache_duration_hours': self.cache_duration.total_seconds() / 3600
        }
    
    def cleanup_expired_cache(self):
        """Remove expired cache entries"""
        cutoff_time = datetime.now() - self.cache_duration
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM query_cache WHERE timestamp < ?
        """, (cutoff_time.isoformat(),))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted > 0:
            self.logger.info(f"Cleaned up {deleted} expired cache entries")
        
        return deleted


class CostBudgetManager:
    """Enhanced budget management with warnings, limits, and optimization suggestions"""
    
    def __init__(self, cost_tracker: Optional[CostTracker] = None):
        self.cost_tracker = cost_tracker or get_cost_tracker()
        self.logger = logging.getLogger(__name__)
        
        # Budget thresholds (can be configured via environment)
        self.daily_budget = float(os.getenv('DAILY_COST_BUDGET', '10.0'))
        self.session_budget = float(os.getenv('SESSION_COST_BUDGET', '5.0'))
        
        # Warning thresholds (percentages of budget)
        self.warning_threshold = 0.7  # 70%
        self.critical_threshold = 0.9  # 90%
        
        # Optimization suggestions
        self.optimization_tips = [
            "Consider using cached results for similar queries",
            "Try more specific prompts to reduce token usage",
            "Break large research tasks into smaller, focused queries",
            "Use agent-specific optimized prompts",
            "Enable prompt optimization to reduce redundancy"
        ]
    
    def check_budget_status(self) -> Dict[str, Any]:
        """Check current budget status and provide recommendations"""
        summary = self.cost_tracker.get_cost_summary()
        
        session_data = summary['current_session']
        daily_data = summary['today']
        
        session_usage = session_data['cost'] / session_data['budget'] if session_data['budget'] > 0 else 0
        daily_usage = daily_data['cost'] / daily_data['budget'] if daily_data['budget'] > 0 else 0
        
        status = {
            'session': self._get_usage_status(session_usage),
            'daily': self._get_usage_status(daily_usage),
            'session_usage_percent': session_usage * 100,
            'daily_usage_percent': daily_usage * 100,
            'recommendations': [],
            'should_continue': True
        }
        
        # Add recommendations based on usage
        if session_usage > self.critical_threshold:
            status['recommendations'].extend([
                "⚠️ Session budget critically low - consider ending session",
                "💡 Use 'cost' command to see detailed breakdown"
            ])
            status['should_continue'] = False
            
        elif session_usage > self.warning_threshold:
            status['recommendations'].extend([
                "⚠️ Session budget approaching limit",
                "💡 Consider enabling caching for remaining queries"
            ])
            
        if daily_usage > self.critical_threshold:
            status['recommendations'].extend([
                "⚠️ Daily budget critically low",
                "💡 Focus on essential queries only"
            ])
            
        elif daily_usage > self.warning_threshold:
            status['recommendations'].extend([
                "⚠️ Daily budget approaching limit",
                "💡 Consider prompt optimization"
            ])
        
        # Add general optimization tips if budget usage is moderate
        if 0.3 < max(session_usage, daily_usage) < 0.7:
            status['recommendations'].append(
                "💡 " + self.optimization_tips[hash(str(datetime.now().date())) % len(self.optimization_tips)]
            )
        
        return status
    
    def _get_usage_status(self, usage_percent: float) -> str:
        """Get status description for usage percentage"""
        if usage_percent >= 1.0:
            return "EXCEEDED"
        elif usage_percent >= self.critical_threshold:
            return "CRITICAL"
        elif usage_percent >= self.warning_threshold:
            return "WARNING"
        elif usage_percent >= 0.3:
            return "MODERATE"
        else:
            return "LOW"
    
    def get_cost_prediction(self, query: str, agent_name: str) -> Dict[str, Any]:
        """Predict cost for a query based on historical data"""
        # Simple prediction based on query length and agent history
        query_tokens = len(query) // 4  # Rough estimation
        
        # Get agent's average cost per token from history
        agent_costs = self.cost_tracker.get_agent_costs(timeframe_hours=168)  # Last week
        
        if agent_name in agent_costs and agent_costs[agent_name] > 0:
            # Rough prediction based on historical average
            predicted_cost = query_tokens * 0.003 / 1000  # Input cost approximation
            predicted_cost += query_tokens * 2 * 0.015 / 1000  # Output cost (assume 2:1 ratio)
        else:
            # Default prediction for new agents
            predicted_cost = query_tokens * 0.003 / 1000 + query_tokens * 1.5 * 0.015 / 1000
        
        return {
            'estimated_cost': predicted_cost,
            'estimated_input_tokens': query_tokens,
            'estimated_output_tokens': int(query_tokens * 1.5),
            'confidence': 'medium' if agent_name in agent_costs else 'low'
        }
    
    def suggest_optimizations(self, current_status: Dict) -> List[str]:
        """Suggest specific cost optimizations based on current status"""
        suggestions = []
        
        session_usage = current_status['session_usage_percent'] / 100
        daily_usage = current_status['daily_usage_percent'] / 100
        
        if session_usage > 0.8 or daily_usage > 0.8:
            suggestions.extend([
                "🎯 Use more specific prompts to reduce token usage",
                "📚 Check cache for similar previous queries",
                "⚡ Break complex queries into smaller parts"
            ])
        
        if session_usage > 0.5:
            suggestions.extend([
                "🔄 Enable query caching if not already active",
                "✂️ Use prompt optimization to remove redundancy",
                "📊 Review agent performance in cost analytics"
            ])
        
        return suggestions


def optimize_cost(agent_name: str, enable_caching: bool = True, enable_prompt_optimization: bool = True):
    """Decorator to add cost optimization to agent methods"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the instance (self) from args
            instance = args[0] if args else None
            
            # Initialize optimizers
            cache = QueryCache() if enable_caching else None
            prompt_optimizer = PromptOptimizer() if enable_prompt_optimization else None
            budget_manager = CostBudgetManager()
            
            # Check budget before proceeding
            budget_status = budget_manager.check_budget_status()
            
            if not budget_status['should_continue']:
                logger = logging.getLogger(__name__)
                logger.warning(f"Budget exceeded for {agent_name} - skipping operation")
                print("⚠️ Budget limit reached. Operation cancelled to prevent overspend.")
                return "Operation cancelled due to budget constraints."
            
            # Show budget warnings if needed
            if budget_status['recommendations']:
                for recommendation in budget_status['recommendations']:
                    print(recommendation)
            
            try:
                result = func(*args, **kwargs)
                logger = logging.getLogger(__name__)
                logger.info(f"Cost-optimized execution completed for {agent_name}")
                return result
                
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Error in cost-optimized {agent_name}: {e}")
                raise
                
        return wrapper
    return decorator


# Global instances for easy access
_global_cache: Optional[QueryCache] = None
_global_prompt_optimizer: Optional[PromptOptimizer] = None
_global_budget_manager: Optional[CostBudgetManager] = None

def get_query_cache() -> QueryCache:
    """Get or create global query cache instance"""
    global _global_cache
    if _global_cache is None:
        _global_cache = QueryCache()
    return _global_cache

def get_prompt_optimizer() -> PromptOptimizer:
    """Get or create global prompt optimizer instance"""
    global _global_prompt_optimizer
    if _global_prompt_optimizer is None:
        _global_prompt_optimizer = PromptOptimizer()
    return _global_prompt_optimizer

def get_budget_manager() -> CostBudgetManager:
    """Get or create global budget manager instance"""
    global _global_budget_manager
    if _global_budget_manager is None:
        _global_budget_manager = CostBudgetManager()
    return _global_budget_manager
