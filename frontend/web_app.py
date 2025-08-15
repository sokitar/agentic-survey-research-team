#!/usr/bin/env python3
"""
Web UI for Agentic Survey Research Team
FastAPI-based web interface with real-time research capabilities
"""

from fastapi import FastAPI, Request, Form, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import asyncio
import logging
from pathlib import Path
import sys
import os
import json
import time
from typing import List, Dict, Any
from datetime import datetime
import threading

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

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.current_research: Dict[str, Any] = {
            "status": "idle",
            "query": "",
            "progress": 0,
            "current_agent": "",
            "start_time": None,
            "estimated_duration": None,
            "agent_status": {
                "coordinator": {"status": "idle", "progress": 0, "activity": "Planning & coordination", "tokens_used": 0, "estimated_time": 0},
                "searcher": {"status": "idle", "progress": 0, "activity": "Finding relevant papers", "tokens_used": 0, "estimated_time": 0},
                "analyst": {"status": "idle", "progress": 0, "activity": "Analyzing findings", "tokens_used": 0, "estimated_time": 0},
                "writer": {"status": "idle", "progress": 0, "activity": "Creating final report", "tokens_used": 0, "estimated_time": 0}
            }
        }
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, data: dict):
        for connection in self.active_connections.copy():
            try:
                await connection.send_json(data)
            except WebSocketDisconnect:
                self.active_connections.remove(connection)
            except Exception as e:
                logger.error(f"WebSocket broadcast error: {e}")
                if connection in self.active_connections:
                    self.active_connections.remove(connection)
    
    async def update_agent_status(self, agent_name: str, status: str, progress: int, activity: str = None):
        """Update specific agent status and broadcast to all clients"""
        if agent_name in self.current_research["agent_status"]:
            self.current_research["agent_status"][agent_name]["status"] = status
            self.current_research["agent_status"][agent_name]["progress"] = progress
            if activity:
                self.current_research["agent_status"][agent_name]["activity"] = activity
            
            await self.broadcast({
                "type": "agent_update",
                "agent": agent_name,
                "data": self.current_research["agent_status"][agent_name]
            })
    
    async def update_cost_tracking(self):
        """Update cost tracking information"""
        if config and config.enable_cost_tracking:
            try:
                cost_summary = config.get_cost_summary()
                if cost_summary:
                    await self.broadcast({
                        "type": "cost_update",
                        "data": {
                            "session_cost": cost_summary["current_session"]["cost"],
                            "daily_cost": cost_summary["today"]["cost"],
                            "session_budget": cost_summary["current_session"]["budget"],
                            "daily_budget": cost_summary["today"]["budget"],
                            "agent_breakdown": cost_summary.get("agent_breakdown", {})
                        }
                    })
            except Exception as e:
                logger.error(f"Cost tracking update error: {e}")

connection_manager = ConnectionManager()

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
        
        # Define WebSocket status callback
        async def status_callback(agent_name, status, progress, activity):
            await connection_manager.update_agent_status(agent_name, status, progress, activity)
            # Also update cost tracking after each agent update
            await connection_manager.update_cost_tracking()
        
        # Initialize AI research team with cost-tracked LLM and WebSocket callback
        research_team = ResearchTeam(config.get_llm(), logger, status_callback=status_callback)
        logger.info("Research team initialized successfully with WebSocket integration")
        
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await connection_manager.connect(websocket)
    
    # Send initial status
    await websocket.send_json({
        "type": "connection",
        "status": "connected",
        "agent_status": connection_manager.current_research["agent_status"]
    })
    
    # Send initial cost summary
    await connection_manager.update_cost_tracking()
    
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_json()
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)

async def simulate_research_progress(query: str):
    """Simulate research progress with realistic updates"""
    connection_manager.current_research["query"] = query
    connection_manager.current_research["status"] = "running"
    
    # Stage 1: Research Coordinator (0-25%)
    await connection_manager.update_agent_status(
        "coordinator", "active", 10, "Analyzing research query: '{}'".format(query[:50] + "..." if len(query) > 50 else query)
    )
    await asyncio.sleep(2)
    
    await connection_manager.update_agent_status(
        "coordinator", "active", 25, "Developing comprehensive research strategy"
    )
    await asyncio.sleep(2)
    
    # Stage 2: Literature Searcher (25-50%)
    await connection_manager.update_agent_status(
        "coordinator", "completed", 25, "Research strategy completed"
    )
    await connection_manager.update_agent_status(
        "searcher", "active", 30, "Searching academic databases (PubMed, JSTOR, IEEE)"
    )
    await asyncio.sleep(3)
    
    await connection_manager.update_agent_status(
        "searcher", "active", 45, "Found 12 relevant papers from Nature, Science, Cell"
    )
    await asyncio.sleep(2)
    
    await connection_manager.update_agent_status(
        "searcher", "completed", 50, "Literature search completed: 15 high-impact papers"
    )
    
    # Stage 3: Research Analyst (50-75%)
    await connection_manager.update_agent_status(
        "analyst", "active", 55, "Analyzing research methodologies and findings"
    )
    await asyncio.sleep(3)
    
    await connection_manager.update_agent_status(
        "analyst", "active", 65, "Identifying key themes across 15 research papers"
    )
    await asyncio.sleep(2)
    
    await connection_manager.update_agent_status(
        "analyst", "active", 70, "Synthesizing findings and identifying research gaps"
    )
    await asyncio.sleep(2)
    
    await connection_manager.update_agent_status(
        "analyst", "completed", 75, "Analysis complete: 5 major themes identified"
    )
    
    # Stage 4: Report Writer (75-100%)
    await connection_manager.update_agent_status(
        "writer", "active", 80, "Drafting executive summary and introduction"
    )
    await asyncio.sleep(3)
    
    await connection_manager.update_agent_status(
        "writer", "active", 90, "Compiling comprehensive 2,500-word research report"
    )
    await asyncio.sleep(2)
    
    await connection_manager.update_agent_status(
        "writer", "completed", 100, "Final research report generated successfully"
    )
    
    connection_manager.current_research["status"] = "completed"
    
    # Update cost tracking at the end
    await connection_manager.update_cost_tracking()

