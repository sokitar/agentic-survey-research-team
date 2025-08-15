# 👤 User Guide

## Welcome to Agentic Survey Research Team

This guide will walk you through everything you need to know to effectively use the Agentic Survey Research Team for your academic research needs.

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Advanced Features](#advanced-features)
4. [Cost Management](#cost-management)
5. [Web Interface](#web-interface)
6. [Real-time Web Dashboard](#real-time-web-dashboard)
7. [Research Strategies](#research-strategies)
7. [Troubleshooting](#troubleshooting)
8. [Tips & Best Practices](#tips--best-practices)

## 🚀 Getting Started

### First-Time Setup

1. **Install the application** following the README.md instructions
2. **Set up your API key** in the `.env` file
3. **Run your first research query** to test the system

```bash
# Quick start
uv run main.py
```

### Understanding the Interface

When you start the application, you'll see:

```
🔬 Agentic Survey Research Team
Welcome! I'll help you research any topic using AI agents.
💰 Cost tracking is enabled - monitoring API usage.
✅ Configuration loaded with cost tracking enabled

==================================================
💰 COST TRACKING SUMMARY
==================================================
📊 Current Session (session_1755191168):
   Cost: $0.0000
   Budget: $5.00
   Remaining: $5.0000

📅 Today:
   Cost: $0.0000
   Budget: $10.00
   Remaining: $10.0000
==================================================

👤 You: 
```

## 📖 Basic Usage

### Making Your First Research Query

Simply type your research question or topic:

```
👤 You: machine learning in healthcare
```

The system will activate all 4 agents:
1. **Research Coordinator** - Plans the research strategy
2. **Literature Searcher** - Finds relevant papers
3. **Research Analyst** - Analyzes the findings
4. **Report Writer** - Creates the final report

### Example Research Topics

#### Excellent Queries:
- `"climate change impacts on agriculture"`
- `"blockchain technology in supply chain management"`
- `"natural language processing for medical diagnosis"`
- `"renewable energy storage solutions"`
- `"artificial intelligence ethics frameworks"`

#### Avoid These:
- Too broad: `"technology"`
- Too narrow: `"Python list comprehensions"`
- Non-academic: `"best pizza recipes"`

### Understanding the Output

Your research will go through these stages:

1. **Strategy Development** (30-60 seconds)
   ```
   🤖 Research Coordinator: Developing research strategy...
   ```

2. **Literature Search** (60-90 seconds)
   ```
   📚 Literature Searcher: Preparing comprehensive search...
   ```

3. **Analysis** (90-120 seconds)
   ```
   🔬 Research Analyst: Ready for deep analysis...
   ```

4. **Report Generation** (60-90 seconds)
   ```
   📝 Report Writer: Standing by for final synthesis...
   ```

## 🎯 Advanced Features

### Available Commands

While in the chat interface, you can use these commands:

#### Basic Commands
- **`help`** - Show available commands
- **`quit`** or **`exit`** - Exit the application

#### Cost Management Commands
- **`cache`** - View cache statistics and hit rates
- **`optimize`** - View optimization metrics
- **`costs`** - Show detailed cost breakdown

Example:
```
👤 You: cache

📊 CACHE STATISTICS
==================================================
Cache Hit Rate: 45%
Total Cached Responses: 12
Cache Size: 2.3MB
Oldest Cache Entry: 2 hours ago
==================================================
```

### Research Query Strategies

#### 1. Specific Domain Research
```
👤 You: quantum computing applications in cryptography
```
**Result**: Focused analysis on specific intersection of fields

#### 2. Comparative Analysis
```
👤 You: compare supervised vs unsupervised machine learning approaches
```
**Result**: Detailed comparison with pros/cons analysis

#### 3. Trend Analysis
```
👤 You: recent developments in gene therapy 2020-2024
```
**Result**: Timeline-focused research with latest findings

#### 4. Methodological Research
```
👤 You: statistical methods for clinical trial analysis
```
**Result**: Method-focused research with practical applications

### Multi-Session Research

The system tracks your research history. You can:

1. **Build on previous research**:
   ```
   👤 You: extend the previous AI ethics research to include governance frameworks
   ```

2. **Reference earlier findings**:
   ```
   👤 You: how do the machine learning methods we discussed apply to financial markets?
   ```

## 💰 Cost Management

### Understanding Your Budget

The system has two budget levels:

- **Session Budget**: $5.00 (resets each time you start the app)
- **Daily Budget**: $10.00 (resets daily)

### Budget Alerts

You'll receive warnings at:
- **70% of budget**: Yellow warning
- **90% of budget**: Red warning
- **100% of budget**: Research blocked until next period

Example warning:
```
⚠️ WARNING: Approaching budget limit (90%)
Current session cost: $4.50 / $5.00
Consider optimizing queries or increasing budget.
```

### Cost Optimization Features

#### 1. Response Caching
- **Benefit**: 40-60% cost reduction for repeated queries
- **Duration**: 24 hours
- **How it works**: Identical queries return cached responses

#### 2. Prompt Optimization
- **Benefit**: 20-30% token reduction
- **How it works**: Removes redundancy and optimizes phrasing
- **Automatic**: Happens behind the scenes

#### 3. Query Cost Estimation
Before starting expensive research, check estimated costs:
```
👤 You: estimate cost for comprehensive climate change analysis
```

### Managing Costs Effectively

#### Low-Cost Strategies:
1. **Use specific queries** (avoid overly broad topics)
2. **Leverage caching** (repeat similar queries within 24 hours)
3. **Monitor session costs** regularly
4. **Use iterative refinement** (start broad, then narrow down)

#### Example Cost-Effective Workflow:
```
# Step 1: Broad overview (moderate cost)
👤 You: overview of renewable energy technologies

# Step 2: Cached follow-up (low cost)
👤 You: solar panel efficiency improvements mentioned in the previous research

# Step 3: Specific deep dive (moderate cost)
👤 You: perovskite solar cell commercialization challenges
```

## 🌐 Web Interface

### Starting the Web Interface

```bash
uv run frontend/web_app.py
```

Then open: http://localhost:8000

### Web Interface Features

#### 1. Dashboard
- Real-time cost tracking
- Agent status display
- Recent research history

#### 2. Research Form
- Text input for research queries
- Progress indicators during research
- Downloadable reports

#### 3. Cost Analytics
- Visual cost breakdowns
- Budget monitoring
- Cache hit rate charts

#### 4. Research History
- Browse previous research
- Search through reports
- Export functionality

### Web vs Terminal Interface

| Feature | Terminal | Web |
|---------|----------|-----|
| Real-time updates | ✅ | ✅ WebSocket |
| Cost tracking | ✅ | ✅ Visual charts |
| Research history | Limited | ✅ Full browser |
| Export options | Text copy | ✅ PDF/CSV/JSON |
| Multi-user support | ❌ | ✅ |
| Accessibility | Limited | ✅ Full responsive |
| Agent visualization | ❌ | ✅ D3.js graphs |
| PDF generation | ❌ | ✅ Professional reports |

## 🎛️ Real-time Web Dashboard

The enhanced web dashboard provides a modern, interactive interface with real-time updates powered by WebSocket technology.

### Key Features

#### 1. Real-time Agent Status Tracking
Watch your research progress live:
- **Agent Status Cards**: See each agent's current activity
- **Progress Bars**: Visual progress indicators (0-100%)
- **Status Badges**: Color-coded status (idle, active, completed, error)
- **Activity Descriptions**: Detailed current activities

Example status updates you'll see:
```
📊 Agent Update: coordinator - active (15%) - Developing comprehensive research strategy
📊 Agent Update: searcher - active (40%) - Analyzing paper abstracts and relevance  
📊 Agent Update: analyst - active (65%) - Identifying key themes across research papers
📊 Agent Update: writer - completed (100%) - Final research report generated successfully
```

#### 2. Interactive Agent Workflow Visualization
D3.js-powered workflow diagram:
- **Node Visualization**: Each agent represented as a colored node
- **Connection Lines**: Show workflow progression
- **Real-time Updates**: Nodes change color based on status
- **Pulse Animation**: Active agents pulse to show activity
- **Status Colors**:
  - 🔘 **Gray**: Idle
  - 🔵 **Blue**: Active (with pulse animation)
  - 🟢 **Green**: Completed
  - 🔴 **Red**: Error

#### 3. Live Cost Tracking Dashboard
Real-time cost monitoring with visual indicators:
- **Session Cost**: Current research session spending
- **Daily Cost**: Today's total spending
- **Budget Progress Bars**: Visual budget utilization
- **Color-coded Alerts**:
  - 🟢 Green: Under 70% budget
  - 🟡 Yellow: 70-90% budget
  - 🔴 Red: Over 90% budget
- **Agent Cost Breakdown**: Per-agent spending tracking

#### 4. Professional PDF Report Generation
One-click PDF export with professional formatting:
- **Markdown Processing**: Converts research markdown to formatted PDF
- **Custom Styling**: Professional document layout
- **Header Information**: Query, generation date, metadata
- **Structured Formatting**: Proper headings, bullet points, emphasis
- **Download Management**: Automatic file naming and download

Example PDF features:
```
✅ Research Report: [Your Query]
✅ Generated: 2024-08-15 19:45:30
✅ Professional formatting with ReportLab
✅ Markdown-to-PDF conversion
✅ Proper typography and spacing
```

#### 5. WebSocket Real-time Communication
Instant updates without page refresh:
- **Connection Status**: Shows WebSocket connection state
- **Live Updates**: Agent status changes in real-time
- **Cost Updates**: Immediate cost tracking updates
- **Error Handling**: Automatic reconnection on disconnect
- **Ping/Pong**: Connection health monitoring

### Using the Web Dashboard

#### Starting a Research Session
1. **Open Browser**: Navigate to http://localhost:8000
2. **Check Connection**: Look for "Connected" badge in Agent Status
3. **Enter Query**: Type research question in the text area
4. **Submit**: Click "Start Research" button
5. **Watch Progress**: Monitor real-time agent updates

#### Real-time Monitoring Experience
Once you submit a query:

1. **Immediate Feedback**:
   ```
   🔄 Research started with real-time updates
   📊 Agent Update: coordinator - active (5%) - Analyzing research query
   ```

2. **Progressive Updates**:
   ```
   📊 Agent Update: coordinator - active (25%) - Research strategy completed successfully
   📊 Agent Update: searcher - active (30%) - Searching academic databases
   📊 Agent Update: searcher - active (45%) - Found 12 relevant papers from Nature, Science, Cell
   ```

3. **Visual Changes**:
   - Agent status cards update colors
   - Progress bars fill up
   - Workflow diagram nodes change colors
   - Cost tracking updates in real-time

#### PDF Report Generation
After research completion:
1. **Download Button**: Appears next to results
2. **Click Download**: Generates PDF with professional formatting
3. **Automatic Download**: Browser downloads the formatted report
4. **File Naming**: Auto-generated filename based on query

### WebSocket Connection Management

The dashboard handles connection issues gracefully:
- **Auto-reconnect**: Attempts reconnection every 3 seconds
- **Status Indicators**: 
  - 🟢 Connected
  - 🔴 Disconnected 
  - 🟡 Error
- **Fallback Mode**: Falls back to polling if WebSocket fails

### Performance and Optimization

#### Browser Requirements
- **Modern Browser**: Chrome 80+, Firefox 75+, Safari 13+
- **JavaScript**: Must be enabled
- **WebSocket Support**: Required for real-time features

#### Network Considerations
- **Local Network**: Optimized for localhost development
- **Low Latency**: Real-time updates typically <100ms
- **Bandwidth**: Minimal - only status updates transmitted

### Troubleshooting Web Dashboard

#### Connection Issues
```
Problem: WebSocket shows "Disconnected"
Solution: 
1. Refresh the page
2. Check if web_app.py is running
3. Verify port 8000 is available
4. Check browser console for errors
```

#### PDF Generation Issues
```
Problem: PDF download fails
Solution:
1. Check browser allows downloads
2. Verify ReportLab is installed
3. Ensure sufficient disk space
4. Try shorter research content
```

#### Performance Issues
```
Problem: Slow real-time updates
Solution:
1. Close other browser tabs
2. Check system resources
3. Restart the web application
4. Use Chrome for best performance
```

## 🔬 Research Strategies

### 1. Systematic Literature Review

For comprehensive topic coverage:

```
# Step 1: Broad landscape
👤 You: artificial intelligence in medical diagnosis overview

# Step 2: Methodological focus
👤 You: deep learning architectures for medical image analysis

# Step 3: Application-specific
👤 You: AI diagnostic tools for radiology workflow integration

# Step 4: Critical analysis
👤 You: limitations and challenges of AI medical diagnosis systems
```

### 2. Comparative Research

For decision-making research:

```
# Compare approaches
👤 You: compare blockchain vs traditional databases for healthcare records

# Analyze trade-offs
👤 You: security vs performance trade-offs in the blockchain healthcare solutions above

# Implementation considerations
👤 You: practical implementation challenges for blockchain healthcare systems
```

### 3. Trend Analysis

For staying current:

```
# Recent developments
👤 You: latest developments in quantum computing 2023-2024

# Emerging applications
👤 You: emerging applications of quantum computing in the research above

# Future directions
👤 You: predicted future directions for quantum computing based on current trends
```

### 4. Gap Analysis

For research opportunities:

```
# Current state
👤 You: current state of natural language processing for legal documents

# Identify limitations
👤 You: main limitations and challenges in the legal NLP research above

# Research opportunities
👤 You: unexplored research opportunities in legal document processing
```

## 🔧 Troubleshooting

### Common Issues

#### 1. API Key Problems
**Error**: `❌ Error: Missing or invalid API key`

**Solutions**:
- Check `.env` file exists and has valid `ANTHROPIC_API_KEY`
- Ensure no extra spaces or quotes around the key
- Verify key is active in Anthropic Console

#### 2. Budget Exceeded
**Error**: `💰 Warning: Approaching budget limit (90%)`

**Solutions**:
- Wait for next budget period
- Clear cache to start fresh: `rm cost_optimization.db`
- Increase budget in environment variables
- Use more specific queries to reduce costs

#### 3. Research Quality Issues
**Problem**: Generic or shallow research results

**Solutions**:
- Use more specific research queries
- Provide context: "For a master's thesis on..."
- Include time constraints: "focusing on 2020-2024 research"
- Specify methodology: "systematic review of..."

#### 4. Slow Performance
**Problem**: Research takes too long

**Solutions**:
- Check internet connection
- Verify API key limits aren't exceeded
- Try simpler queries first
- Restart the application

#### 5. Cache Issues
**Problem**: Unexpected cache hits or misses

**Solutions**:
- Clear cache: `rm cost_optimization.db`
- Check cache statistics: type `cache` in chat
- Restart application for fresh session

### Error Codes Reference

| Error Code | Meaning | Solution |
|------------|---------|----------|
| `ValueError` | Configuration issue | Check `.env` file |
| `sqlite3.Error` | Database problem | Delete database files and restart |
| `ConnectionError` | API connectivity | Check internet and API status |
| `RateLimitError` | Too many requests | Wait and retry, or increase limits |

## 💡 Tips & Best Practices

### Crafting Effective Research Queries

#### ✅ Good Practices:
1. **Be specific**: "machine learning for fraud detection" vs "AI"
2. **Include context**: "for financial services industry"
3. **Specify timeframe**: "recent developments 2022-2024"
4. **Mention methodology**: "systematic review of" or "meta-analysis of"

#### ❌ Avoid:
1. **Too broad**: "technology trends"
2. **Too narrow**: "specific algorithm parameters"
3. **Non-academic**: "business advice" or "personal opinions"
4. **Multiple unrelated topics**: "AI and cooking and sports"

### Maximizing Research Quality

#### 1. Progressive Refinement
Start broad, then narrow down:
```
Query 1: "renewable energy storage"
Query 2: "battery technologies for grid-scale renewable energy storage"
Query 3: "lithium-ion vs flow battery performance for utility-scale applications"
```

#### 2. Multi-Angle Analysis
Approach topics from different perspectives:
```
Technical: "blockchain consensus mechanisms for supply chain"
Economic: "cost-benefit analysis of blockchain supply chain solutions"
Social: "adoption barriers for blockchain in supply chain management"
```

#### 3. Literature Gap Identification
```
Current: "existing research on AI bias detection"
Gaps: "underexplored areas in AI bias detection research"
Future: "emerging approaches to AI bias mitigation"
```

### Cost Optimization Strategies

#### 1. Smart Query Sequencing
```
# High-impact order
1. Broad overview (comprehensive base)
2. Specific deep-dives (focused analysis)
3. Comparative studies (using previous context)
4. Gap analysis (leveraging all previous research)
```

#### 2. Cache Leveraging
```
# First query
👤 You: machine learning applications in healthcare

# Follow-up (likely cached elements)
👤 You: deep learning approaches mentioned in the healthcare ML research above

# Related query (some cache benefits)
👤 You: regulatory challenges for the ML healthcare applications discussed
```

#### 3. Session Planning
- Plan your research session with 3-5 related queries
- Use your $5 session budget strategically
- Save broader topics for fresh sessions

### Research Report Utilization

#### 1. Academic Writing Support
- Use reports as literature review foundations
- Extract key citations and methodologies
- Identify research gaps for your own work

#### 2. Grant Proposal Development
- Current state of research
- Identified gaps and opportunities
- Methodology benchmarks

#### 3. Industry Analysis
- Technology trends and adoption
- Competitive landscape analysis
- Implementation case studies

### Quality Indicators

Look for these signs of high-quality research:

#### ✅ Good Research Output:
- Multiple recent citations (2020-2024)
- Balanced perspective with limitations
- Clear methodology descriptions
- Identified research gaps
- Practical implications discussed

#### ⚠️ May Need Refinement:
- Only older citations (pre-2020)
- Single perspective or biased view
- Vague or generic findings
- No clear limitations discussed
- Missing practical applications

---

## 🎓 Getting the Most Value

### For Students
- Use for literature review foundations
- Identify research gaps for thesis topics
- Understand methodological approaches
- Build comprehensive bibliographies

### For Researchers
- Stay current with field developments
- Identify collaboration opportunities
- Benchmark methodologies
- Explore interdisciplinary connections

### For Professionals
- Industry trend analysis
- Technology assessment
- Competitive intelligence
- Solution evaluation

---

**Remember**: The Agentic Survey Research Team is a research assistant, not a replacement for critical thinking. Always verify important findings and use the research as a starting point for deeper investigation.

For technical issues, see the [API Documentation](API.md) or [Developer Guide](DEVELOPER.md).
