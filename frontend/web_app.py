#!/usr/bin/env python3
"""
Web UI for Agentic Survey Research Team
FastAPI-based web interface with real-time research capabilities
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import asyncio
import logging
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from config import Config, setup_logging
from agents import ResearchTeam

# Initialize FastAPI app
app = FastAPI(
    title="Agentic Survey Research Team",
    description="AI-powered research team with multi-agent coordination",
    version="1.0.0"
)

# Setup templates
templates = Jinja2Templates(directory=current_dir / "templates")

# Global variables for application state
config = None
research_team = None
logger = None

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    global config, research_team, logger
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting Agentic Survey Research Team Web Interface")
    
    try:
        # Initialize configuration with cost tracking enabled
        config = Config(enable_cost_tracking=True)
        logger.info("Configuration loaded successfully with cost tracking")
        
        # Initialize AI research team with cost-tracked LLM
        research_team = ResearchTeam(config.get_llm(), logger)
        logger.info("Research team initialized successfully")
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main research interface page"""
    cost_summary = None
    if config and config.enable_cost_tracking:
        raw_summary = config.get_cost_summary()
        if raw_summary:
            # Flatten the cost summary for template use
            cost_summary = {
                "session_cost": raw_summary["current_session"]["cost"],
                "daily_cost": raw_summary["today"]["cost"],
                "session_budget": raw_summary["current_session"]["budget"],
                "daily_budget": raw_summary["today"]["budget"],
                "total_tokens": sum(raw_summary.get("agent_breakdown", {}).values()) * 1000,  # Rough estimate
                "agent_breakdown": raw_summary.get("agent_breakdown", {})
            }
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Agentic Survey Research Team",
        "cost_summary": cost_summary
    })

@app.post("/research", response_class=JSONResponse)
async def conduct_research(query: str = Form(...)):
    """Conduct research using the agent team"""
    if not research_team:
        raise HTTPException(status_code=500, detail="Research team not initialized")
    
    if not query or len(query.strip()) < 3:
        raise HTTPException(status_code=400, detail="Please provide a valid research query (minimum 3 characters)")
    
    logger.info(f"Web request: Research query received: {query}")
    
    try:
        # Execute research using the research team
        result = await asyncio.get_event_loop().run_in_executor(
            None, research_team.conduct_research, query.strip()
        )
        
        # Get updated cost summary
        cost_summary = None
        if config and config.enable_cost_tracking:
            cost_summary = config.get_cost_summary()
        
        return {
            "success": True,
            "query": query.strip(),
            "result": result,
            "cost_summary": cost_summary
        }
        
    except Exception as e:
        logger.error(f"Research error: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": query.strip()
        }

@app.get("/cost-summary", response_class=JSONResponse)
async def get_cost_summary():
    """Get current cost tracking summary"""
    if not config or not config.enable_cost_tracking:
        return {"cost_tracking_enabled": False}
    
    try:
        cost_summary = config.get_cost_summary()
        return {
            "cost_tracking_enabled": True,
            "cost_summary": cost_summary
        }
    except Exception as e:
        logger.error(f"Cost summary error: {e}")
        return {"error": str(e)}

@app.get("/health", response_class=JSONResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "research_team_ready": research_team is not None,
        "cost_tracking_enabled": config.enable_cost_tracking if config else False
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "web_app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
