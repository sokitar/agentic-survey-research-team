# Repository Structure - Agentic Survey Research Team

## Main Project Files

```
├── .env                      # Environment variables (API keys, config)
├── .env.template             # Template for environment variables
├── .gitignore               # Git ignore patterns
├── .python-version          # Python version specification
├── COMMITS.md               # Development progress tracking and commit plan
├── REPO_STRUC.md           # This file - repository structure documentation
├── agents.py                # AI agents implementation (CrewAI-based)
├── chat.py                  # Terminal chat interface
├── config.py                # Configuration management with cost tracking
├── cost_tracker.py          # Cost tracking infrastructure
├── cost_tracking.db         # SQLite database for cost data
├── main.py                  # Main application entry point
├── pyproject.toml           # Project metadata and dependencies (UV format)
├── requirements.txt         # Python dependencies (legacy format)
├── test_cost_tracking.py    # Comprehensive cost tracking tests
├── tracked_llm.py           # LLM wrapper with automatic cost instrumentation
└── uv.lock                  # UV lock file for reproducible dependencies
```

## Key Components

### Core Application
- **main.py**: Entry point with cost tracking integration
- **config.py**: Enhanced configuration with cost-tracked LLM management
- **chat.py**: Terminal interface with cost commands and summaries

### AI Agents System
- **agents.py**: Complete 4-agent research workflow
  - ResearchCoordinator: Strategy and planning
  - LiteratureSearcher: Academic paper discovery
  - PaperAnalyzer: Research synthesis
  - ReportSynthesizer: Final report generation
  - ResearchTeam: Orchestrates complete workflow

### Cost Tracking Infrastructure (NEW in Commit 8)
- **cost_tracker.py**: Core cost monitoring system
  - Real-time API cost calculation
  - SQLite database storage
  - Budget alerts and warnings
  - Session and daily cost tracking
- **tracked_llm.py**: LLM wrapper for automatic cost tracking
  - Intercepts all API calls
  - Per-agent cost attribution
  - Token usage estimation and tracking
- **cost_tracking.db**: Persistent cost data storage

### Development & Testing
- **test_cost_tracking.py**: Comprehensive test suite for cost infrastructure
- **COMMITS.md**: Development roadmap and progress tracking
- **test.ipynb**: Jupyter notebook for experimentation

### Configuration
- **pyproject.toml**: UV-based project configuration
- **requirements.txt**: Python dependencies
- **.env**: API keys and environment configuration
- **.python-version**: Python 3.11+ requirement

## Architecture Overview

The application uses a multi-agent architecture powered by CrewAI, with comprehensive cost tracking:

1. **Research Workflow**: Coordinator → Literature Search → Analysis → Report Generation
2. **Cost Monitoring**: Every LLM call is tracked with token usage and cost calculation
3. **Budget Management**: Real-time alerts for session and daily budget limits
4. **Database Storage**: Historical cost data for analytics and optimization

## Current Status

✅ **Completed Features**:
- Complete 4-agent research workflow
- Claude Sonnet 4 integration
- Comprehensive cost tracking infrastructure
- Real-time budget monitoring
- SQLite-based cost data storage
- Terminal interface with cost commands

🚧 **Next Development Phase** (Commit 9):
- Cost optimization features
- Advanced prompt engineering
- Query caching for cost reduction
- Enhanced budget management

## Usage

Run with UV (recommended):
```bash
uv run python main.py
```

The application automatically enables cost tracking and displays:
- Real-time cost summaries
- Budget alerts
- Per-agent cost attribution
- Session and daily spending

## Cost Tracking Commands

In the chat interface:
- `cost` / `budget` - Show detailed cost summary
- Automatic cost updates after each research session
- Budget warnings when limits are exceeded
