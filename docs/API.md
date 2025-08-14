# 📚 API Documentation

## Overview

This document provides comprehensive documentation for the Agentic Survey Research Team API, including all modules, classes, and functions with usage examples.

## Core Modules

### 🔧 Config Module (`config.py`)

The configuration module handles application settings, environment variables, and LLM initialization.

#### Classes

##### `Config`

Main configuration class for the application.

**Constructor:**
```python
Config(enable_cost_tracking=True)
```

**Parameters:**
- `enable_cost_tracking` (bool): Enable/disable cost tracking functionality

**Methods:**

##### `get_llm(agent_name="Unknown")`
Returns a configured LLM instance for CrewAI agents.

```python
# Basic usage
config = Config()
llm = config.get_llm("Research Coordinator")

# Without cost tracking
config = Config(enable_cost_tracking=False)
llm = config.get_llm()
```

**Parameters:**
- `agent_name` (str): Name of the agent using the LLM (for cost tracking)

**Returns:** `LLM` or `TrackedLLM` instance

##### `get_cost_summary()`
Returns current cost summary if tracking is enabled.

```python
config = Config()
summary = config.get_cost_summary()
if summary:
    print(f"Session cost: ${summary['session_cost']:.4f}")
```

**Returns:** `Dict` with cost information or `None`

##### `print_cost_summary()`
Prints formatted cost summary to console.

```python
config = Config()
config.print_cost_summary()
```

#### Functions

##### `setup_logging()`
Configures basic logging for the application.

```python
logger = setup_logging()
logger.info("Application started")
```

**Returns:** `logging.Logger` instance

---

### 🤖 Agents Module (`agents.py`)

Contains all AI agent definitions and research workflow orchestration.

#### Classes

##### `ResearchCoordinator`

Coordinates the entire research process and manages background actions.

**Constructor:**
```python
ResearchCoordinator(llm, logger=None)
```

**Parameters:**
- `llm`: LLM instance for the agent
- `logger` (optional): Logger instance

**Methods:**

##### `create_research_task(research_query)`
Creates a research coordination task.

```python
coordinator = ResearchCoordinator(llm, logger)
task = coordinator.create_research_task("climate change impacts")
```

##### `execute_research(research_query)`
Executes the complete research coordination process.

```python
result = coordinator.execute_research("macroeconomic models")
print(result)
```

##### `LiteratureSearcher`

Agent specialized in finding and searching academic literature.

**Constructor:**
```python
LiteratureSearcher(llm, logger=None)
```

**Methods:**

##### `create_search_task(research_query)`
Creates a literature search task.

```python
searcher = LiteratureSearcher(llm, logger)
task = searcher.create_search_task("machine learning applications")
```

##### `PaperAnalyzer`

Agent for analyzing and synthesizing research findings.

**Constructor:**
```python
PaperAnalyzer(llm, logger=None)
```

##### `ReportSynthesizer`

Agent for synthesizing final comprehensive research reports.

**Constructor:**
```python
ReportSynthesizer(llm, logger=None)
```

##### `ResearchTeam`

Coordinates multiple agents working together in a research workflow.

**Constructor:**
```python
ResearchTeam(llm, logger=None)
```

**Methods:**

##### `execute_complete_research(query)`
Executes the complete 4-agent research workflow.

```python
team = ResearchTeam(llm, logger)
report = team.execute_complete_research("artificial intelligence ethics")
```

---

### 💰 Cost Tracking Module (`cost_tracker.py`)

Comprehensive API cost tracking and monitoring system.

#### Classes

##### `CostEvent`

Dataclass representing a single API cost event.

**Attributes:**
- `timestamp` (datetime): When the event occurred
- `agent_name` (str): Name of the agent making the call
- `session_id` (str): Unique session identifier
- `model` (str): LLM model used
- `input_tokens` (int): Number of input tokens
- `output_tokens` (int): Number of output tokens
- `cost_usd` (float): Cost in USD
- `task_description` (str): Description of the task

**Methods:**

##### `to_dict()`
Converts the event to a dictionary for JSON serialization.

```python
event = CostEvent(...)
event_dict = event.to_dict()
```

##### `CostTracker`

Main cost tracking and monitoring system.

**Constructor:**
```python
CostTracker(db_path="cost_tracking.db", logger=None)
```

**Parameters:**
- `db_path` (str): Path to SQLite database file
- `logger` (optional): Logger instance

**Methods:**

##### `calculate_cost(model, input_tokens, output_tokens)`
Calculates cost for given token usage.

```python
tracker = CostTracker()
cost = tracker.calculate_cost(
    "anthropic/claude-sonnet-4-20250514", 
    1000, 
    500
)
print(f"Cost: ${cost:.4f}")
```

##### `track_api_call(agent_name, model, input_tokens, output_tokens, task_description="")`
Tracks a single API call and returns cost event.

```python
event = tracker.track_api_call(
    agent_name="Research Coordinator",
    model="anthropic/claude-sonnet-4-20250514",
    input_tokens=1500,
    output_tokens=800,
    task_description="Literature search coordination"
)
```

##### `get_session_cost(session_id=None)`
Gets total cost for a session.

```python
session_cost = tracker.get_session_cost()
print(f"Current session cost: ${session_cost:.4f}")
```

##### `get_daily_cost(date=None)`
Gets total cost for a specific date.

```python
daily_cost = tracker.get_daily_cost()
print(f"Today's cost: ${daily_cost:.4f}")
```

##### `get_cost_summary()`
Gets comprehensive cost summary.

```python
summary = tracker.get_cost_summary()
print(f"Session cost: ${summary['session_cost']:.4f}")
print(f"Daily cost: ${summary['daily_cost']:.4f}")
```

##### `print_cost_summary()`
Prints formatted cost summary to console.

