# 🛠️ Developer Guide

## Welcome to Agentic Survey Research Team Development

This guide provides comprehensive information for developers who want to contribute to, extend, or understand the technical architecture of the Agentic Survey Research Team.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Development Setup](#development-setup)
3. [Code Structure](#code-structure)
4. [Contributing Guidelines](#contributing-guidelines)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Performance Optimization](#performance-optimization)
8. [Security Considerations](#security-considerations)

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACES                         │
├─────────────────────┬───────────────────────────────────────┤
│   Terminal Chat     │         Web Interface                 │
│   (chat.py)         │         (web_app.py)                  │
└─────────────────────┴───────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 CORE ORCHESTRATION                          │
├─────────────────────────────────────────────────────────────┤
│              Configuration (config.py)                     │
│           Research Team (agents.py)                        │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  AGENT LAYER                               │
├─────────────────────┬─────────────────┬───────────────────────┤
│ Research Coordinator│ Literature      │ Research Analyst     │
│                     │ Searcher        │ Report Writer        │
└─────────────────────┴─────────────────┴───────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 LLM ABSTRACTION                            │
├─────────────────────────────────────────────────────────────┤
│        Tracked LLM (tracked_llm.py)                        │
│          │                        │                        │
│   Cost Tracker          Cost Optimizer                     │
│   (cost_tracker.py)     (cost_optimizer.py)                │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 EXTERNAL SERVICES                          │
├─────────────────────────────────────────────────────────────┤
│         Anthropic Claude API                               │
│         SQLite Databases                                   │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. **Configuration Layer** (`config.py`)
- Environment variable management
- LLM initialization and configuration
- Cost tracking setup
- Logging configuration

#### 2. **Agent Orchestration** (`agents.py`)
- CrewAI agent definitions
- Task creation and management
- Multi-agent workflow coordination
- Research team orchestration

#### 3. **Cost Management System**
- **Cost Tracker** (`cost_tracker.py`): Real-time cost monitoring
- **Cost Optimizer** (`cost_optimizer.py`): Caching and optimization
- **Tracked LLM** (`tracked_llm.py`): LLM wrapper with cost tracking

#### 4. **User Interfaces**
- **Terminal Interface** (`chat.py`): Command-line interaction
- **Web Interface** (`frontend/web_app.py`): FastAPI web application

### Data Flow

```
User Query → Configuration → Research Team → Agents → TrackedLLM → 
Cost Tracking → API Call → Response → Cost Recording → User Output
```

## 🚀 Development Setup

### Prerequisites

- **Python 3.11+**
- **UV package manager**
- **Git**
- **Anthropic API key**

### Installation

1. **Clone and setup:**
   ```bash
   git clone https://github.com/sokitar/agentic-survey-research-team.git
   cd agentic-survey-research-team
   
   # Install dependencies
   uv install
   
   # Setup environment
   cp .env.example .env
   # Edit .env with your API key
   ```

2. **Development environment:**
   ```bash
   # Install development dependencies
   uv add --dev pytest pytest-asyncio black isort mypy
   
   # Setup pre-commit hooks
   uv add --dev pre-commit
   pre-commit install
   ```

3. **Database setup:**
   ```bash
   # Databases are created automatically on first run
   # For development, you may want to start fresh:
   rm -f cost_tracking.db cost_optimization.db
   ```

### Environment Variables

Create a `.env` file with:

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Development settings
DAILY_COST_BUDGET=10.0
SESSION_COST_BUDGET=5.0
CACHE_DURATION_HOURS=24

# Debug settings
LOG_LEVEL=INFO
DEBUG_MODE=False
```

## 📁 Code Structure

### Module Organization

```
agentic-survey-research-team/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── agents.py              # AI agent definitions
├── chat.py                # Terminal interface
├── cost_tracker.py        # Cost monitoring system
├── cost_optimizer.py      # Caching and optimization
├── tracked_llm.py         # LLM wrapper with tracking
├── frontend/              # Web interface
│   ├── web_app.py         # FastAPI application
│   └── templates/         # HTML templates
│       ├── base.html      # Base template
│       └── index.html     # Main dashboard
├── tests/                 # Test suite
│   ├── test_cost_tracking.py
│   └── test_cost_optimization.py
├── docs/                  # Documentation
│   ├── API.md
│   ├── USER_GUIDE.md
│   └── DEVELOPER.md
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── pyproject.toml         # Project configuration
├── COMMITS.md             # Development history
└── README.md              # Project overview
```

### Key Classes and Their Responsibilities

#### Configuration (`config.py`)
```python
class Config:
    """Main configuration class"""
    def __init__(self, enable_cost_tracking=True)
    def get_llm(self, agent_name="Unknown")  # Returns TrackedLLM
    def get_cost_summary()                   # Cost information
    def print_cost_summary()                 # Display costs
```

#### Research Team (`agents.py`)
```python
class ResearchTeam:
    """Orchestrates multi-agent research workflow"""
    def __init__(self, llm, logger=None)
    def execute_complete_research(self, query)  # Main workflow
    
class ResearchCoordinator:
    """Coordinates research strategy"""
    
class LiteratureSearcher:
    """Finds academic papers"""
    
class PaperAnalyzer:
    """Analyzes research findings"""
    
class ReportSynthesizer:
    """Generates final reports"""
```

#### Cost Management (`cost_tracker.py`)
```python
class CostTracker:
    """Tracks API costs and budget"""
    def track_api_call(self, agent_name, model, tokens...)
    def get_session_cost(self, session_id=None)
    def get_daily_cost(self, date=None)
    
@dataclass
class CostEvent:
    """Represents a cost event"""
    timestamp: datetime
    agent_name: str
    cost_usd: float
    # ... other fields
```

#### Optimization (`cost_optimizer.py`)
```python
class CostOptimizer:
    """Manages caching and optimization"""
    def get_cached_response(self, prompt_hash)
    def cache_response(self, prompt_hash, response)
    def optimize_prompt(self, prompt, agent_name)
```

### Design Patterns

#### 1. **Factory Pattern** (LLM Creation)
```python
def create_tracked_llm(model, api_key, agent_name="Unknown"):
    """Factory function for creating tracked LLM instances"""
    base_llm = LLM(model=model, api_key=api_key)
    cost_tracker = get_cost_tracker()
    cost_optimizer = CostOptimizer()
    return TrackedLLM(base_llm, cost_tracker, cost_optimizer, agent_name)
```

#### 2. **Decorator Pattern** (Cost Tracking)
```python
class TrackedLLM:
    """Wraps base LLM with cost tracking capabilities"""
    def __init__(self, base_llm, cost_tracker, cost_optimizer, agent_name):
        self.base_llm = base_llm
        self.cost_tracker = cost_tracker
        # ...
    
    def call(self, prompt, **kwargs):
        # Pre-processing: optimization, caching
        # LLM call
        # Post-processing: cost tracking
```

#### 3. **Observer Pattern** (Cost Alerts)
```python
class CostTracker:
    def _check_budget_alerts(self, event: CostEvent):
        """Automatically triggered after each cost event"""
        if session_cost > self.session_budget:
            self.logger.warning("Budget exceeded!")
```

## 🤝 Contributing Guidelines

### Code Style

We follow **PEP 8** with some specific guidelines:

```python
# Good: Descriptive function names
def execute_complete_research(self, query: str) -> str:
    """Execute the complete 4-agent research workflow."""
    
# Good: Type hints
def track_api_call(self, 
                  agent_name: str, 
                  model: str, 
                  input_tokens: int, 
                  output_tokens: int) -> CostEvent:

# Good: Comprehensive docstrings
def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost for given token usage.
    
    Args:
        model: The model identifier (e.g., 'anthropic/claude-sonnet-4-20250514')
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        
    Returns:
        Total cost in USD
        
    Raises:
        ValueError: If model is not supported
    """
```

### Development Workflow

#### 1. **Feature Development**
```bash
# Create feature branch
git checkout -b feature/new-agent-type

# Make small, focused commits
git commit -m "Add: New agent base class with enhanced capabilities"
git commit -m "Test: Unit tests for new agent functionality"
git commit -m "Docs: Update API documentation for new agent"

# Push and create PR
git push origin feature/new-agent-type
```

#### 2. **Commit Message Format**
```
Type: Brief description

Longer description if needed:
- What changed
- Why it changed
- Any breaking changes

Closes #123
```

**Types:**
- `Add:` New features
- `Fix:` Bug fixes
- `Update:` Modifications to existing features
- `Remove:` Deletions
- `Docs:` Documentation changes
- `Test:` Test additions/modifications
- `Refactor:` Code restructuring

#### 3. **Testing Requirements**
```bash
# Run all tests before committing
uv run pytest

# Specific test categories
uv run pytest test_cost_tracking.py
uv run pytest test_cost_optimization.py

# Coverage check
uv run pytest --cov=. --cov-report=html
```

### Adding New Features

#### 1. **Adding a New Agent**

```python
# 1. Define agent class in agents.py
class NewSpecializedAgent:
    def __init__(self, llm, logger=None):
        self.llm = llm
        self.logger = logger
        
        # Set LLM context for cost tracking
        if hasattr(llm, 'set_context'):
            llm.set_context("New Agent", "Specialized task description")
        
        self.agent = self._create_agent()
    
    def _create_agent(self):
        return Agent(
            role="Specialized Role",
            goal="Specific goal for this agent",
            backstory="Agent background and expertise",
            verbose=True,
            llm=self.llm
        )

# 2. Add to ResearchTeam class
class ResearchTeam:
    def __init__(self, llm, logger=None):
        # ... existing agents ...
        self.new_agent = NewSpecializedAgent(llm, logger)
    
    def execute_specialized_task(self, query):
        # Implement specialized workflow
        pass

# 3. Add tests
def test_new_agent_initialization():
    # Test agent creation and configuration
    pass

def test_new_agent_task_execution():
    # Test agent functionality
    pass
```

#### 2. **Adding Cost Optimization Features**

```python
# 1. Extend CostOptimizer class
class CostOptimizer:
    def new_optimization_strategy(self, prompt: str, context: Dict) -> str:
        """Implement new optimization approach"""
        # Optimization logic
        return optimized_prompt
    
    def analyze_optimization_effectiveness(self) -> Dict:
        """Analyze how well optimizations are working"""
        # Analysis logic
        return metrics

# 2. Integrate with TrackedLLM
class TrackedLLM:
    def call(self, prompt, **kwargs):
        # Apply new optimization
        optimized_prompt = self.cost_optimizer.new_optimization_strategy(
            prompt, self.get_context()
        )
        # ... rest of the method
```

#### 3. **Extending Web Interface**

```python
# 1. Add new FastAPI route
@app.get("/new-feature")
async def new_feature_endpoint():
    """New API endpoint"""
    return {"data": "new feature response"}

# 2. Add HTML template
<!-- templates/new_feature.html -->
{% extends "base.html" %}
{% block content %}
<div class="new-feature">
    <!-- New feature UI -->
</div>
{% endblock %}

# 3. Update navigation
<!-- Update base.html navigation -->
```

### Code Review Checklist

Before submitting a PR, ensure:

- [ ] **Code follows PEP 8** styling guidelines
- [ ] **All functions have docstrings** with clear descriptions
- [ ] **Type hints** are used for function parameters and returns
- [ ] **Tests are written** for new functionality
- [ ] **Error handling** is implemented appropriately
- [ ] **Cost tracking** is integrated for any LLM calls
- [ ] **Documentation** is updated for user-facing changes
- [ ] **COMMITS.md** is updated for significant features

## 🧪 Testing

### Test Structure

```
tests/
├── test_cost_tracking.py      # Cost tracking functionality
├── test_cost_optimization.py  # Optimization features
├── test_agents.py             # Agent functionality
├── test_config.py             # Configuration management
├── test_web_interface.py      # Web API testing
└── conftest.py                # Test configuration
```

### Writing Tests

#### 1. **Unit Tests Example**
```python
import pytest
from cost_tracker import CostTracker, CostEvent

def test_cost_calculation():
    """Test cost calculation accuracy"""
    tracker = CostTracker()
    cost = tracker.calculate_cost(
        "anthropic/claude-sonnet-4-20250514", 
        input_tokens=1000, 
        output_tokens=500
    )
    expected = (1000/1000 * 0.003) + (500/1000 * 0.015)
    assert abs(cost - expected) < 0.001

def test_budget_alerts():
    """Test budget alert functionality"""
    tracker = CostTracker()
    tracker.session_budget = 1.0  # Low budget for testing
    
    # Simulate expensive API call
    event = tracker.track_api_call(
        agent_name="Test Agent",
        model="anthropic/claude-sonnet-4-20250514",
        input_tokens=10000,
        output_tokens=5000
    )
    
    # Should trigger budget alert
    assert event.cost_usd > tracker.session_budget
```

#### 2. **Integration Tests Example**
```python
def test_complete_research_workflow():
    """Test end-to-end research workflow"""
    config = Config(enable_cost_tracking=True)
    team = ResearchTeam(config.get_llm(), config.logger)
    
    result = team.execute_complete_research("test query")
    
    assert result is not None
    assert len(result) > 100  # Substantial response
    assert config.get_cost_summary()['session_cost'] > 0
```

### Test Data Management

```python
# conftest.py
import pytest
import tempfile
import os

@pytest.fixture
def temp_db():
    """Provide temporary database for testing"""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    os.unlink(path)

@pytest.fixture
def mock_config():
    """Provide test configuration"""
    return Config(enable_cost_tracking=True)
```

### Running Tests

```bash
# All tests
uv run pytest

# Specific test file
uv run pytest tests/test_cost_tracking.py

# With coverage
uv run pytest --cov=. --cov-report=html

# Verbose output
uv run pytest -v

# Test specific function
uv run pytest tests/test_cost_tracking.py::test_cost_calculation
```

## 🚀 Deployment

### Local Development

```bash
# Terminal interface
uv run main.py

# Web interface
uv run frontend/web_app.py
# Access: http://localhost:8000
```

### Production Deployment

#### 1. **Docker Deployment**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

# Install UV and dependencies
RUN pip install uv
RUN uv install --frozen

# Set environment
ENV PYTHONPATH=/app

# Run application
CMD ["uv", "run", "frontend/web_app.py"]
```

```bash
# Build and run
docker build -t agentic-research .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your_key agentic-research
```

#### 2. **Environment Configuration**
```bash
# Production .env
ANTHROPIC_API_KEY=prod_key_here
DAILY_COST_BUDGET=100.0
SESSION_COST_BUDGET=20.0
LOG_LEVEL=WARNING
DEBUG_MODE=False
```

#### 3. **Database Management**
```bash
# Production database backup
cp cost_tracking.db cost_tracking_backup_$(date +%Y%m%d).db

# Database cleanup (removes old entries)
sqlite3 cost_tracking.db "DELETE FROM cost_events WHERE timestamp < datetime('now', '-30 days')"
```

## ⚡ Performance Optimization

### Database Optimization

```sql
-- Add indexes for common queries
CREATE INDEX IF NOT EXISTS idx_timestamp ON cost_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_session ON cost_events(session_id);
CREATE INDEX IF NOT EXISTS idx_agent ON cost_events(agent_name);

-- Optimize cache queries
CREATE INDEX IF NOT EXISTS idx_cache_hash ON cached_responses(prompt_hash);
CREATE INDEX IF NOT EXISTS idx_cache_expiry ON cached_responses(expires_at);
```

### Memory Management

```python
# Use generators for large datasets
def get_cost_events_generator(self, start_date: datetime):
    """Memory-efficient cost event iteration"""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cost_events WHERE timestamp >= ?", 
                   (start_date.isoformat(),))
    
    while True:
        rows = cursor.fetchmany(1000)
        if not rows:
            break
        for row in rows:
            yield CostEvent(*row)
    
    conn.close()
```

### Caching Strategies

```python
# Implement intelligent cache warming
class CostOptimizer:
    def warm_cache_for_common_queries(self):
        """Pre-cache responses for common research topics"""
        common_topics = [
            "machine learning applications",
            "climate change research",
            "artificial intelligence ethics"
        ]
        
        for topic in common_topics:
            if not self.get_cached_response(self._hash_prompt(topic)):
                # Generate and cache response
                pass
```

## 🔒 Security Considerations

### API Key Management

```python
# Never log API keys
def sanitize_for_logging(self, data: Dict) -> Dict:
    """Remove sensitive information from logs"""
    sanitized = data.copy()
    if 'api_key' in sanitized:
        sanitized['api_key'] = '***REDACTED***'
    return sanitized

# Validate API key format
def validate_api_key(self, api_key: str) -> bool:
    """Validate API key format without revealing key"""
    if not api_key or len(api_key) < 10:
        return False
    if not api_key.startswith('sk-ant-'):
        return False
    return True
```

### Database Security

```python
# Use parameterized queries
def get_cost_events(self, agent_name: str) -> List[CostEvent]:
    """Safe database query with parameterization"""
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    # Safe - parameterized query
    cursor.execute("SELECT * FROM cost_events WHERE agent_name = ?", 
                   (agent_name,))
    
    # Unsafe - string interpolation (DON'T DO THIS)
    # cursor.execute(f"SELECT * FROM cost_events WHERE agent_name = '{agent_name}'")
```

### Input Validation

```python
def validate_research_query(self, query: str) -> bool:
    """Validate user research query"""
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")
    
    if len(query) > 1000:
        raise ValueError("Query too long (max 1000 characters)")
    
    # Check for potential injection attempts
    suspicious_patterns = ['<script', 'javascript:', 'DROP TABLE']
    if any(pattern.lower() in query.lower() for pattern in suspicious_patterns):
        raise ValueError("Query contains suspicious content")
    
    return True
```

## 📊 Monitoring and Logging

### Logging Configuration

```python
# config.py
def setup_logging(level: str = "INFO"):
    """Configure comprehensive logging"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('agentic_research.log', mode='a')
        ]
    )
    
    # Separate logger for cost tracking
    cost_logger = logging.getLogger('cost_tracking')
    cost_handler = logging.FileHandler('cost_tracking.log', mode='a')
    cost_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    )
    cost_logger.addHandler(cost_handler)
    
    return logging.getLogger(__name__)
```

### Performance Monitoring

```python
import time
from functools import wraps

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = None
            success = False
            raise
        finally:
            duration = time.time() - start_time
            logger = logging.getLogger('performance')
            logger.info(f"{func.__name__}: {duration:.2f}s, Success: {success}")
        return result
    return wrapper

# Usage
@monitor_performance
def execute_complete_research(self, query: str) -> str:
    # Research implementation
    pass
```

---

## 🔄 Release Process

### Version Management

```bash
# Update version in pyproject.toml
[project]
name = "agentic-survey-research-team"
version = "0.2.0"  # Update version

# Tag release
git tag -a v0.2.0 -m "Release v0.2.0: Add WebSocket real-time dashboard"
git push origin v0.2.0
```

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] COMMITS.md updated with new release
- [ ] Version bumped in pyproject.toml
- [ ] Release notes prepared
- [ ] Security review completed
- [ ] Performance benchmarks verified

---

**Happy coding! 🚀**

For questions about development, please open an issue on GitHub or refer to the [API Documentation](API.md) for technical details.
