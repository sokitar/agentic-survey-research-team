"""
AI Agents for the Agentic Survey Research Team using CrewAI
"""

from crewai import Agent, Task, Crew
import logging
import time

class ResearchCoordinator:
    """Coordinates the entire research process and shows background actions"""
    
    def __init__(self, llm, logger=None):
        self.llm = llm
        self.logger = logger or logging.getLogger(__name__)
        self.coordinator_agent = self._create_coordinator_agent()
    
    def _create_coordinator_agent(self):
        """Create the Research Coordinator agent"""
        return Agent(
            role="Research Coordinator",
            goal="Coordinate comprehensive academic research on any given topic",
            backstory="""You are an expert research coordinator with deep knowledge 
            of academic literature across all fields. You break down research requests 
            into actionable steps, coordinate with specialist agents, and ensure 
            comprehensive coverage of the topic.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
    
    def create_research_task(self, research_query):
        """Create a research coordination task"""
        return Task(
            description=f"""
            Coordinate a comprehensive research investigation on: {research_query}
            
            Your responsibilities:
            1. Analyze the research query and break it down into key areas
            2. Identify what types of papers and sources would be most relevant
            3. Plan the research strategy and approach
            4. Coordinate with specialist agents (when they become available)
            5. Ensure comprehensive coverage of the topic
            
            For now, provide a detailed research plan and initial analysis since 
            the specialist agents are still being implemented.
            
            Research Query: {research_query}
            """,
            agent=self.coordinator_agent,
            expected_output="""A comprehensive research plan including:
            - Key research areas to explore
            - Types of papers/sources to search for
            - Initial analysis and approach
            - Next steps for investigation"""
        )
    
    def execute_research(self, research_query):
        """Execute the research coordination process"""
        self.logger.info(f"🔍 Starting research coordination for: {research_query}")
        
        # Show background action
        print(f"\n🤖 Research Coordinator: Analyzing your request...")
        print(f"📋 Topic: {research_query}")
        
        # Create and execute the research task
        task = self.create_research_task(research_query)
        
        # Create a simple crew with just the coordinator for now
        crew = Crew(
            agents=[self.coordinator_agent],
            tasks=[task],
            verbose=True
        )
        
        print(f"\n🔄 Research Coordinator: Planning comprehensive research strategy...")
        
        try:
            result = crew.kickoff()
            self.logger.info("Research coordination completed successfully")
            return str(result)
        except Exception as e:
            self.logger.error(f"Error in research coordination: {e}")
            return f"Sorry, I encountered an error while coordinating the research: {str(e)}"

class LiteratureSearcher:
    """Agent for finding and searching academic literature"""
    
    def __init__(self, llm, logger=None):
        self.llm = llm
        self.logger = logger or logging.getLogger(__name__)
        self.searcher_agent = self._create_searcher_agent()
        self.logger.info("Literature Searcher agent initialized")
    
    def _create_searcher_agent(self):
        """Create the Literature Search agent"""
        return Agent(
            role="Literature Searcher",
            goal="Find and identify the most relevant academic papers and sources for research topics",
            backstory="""You are an expert academic librarian and research specialist 
            with access to major academic databases. You excel at creating targeted 
            search queries, identifying high-impact papers, and finding comprehensive 
            literature coverage for any research topic.""",
            verbose=True,
            llm=self.llm
        )
    
    def create_search_task(self, research_query):
        """Create a literature search task"""
        return Task(
            description=f"""
            Conduct a comprehensive literature search for: {research_query}
            
            Your responsibilities:
            1. Generate optimal search queries and keywords
            2. Identify key databases and sources to search
            3. Find the most relevant and recent papers (focus on 2020-2024)
            4. Prioritize high-impact journals and authoritative sources
            5. Provide a structured list of papers with titles, authors, and brief relevance notes
            
            Focus on finding 8-12 of the most relevant papers that would give 
            comprehensive coverage of the topic.
            
            Research Query: {research_query}
            """,
            agent=self.searcher_agent,
            expected_output="""A structured literature search result including:
            - Optimized search strategy
            - List of 8-12 key papers with titles, authors, publication info
            - Brief relevance explanation for each paper
            - Coverage assessment of the topic"""
        )

class PaperAnalyzer:
    """Agent for analyzing and synthesizing research findings"""
    
    def __init__(self, llm, logger=None):
        self.llm = llm
        self.logger = logger or logging.getLogger(__name__)
        self.analyzer_agent = self._create_analyzer_agent()
        self.logger.info("Paper Analyzer agent initialized")
    
    def _create_analyzer_agent(self):
        """Create the Paper Analysis agent"""
        return Agent(
            role="Research Analyst",
            goal="Analyze research findings and synthesize key insights from literature",
            backstory="""You are an expert research analyst with deep expertise in 
            synthesizing academic literature. You excel at identifying key themes, 
            methodologies, findings, and gaps across multiple research papers to 
            create comprehensive analysis and insights.""",
            verbose=True,
            llm=self.llm
        )

class ReportSynthesizer:
    """Agent for synthesizing final comprehensive research reports"""
    
    def __init__(self, llm, logger=None):
        self.llm = llm
        self.logger = logger or logging.getLogger(__name__)
        self.synthesizer_agent = self._create_synthesizer_agent()
        self.logger.info("Report Synthesizer agent initialized")
    
    def _create_synthesizer_agent(self):
        """Create the Report Synthesis agent"""
        return Agent(
            role="Research Report Writer",
            goal="Create comprehensive, easy-to-understand research reports from analyzed findings",
            backstory="""You are an expert academic writer and research synthesizer 
            with exceptional skills in creating clear, comprehensive research reports. 
            You excel at organizing complex research findings into well-structured, 
            accessible documents that serve both academic and general audiences.""",
            verbose=True,
            llm=self.llm
        )

class ResearchTeam:
    """Coordinates multiple agents working together in a research team"""
    
    def __init__(self, llm, logger=None):
        self.llm = llm
        self.logger = logger or logging.getLogger(__name__)
        
        # Initialize all agents
        print("⚙️  Initializing Research Team...")
        self.coordinator = ResearchCoordinator(llm, logger)
        self.searcher = LiteratureSearcher(llm, logger)
        self.analyzer = PaperAnalyzer(llm, logger)
        self.synthesizer = ReportSynthesizer(llm, logger)
        self.logger.info("Research Team initialized with all 4 agents")
        print("✅ Complete multi-agent research team ready")
    
    def execute_coordinated_research(self, research_query):
        """Execute complete research workflow ending with comprehensive report"""
        self.logger.info(f"🚀 Starting complete research workflow: {research_query}")
        
        # Show complete team action overview
        print(f"\n🔍 COMPLETE RESEARCH WORKFLOW ACTIVATED")
        print(f"📋 Query: {research_query}")
        print(f"👥 All Agents: Coordinator → Literature Searcher → Analyst → Report Writer")
        print("─" * 60)
        
        # Create all tasks in sequential workflow
        coordinator_task = Task(
            description=f"""
            As Research Coordinator, provide strategic direction for researching: {research_query}
            
            Create a focused research strategy including:
            1. Key research areas and scope
            2. Research methodology approach  
            3. Success criteria for the literature search
            4. Integration plan for findings
            
            Keep your response concise and actionable for the team.
            """,
            agent=self.coordinator.coordinator_agent,
            expected_output="Concise research strategy with clear direction for the team."
        )
        
        literature_task = Task(
            description=f"""
            Based on the Research Coordinator's strategy, conduct targeted literature search for: {research_query}
            
            Deliver:
            1. Optimized search keywords and strategy
            2. 6-8 most relevant recent papers (2020-2024)
            3. Key findings and research gaps identified
            4. Quality assessment of literature coverage
            
            Be comprehensive but organized in your findings.
            """,
            agent=self.searcher.searcher_agent,
            expected_output="Structured literature search results with key papers and coverage assessment."
        )
        
        analysis_task = Task(
            description=f"""
            Based on the literature search results, conduct deep analysis of the research findings for: {research_query}
            
            Your analysis should include:
            1. Synthesis of key themes and patterns across papers
            2. Identification of methodological approaches
            3. Summary of major findings and conclusions
            4. Critical gaps and limitations in current research
            5. Emerging trends and future directions
            
            Provide structured analysis that will inform the final report.
            """,
            agent=self.analyzer.analyzer_agent,
            expected_output="Comprehensive analysis of research findings with key insights and gaps."
        )
        
        report_task = Task(
            description=f"""
            Create a comprehensive, easy-to-understand research report on: {research_query}
            
            Based on all previous work (strategy, literature search, and analysis), write a complete report that includes:
            
            1. EXECUTIVE SUMMARY (2-3 paragraphs)
            2. INTRODUCTION & BACKGROUND
            3. METHODOLOGY (search strategy and approach)
            4. KEY FINDINGS & INSIGHTS
               - Major themes and patterns
               - Important research outcomes
               - Methodological insights
            5. RESEARCH GAPS & LIMITATIONS
            6. FUTURE DIRECTIONS & RECOMMENDATIONS
            7. CONCLUSION
            
            Write in clear, accessible language that serves both academic and general audiences.
            Make the report comprehensive yet engaging and easy to understand.
            Aim for approximately 2000-3000 words.
            """,
            agent=self.synthesizer.synthesizer_agent,
            expected_output="A comprehensive, well-structured research report of 2000-3000 words covering all aspects of the research topic."
        )
        
        # Create complete workflow crew
        crew = Crew(
            agents=[
                self.coordinator.coordinator_agent, 
                self.searcher.searcher_agent,
                self.analyzer.analyzer_agent,
                self.synthesizer.synthesizer_agent
            ],
            tasks=[coordinator_task, literature_task, analysis_task, report_task],
            verbose=True
        )
        
        # Execute complete workflow
        try:
            print("\n🤖 Research Coordinator: Developing research strategy...")
            print("📚 Literature Searcher: Preparing comprehensive search...")
            print("🔬 Research Analyst: Ready for deep analysis...")
            print("📝 Report Writer: Standing by for final synthesis...")
            print("\n🔄 Executing complete research workflow...")
            
            result = crew.kickoff()
            
            print("\n✅ COMPLETE RESEARCH REPORT GENERATED")
            print("📋 Full workflow completed: Strategy → Search → Analysis → Report")
            self.logger.info("Complete research workflow completed successfully")
            return str(result)
            
        except Exception as e:
            self.logger.error(f"Error in complete research workflow: {e}")
            return f"❌ Research team encountered an error: {str(e)}"
