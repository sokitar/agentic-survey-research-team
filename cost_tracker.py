"""
Cost Tracking Infrastructure for Agentic Survey Research Team
Monitors API usage, tracks costs, and provides real-time cost alerts.
"""
import sqlite3
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import os
from dataclasses import dataclass, asdict
from functools import wraps


@dataclass
class CostEvent:
    """Represents a single API cost event"""
    timestamp: datetime
    agent_name: str
    session_id: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    task_description: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


class CostTracker:
    """Comprehensive API cost tracking and monitoring system"""
    
    # Claude Sonnet 4 pricing (as of 2024 - update as needed)
    MODEL_PRICING = {
        "anthropic/claude-sonnet-4-20250514": {
            "input_per_1k": 0.003,   # $0.003 per 1K input tokens
            "output_per_1k": 0.015   # $0.015 per 1K output tokens
        },
        "anthropic/claude-3-sonnet-20240229": {
            "input_per_1k": 0.003,
            "output_per_1k": 0.015
        }
    }
    
    def __init__(self, db_path: str = "cost_tracking.db", logger: Optional[logging.Logger] = None):
        self.db_path = db_path
        self.logger = logger or logging.getLogger(__name__)
        self.current_session_id = self._generate_session_id()
        self._init_database()
        
        # Cost alerts configuration
        self.daily_budget = float(os.getenv('DAILY_COST_BUDGET', '10.0'))  # $10 default
        self.session_budget = float(os.getenv('SESSION_COST_BUDGET', '5.0'))  # $5 default
        
        self.logger.info(f"Cost tracker initialized - Session: {self.current_session_id}")
        self.logger.info(f"Daily budget: ${self.daily_budget}, Session budget: ${self.session_budget}")
    
    def _generate_session_id(self) -> str:
        """Generate unique session identifier"""
        return f"session_{int(time.time())}"
    
    def _init_database(self):
        """Initialize SQLite database for cost tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cost_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                session_id TEXT NOT NULL,
                model TEXT NOT NULL,
                input_tokens INTEGER NOT NULL,
                output_tokens INTEGER NOT NULL,
                cost_usd REAL NOT NULL,
                task_description TEXT
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON cost_events(timestamp)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_session ON cost_events(session_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_agent ON cost_events(agent_name)
        """)
        
        conn.commit()
        conn.close()
        self.logger.info(f"Database initialized: {self.db_path}")
    
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for given token usage"""
        if model not in self.MODEL_PRICING:
            self.logger.warning(f"Unknown model {model}, using default pricing")
            model = "anthropic/claude-sonnet-4-20250514"
        
        pricing = self.MODEL_PRICING[model]
        input_cost = (input_tokens / 1000) * pricing["input_per_1k"]
        output_cost = (output_tokens / 1000) * pricing["output_per_1k"]
        total_cost = input_cost + output_cost
        
        return round(total_cost, 6)
    
    def track_api_call(self, 
                      agent_name: str, 
                      model: str, 
                      input_tokens: int, 
                      output_tokens: int, 
                      task_description: str = "") -> CostEvent:
        """Track a single API call and return cost event"""
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        
        event = CostEvent(
            timestamp=datetime.now(),
            agent_name=agent_name,
            session_id=self.current_session_id,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            task_description=task_description
        )
        
        # Store in database
        self._store_event(event)
        
        # Check for budget alerts
        self._check_budget_alerts(event)
        
        # Log the event
        self.logger.info(f"API Call - Agent: {agent_name}, Cost: ${cost:.4f}, "
                        f"Tokens: {input_tokens}in/{output_tokens}out")
        
        return event
    
    def _store_event(self, event: CostEvent):
        """Store cost event in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO cost_events 
            (timestamp, agent_name, session_id, model, input_tokens, output_tokens, cost_usd, task_description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.timestamp.isoformat(),
            event.agent_name,
            event.session_id,
            event.model,
            event.input_tokens,
            event.output_tokens,
            event.cost_usd,
            event.task_description
        ))
        
        conn.commit()
        conn.close()
    
    def _check_budget_alerts(self, event: CostEvent):
        """Check and alert for budget exceeded"""
        # Check session budget
        session_cost = self.get_session_cost(self.current_session_id)
        if session_cost > self.session_budget:
            self.logger.warning(f"⚠️ SESSION BUDGET EXCEEDED: ${session_cost:.4f} > ${self.session_budget}")
            print(f"⚠️ WARNING: Session budget exceeded! Current: ${session_cost:.4f}, Budget: ${self.session_budget}")
        
        # Check daily budget
        daily_cost = self.get_daily_cost()
        if daily_cost > self.daily_budget:
            self.logger.warning(f"⚠️ DAILY BUDGET EXCEEDED: ${daily_cost:.4f} > ${self.daily_budget}")
            print(f"⚠️ WARNING: Daily budget exceeded! Current: ${daily_cost:.4f}, Budget: ${self.daily_budget}")
    
    def get_session_cost(self, session_id: str = None) -> float:
        """Get total cost for a session"""
        if session_id is None:
            session_id = self.current_session_id
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(cost_usd) FROM cost_events WHERE session_id = ?
        """, (session_id,))
        
        result = cursor.fetchone()[0]
        conn.close()
        
        return result or 0.0
    
    def get_daily_cost(self, date: datetime = None) -> float:
        """Get total cost for a specific date"""
        if date is None:
            date = datetime.now()
        
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(cost_usd) FROM cost_events 
            WHERE timestamp >= ? AND timestamp < ?
        """, (start_of_day.isoformat(), end_of_day.isoformat()))
        
        result = cursor.fetchone()[0]
        conn.close()
        
        return result or 0.0
    
    def get_agent_costs(self, timeframe_hours: int = 24) -> Dict[str, float]:
        """Get cost breakdown by agent for specified timeframe"""
        cutoff = datetime.now() - timedelta(hours=timeframe_hours)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT agent_name, SUM(cost_usd) 
            FROM cost_events 
            WHERE timestamp >= ?
            GROUP BY agent_name
            ORDER BY SUM(cost_usd) DESC
        """, (cutoff.isoformat(),))
        
        results = cursor.fetchall()
        conn.close()
        
        return {agent: cost for agent, cost in results}
    
    def get_cost_summary(self) -> Dict:
        """Get comprehensive cost summary"""
        current_session_cost = self.get_session_cost()
        daily_cost = self.get_daily_cost()
        agent_costs = self.get_agent_costs()
        
        return {
            "current_session": {
                "session_id": self.current_session_id,
                "cost": current_session_cost,
                "budget": self.session_budget,
                "remaining": max(0, self.session_budget - current_session_cost)
            },
            "today": {
                "cost": daily_cost,
                "budget": self.daily_budget,
                "remaining": max(0, self.daily_budget - daily_cost)
            },
            "agent_breakdown": agent_costs
        }
    
    def print_cost_summary(self):
        """Print formatted cost summary"""
        summary = self.get_cost_summary()
        
        print("\n" + "="*50)
        print("💰 COST TRACKING SUMMARY")
        print("="*50)
        
        print(f"📊 Current Session ({summary['current_session']['session_id']}):")
        print(f"   Cost: ${summary['current_session']['cost']:.4f}")
        print(f"   Budget: ${summary['current_session']['budget']:.2f}")
        print(f"   Remaining: ${summary['current_session']['remaining']:.4f}")
        
        print(f"\n📅 Today:")
        print(f"   Cost: ${summary['today']['cost']:.4f}")
        print(f"   Budget: ${summary['today']['budget']:.2f}")
        print(f"   Remaining: ${summary['today']['remaining']:.4f}")
        
        if summary['agent_breakdown']:
            print(f"\n🤖 Agent Costs (Last 24h):")
            for agent, cost in summary['agent_breakdown'].items():
                print(f"   {agent}: ${cost:.4f}")
        
        print("="*50)


def track_llm_cost(agent_name: str, task_description: str = ""):
    """Decorator to automatically track LLM costs for agent methods"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Get the cost tracker from the agent instance
            cost_tracker = getattr(self, 'cost_tracker', None)
            if not cost_tracker:
                # If no cost tracker, just execute normally
                return func(self, *args, **kwargs)
            
            # Execute the function and track costs
            # Note: This is a basic implementation - would need to be adapted
            # based on how CrewAI exposes token usage information
            result = func(self, *args, **kwargs)
            
            # For now, we'll need to integrate with CrewAI's callback system
            # or modify the LLM calls to capture token usage
            self.logger.info(f"Cost tracking enabled for {agent_name}: {task_description}")
            
            return result
        return wrapper
    return decorator


# Global cost tracker instance
_global_cost_tracker: Optional[CostTracker] = None

def get_cost_tracker() -> CostTracker:
    """Get or create global cost tracker instance"""
    global _global_cost_tracker
    if _global_cost_tracker is None:
        _global_cost_tracker = CostTracker()
    return _global_cost_tracker

def initialize_cost_tracking(db_path: str = "cost_tracking.db", 
                           daily_budget: float = 10.0,
                           session_budget: float = 5.0) -> CostTracker:
    """Initialize global cost tracking with custom settings"""
    global _global_cost_tracker
    
    # Set environment variables for budgets
    os.environ['DAILY_COST_BUDGET'] = str(daily_budget)
    os.environ['SESSION_COST_BUDGET'] = str(session_budget)
    
    _global_cost_tracker = CostTracker(db_path)
    return _global_cost_tracker
