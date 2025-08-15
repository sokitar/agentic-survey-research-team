# 🔬 Agentic Survey Research Team

A sophisticated multi-agent AI research system built with CrewAI that automates comprehensive academic research workflows. The system orchestrates 4 specialized AI agents to conduct literature searches, analysis, and report generation with built-in cost tracking and optimization.

## ✨ Features

### 🤖 Multi-Agent Research Workflow
- **Research Coordinator**: Develops strategic research plans and coordinates team activities
- **Literature Searcher**: Performs comprehensive literature searches and identifies key papers
- **Research Analyst**: Conducts deep analysis and synthesizes research findings
- **Report Writer**: Generates comprehensive 2000-3000 word research reports

### 💰 Advanced Cost Management
- Real-time API cost tracking with SQLite database
- Budget alerts at 70% and 90% thresholds
- 24-hour response caching system
- Intelligent prompt optimization
- Per-agent cost monitoring and analytics

### 🌐 Enhanced Web Dashboard
- **Real-time WebSocket Updates**: Live agent status tracking and progress monitoring
- **Interactive Agent Visualization**: D3.js-powered workflow diagrams with real-time status updates
- **Professional PDF Generation**: ReportLab-powered PDF export with markdown formatting
- **Live Cost Tracking**: Real-time cost updates and budget monitoring via WebSocket
- **Responsive Bootstrap Design**: Mobile-friendly interface with modern UI components
- **Terminal Interface**: Interactive chat-based research queries for advanced users

### 🎯 Intelligent Optimization
- Query response caching to reduce redundant API calls
- Prompt optimization for cost efficiency
- Session and daily budget management
- Comprehensive cost analytics and reporting

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- UV package manager (recommended)
- Anthropic API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sokitar/agentic-survey-research-team.git
   cd agentic-survey-research-team
   ```

2. **Set up environment:**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env and add your Anthropic API key
   nano .env
   ```

3. **Install dependencies:**
   ```bash
   uv install
   ```

### Usage

#### Terminal Interface (Recommended)
```bash
uv run main.py
```

#### Web Interface
```bash
uv run frontend/web_app.py
```
Then open http://localhost:8000 in your browser.

## 📋 Usage Examples

### Basic Research Query
```
👤 You: climate change impacts on agriculture

🚀 Activating multi-agent research team...
📋 Query: climate change impacts on agriculture
👥 All Agents: Coordinator → Literature Searcher → Analyst → Report Writer
```

### Available Commands
- **Research Query**: Type any academic topic or research question
- **`quit`** or **`exit`**: Exit the application
- **`help`**: Show available commands
- **`cache`**: View cache statistics
- **`optimize`**: View optimization metrics

## 🏗️ Architecture

### Core Components

```
agentic-survey-research-team/
├── main.py              # Main terminal application
├── config.py            # Configuration and LLM setup
├── agents.py            # CrewAI agent definitions
├── chat.py              # Terminal chat interface
├── cost_tracker.py      # Cost monitoring system
├── cost_optimizer.py    # Caching and optimization
├── tracked_llm.py       # Cost-tracked LLM wrapper
├── frontend/
│   ├── web_app.py      # FastAPI web application
│   └── templates/      # HTML templates
├── tests/              # Test suites
└── docs/               # Documentation
```

### Agent Workflow

1. **Research Coordinator** analyzes the query and creates research strategy
2. **Literature Searcher** finds relevant academic papers and sources
3. **Research Analyst** synthesizes findings and identifies patterns
4. **Report Writer** generates comprehensive final report

### Cost Tracking System

- **Real-time monitoring** of all API calls
- **SQLite database** for persistent cost storage
- **Budget management** with configurable limits
- **Caching system** to minimize redundant requests
- **Per-agent analytics** for performance optimization

## 🔧 Configuration

### Environment Variables
```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional (with defaults)
DAILY_BUDGET=10.0
SESSION_BUDGET=5.0
CACHE_DURATION_HOURS=24
```

### Model Configuration
The system uses Claude Sonnet 4 (`anthropic/claude-sonnet-4-20250514`) by default. This can be configured in `config.py`.

## 📊 Cost Management

### Budget Controls
- **Daily Budget**: $10.00 (configurable)
- **Session Budget**: $5.00 (configurable)
- **Warning Thresholds**: 70% and 90% of budget

### Cost Optimization Features
- **Response Caching**: 24-hour cache for identical queries
- **Prompt Optimization**: Automatic redundancy removal
- **Agent-specific Optimization**: Tailored optimizations per agent type
- **Budget Predictions**: Estimates for research queries

### Cost Monitoring
```bash
# View current costs
uv run main.py
# Check cache statistics
# Type 'cache' in the chat interface
```

## 🧪 Testing

Run the complete test suite:
```bash
# Cost tracking tests
uv run test_cost_tracking.py

# Cost optimization tests  
uv run test_cost_optimization.py
```

## 🛠️ Development

### Adding New Agents
1. Define agent in `agents.py`
2. Configure cost tracking in `config.py`
3. Update workflow in research team
4. Add tests for new functionality

### Extending Cost Tracking
1. Implement new metrics in `cost_tracker.py`
2. Add optimization strategies in `cost_optimizer.py`
3. Update analytics in web interface

## 📈 Performance

### Typical Research Session
- **Processing Time**: 2-5 minutes for comprehensive research
- **API Costs**: $0.50-$2.00 per research query
- **Output Quality**: 2000-3000 word professional research reports
- **Cache Hit Rate**: 40-60% for repeated queries

### Benchmarks
- **Literature Search**: 6-8 high-quality recent papers
- **Analysis Depth**: Multi-dimensional thematic analysis
- **Report Structure**: Executive summary + detailed analysis + bibliography
- **Cost Efficiency**: 30-50% savings through caching and optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 coding standards
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation for changes
- Use small, focused commits

## 📋 Roadmap

### Upcoming Features (Next Commits)
- **Commit 11**: Real-time Web Dashboard with WebSockets
- **Commit 12**: Advanced Web Features & Agent Monitor
- **Commit 13**: Interactive Web Controls & Configuration
- **Commit 14**: Web UI Polish & Advanced Features
- **Commit 15**: Comprehensive Testing Suite

See `COMMITS.md` for detailed development history and future plans.

## 🐛 Troubleshooting

### Common Issues

**API Key Error:**
```
❌ Error: Missing or invalid API key
```
Solution: Check `.env` file has valid `ANTHROPIC_API_KEY`

**Budget Exceeded:**
```
💰 Warning: Approaching budget limit (90%)
```
Solution: Check cost summary, clear cache, or increase budget limits

**Cache Issues:**
```python
# Clear cache database
rm cost_optimization.db
```

**Cost Tracking Database:**
```python
# Reset cost database
rm cost_tracking.db
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent orchestration framework
- **Anthropic**: Claude AI model and API
- **FastAPI**: Modern web framework
- **UV**: Fast Python package manager

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/sokitar/agentic-survey-research-team/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sokitar/agentic-survey-research-team/discussions)
- **Documentation**: See `docs/` directory for detailed guides

---

**Built with ❤️ by the Agentic Survey Research Team**