```python
tracker.print_cost_summary()
```

---

### 🎯 Cost Optimizer Module (`cost_optimizer.py`)

Implements caching and optimization strategies to reduce API costs.

#### Classes

##### `CostOptimizer`

Manages response caching and prompt optimization.

**Constructor:**
```python
CostOptimizer(db_path="cost_optimization.db", cache_duration_hours=24, logger=None)
```

**Methods:**

##### `get_cached_response(prompt_hash)`
Retrieves cached response if available and not expired.

```python
optimizer = CostOptimizer()
cached = optimizer.get_cached_response("prompt_hash_123")
if cached:
    print("Using cached response")
```

##### `cache_response(prompt_hash, response, metadata=None)`
Caches a response for future use.

```python
optimizer.cache_response(
    prompt_hash="hash_123",
    response="AI response content",
    metadata={"tokens": 1000, "cost": 0.015}
)
```

##### `optimize_prompt(prompt, agent_name="Unknown")`
Optimizes prompt to reduce token usage.

```python
optimized = optimizer.optimize_prompt(
    "Write a comprehensive analysis of climate change...",
    agent_name="Research Analyst"
)
```

---

### 🔌 Tracked LLM Module (`tracked_llm.py`)

Wrapper for LLM instances that adds cost tracking capabilities.

#### Classes

##### `TrackedLLM`

LLM wrapper that tracks costs and applies optimizations.

**Constructor:**
```python
TrackedLLM(base_llm, cost_tracker, cost_optimizer, agent_name="Unknown", task_context="")
```

**Methods:**

##### `call(prompt, **kwargs)`
Makes an LLM call with cost tracking and optimization.

```python
tracked_llm = TrackedLLM(base_llm, tracker, optimizer, "Research Agent")
response = tracked_llm.call("Analyze the following research paper...")
```

##### `set_context(agent_name, task_context)`
Updates the agent name and task context.

```python
tracked_llm.set_context("Literature Searcher", "Academic paper search")
```

#### Functions

##### `create_tracked_llm(model, api_key, agent_name="Unknown", task_context="")`
Factory function to create a TrackedLLM instance.

```python
tracked_llm = create_tracked_llm(
    model="anthropic/claude-sonnet-4-20250514",
    api_key="your_api_key",
    agent_name="Research Coordinator",
    task_context="Research planning"
)
```

---

### 💬 Chat Interface Module (`chat.py`)

Provides terminal-based chat interface for user interaction.

#### Classes

##### `ChatInterface`

Manages the terminal chat interface and user interactions.

**Constructor:**
```python
ChatInterface(logger, config)
```

**Methods:**

##### `run_chat_loop(research_team)`
Runs the main chat interaction loop.

```python
chat = ChatInterface(logger, config)
chat.run_chat_loop(research_team)
```

##### `handle_command(command, config)`
Processes special commands like 'help', 'cache', 'optimize'.

```python
result = chat.handle_command("cache", config)
```

---

### 🌐 Web Application Module (`frontend/web_app.py`)

FastAPI-based web interface for the research system.

#### FastAPI Routes

##### `GET /`
Main dashboard page.

##### `POST /research`
Submits research query and returns results.

##### `GET /costs`
Returns current cost information.

##### `GET /health`
Health check endpoint.

---

## Usage Examples

### Basic Research Query

```python
from config import Config
from agents import ResearchTeam

# Initialize configuration
config = Config(enable_cost_tracking=True)

# Create research team
team = ResearchTeam(config.get_llm(), config.logger)

# Execute research
result = team.execute_complete_research("artificial intelligence in healthcare")
print(result)

# Check costs
config.print_cost_summary()
```

### Cost Tracking Example

```python
from cost_tracker import CostTracker

# Initialize cost tracker
tracker = CostTracker()

# Track an API call
event = tracker.track_api_call(
    agent_name="Research Coordinator",
    model="anthropic/claude-sonnet-4-20250514",
    input_tokens=1000,
    output_tokens=500,
    task_description="Initial research planning"
)

# Get cost summary
summary = tracker.get_cost_summary()
print(f"Session cost: ${summary['session_cost']:.4f}")
```

### Optimization Example

```python
from cost_optimizer import CostOptimizer

# Initialize optimizer
optimizer = CostOptimizer()

# Optimize a prompt
original_prompt = "Please provide a very detailed and comprehensive analysis..."
optimized_prompt = optimizer.optimize_prompt(original_prompt, "Research Analyst")

# Check cache
cached_response = optimizer.get_cached_response("prompt_hash_123")
if cached_response:
    print("Using cached response, saving API costs!")
```

### Web Interface Example

```python
from frontend.web_app import app
import uvicorn

# Run web server
uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Error Handling

### Common Exceptions

- `ValueError`: Invalid configuration or missing environment variables
- `sqlite3.Error`: Database connection or query errors
- `Exception`: General API or processing errors

### Error Handling Pattern

```python
try:
    config = Config()
    result = research_team.execute_research(query)
except ValueError as e:
    logger.error(f"Configuration error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    # Handle gracefully
```

## Performance Considerations

- **Caching**: 24-hour response cache reduces API calls by 40-60%
- **Prompt Optimization**: Reduces token usage by 20-30%
- **Batch Processing**: Group related queries when possible
- **Budget Monitoring**: Set appropriate daily and session budgets

## Best Practices

1. **Always enable cost tracking** in production
2. **Set reasonable budgets** to prevent cost overruns
3. **Monitor cache hit rates** for optimization effectiveness
4. **Use specific agent names** for better cost attribution
5. **Implement proper error handling** for API failures
6. **Regular database maintenance** for optimal performance

---

For more detailed examples and advanced usage patterns, see the user guide and developer documentation.