@app.post("/research-realtime", response_class=JSONResponse)
async def conduct_research_realtime(query: str = Form(...)):
    """Conduct research with real-time updates"""
    if not research_team:
        raise HTTPException(status_code=500, detail="Research team not initialized")
    
    if not query or len(query.strip()) < 3:
        raise HTTPException(status_code=400, detail="Please provide a valid research query (minimum 3 characters)")
    
    logger.info(f"Real-time research request: {query}")
    
    # Set research status
    connection_manager.current_research["query"] = query.strip()
    connection_manager.current_research["status"] = "running"
    
    # Run actual research with real-time updates in background
    async def run_research():
        try:
            # Use the async research method that provides real WebSocket updates
            result = await research_team.execute_coordinated_research_with_updates(query.strip())
            
            # Broadcast completion with result
            await connection_manager.broadcast({
                "type": "research_complete",
                "query": query.strip(),
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
            
            connection_manager.current_research["status"] = "completed"
            
        except Exception as e:
            logger.error(f"Research error: {e}")
            await connection_manager.broadcast({
                "type": "research_error",
                "error": str(e),
                "query": query.strip()
            })
            
            connection_manager.current_research["status"] = "error"
    
    asyncio.create_task(run_research())
    
    return {
        "success": True,
        "message": "Research started with real-time updates",
        "query": query.strip()
    }

@app.post("/generate-pdf")
async def generate_pdf(query: str = Form(...), content: str = Form(...)):
    """Generate PDF report from research content with markdown support"""
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    import tempfile
    import re
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_filename = tmp_file.name
        
        # Create PDF document
        doc = SimpleDocTemplate(tmp_filename, pagesize=A4,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles for markdown
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#2c3e50')
        )
        
        h1_style = ParagraphStyle(
            'CustomH1',
            parent=styles['Heading1'],
            fontSize=18,
            spaceBefore=20,
            spaceAfter=12,
            textColor=HexColor('#2c3e50')
        )
        
        h2_style = ParagraphStyle(
            'CustomH2',
            parent=styles['Heading2'],
            fontSize=16,
            spaceBefore=16,
            spaceAfter=10,
            textColor=HexColor('#34495e')
        )
        
        h3_style = ParagraphStyle(
            'CustomH3',
            parent=styles['Heading3'],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=8,
            textColor=HexColor('#34495e')
        )
        
        # Build PDF content
        story = []
        
        # Title
        story.append(Paragraph(f"Research Report: {query}", title_style))
        story.append(Spacer(1, 20))
        
        # Metadata
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Paragraph(f"<b>Query:</b> {query}", styles['Normal']))
        story.append(Spacer(1, 30))
        
        # Process markdown content
        lines = content.split('\n')
        current_paragraph = []
        
        for line in lines:
            line = line.strip()
            
            if not line:  # Empty line
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), styles['Normal']))
                    story.append(Spacer(1, 12))
                    current_paragraph = []
                continue
            
            # Handle headers
            if line.startswith('# '):
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), styles['Normal']))
                    current_paragraph = []
                story.append(Spacer(1, 16))
                story.append(Paragraph(line[2:], h1_style))
                continue
            elif line.startswith('## '):
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), styles['Normal']))
                    current_paragraph = []
                story.append(Spacer(1, 12))
                story.append(Paragraph(line[3:], h2_style))
                continue
            elif line.startswith('### '):
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), styles['Normal']))
                    current_paragraph = []
                story.append(Spacer(1, 10))
                story.append(Paragraph(line[4:], h3_style))
                continue
            elif line.startswith('#### '):
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), styles['Normal']))
                    current_paragraph = []
                story.append(Spacer(1, 8))
                story.append(Paragraph(f"<b>{line[5:]}</b>", styles['Normal']))
                continue
            
            # Handle bold and italic text
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)
            
            # Handle bullet points
            if line.startswith('- ') or line.startswith('* '):
                if current_paragraph:
                    story.append(Paragraph(' '.join(current_paragraph), styles['Normal']))
                    current_paragraph = []
                story.append(Paragraph(f"• {line[2:]}", styles['Normal']))
                continue
            
            # Regular text
            current_paragraph.append(line)
        
        # Add any remaining paragraph
        if current_paragraph:
            story.append(Paragraph(' '.join(current_paragraph), styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        # Return PDF file
        return FileResponse(
            tmp_filename,
            media_type='application/pdf',
            filename=f"research_report_{query.replace(' ', '_')[:30]}.pdf"
        )
        
    except Exception as e:
        logger.error(f"PDF generation error: {e}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.get("/health", response_class=JSONResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "research_team_ready": research_team is not None,
        "cost_tracking_enabled": config.enable_cost_tracking if config else False,
        "websocket_connections": len(connection_manager.active_connections)
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
