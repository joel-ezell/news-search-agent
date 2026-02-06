from crewai import Crew
from agents import NewsAgents       # Updated to use NewsAgents class
from tasks import NewsTasks         # Updated to use NewsTasks class
from agents import _make_llm
import os
from dotenv import load_dotenv

load_dotenv()

class QueryRouter:
    """Routes queries to either news or general inquiry based on content analysis."""
    
    def __init__(self):
        groq_api_key = os.getenv("GROQ_API_KEY")
        model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.llm = _make_llm(model_name, groq_api_key, "https://api.groq.com/openai/v1", timeout=30)
    
    def route_query(self, query):
        """
        Determines if a query is news-related or general inquiry.   
        Returns 'news' or 'general'.
        """
        prompt = f"""You are a query classifier. Determine if the following query is asking for NEWS/current events information or if it's a GENERAL inquiry about a topic.

News-related queries ask about:
- Current events, breaking news, recent developments
- What's happening right now in the world
- Latest developments in sports, technology, finance, politics, etc.
- Recent news stories

General inquiry queries ask about:
- How things work, explanations of concepts
- Historical information
- General knowledge, facts, definitions
- Non-time-sensitive information
- Educational topics

Query: "{query}"

Respond with ONLY one word: "news" or "general"."""

        try:
            # Use invoke which is the current standard interface for LangChain
            from langchain_core.messages import HumanMessage
            response = self.llm.invoke([HumanMessage(content=prompt)])
            
            # Extract text from the response object
            result_text = response.content if hasattr(response, 'content') else str(response)
            result = result_text.lower().strip()
            
            # Ensure we return either 'news' or 'general'
            if 'news' in result:
                return 'news'
            elif 'general' in result:
                return 'general'
            else:
                # Default to general if uncertain
                return 'general'
        except Exception as e:
            print(f"Error in query routing: {e}")
            # Default to general on error
            return 'general'

class NewsResearchCrew:
    def __init__(self, topics):
        self.topics = topics
    
    def run(self):
        """
            Executes the news research process by:

            1. Initializing the news research agent.
            2. Assigning news gathering and analysis tasks.
            3. Creating a Crew to coordinate and execute news research.
            4. Running the Crew to generate comprehensive news reports.

            Returns:
                str: A comprehensive news research report covering the specified topics.
        """
        
        # Initialize news agents and tasks
        news_agents = NewsAgents()    # Updated to use NewsAgents class
        news_tasks = NewsTasks()      # Updated to use NewsTasks class

        # Create agent instance
        news_researcher = news_agents.news_researcher()

        # Assign news research task to agent
        news_research_task = news_tasks.research_news(
            news_researcher,
            self.topics
        )

        # Create and run the News Research Crew
        news_crew = Crew(
            agents=[news_researcher],
            tasks=[news_research_task],
            verbose=True,
        )

        result = news_crew.kickoff()
        return result


class GeneralInquiryCrew:
    def __init__(self, query):
        self.query = query
    
    def run(self):
        """
            Executes the general inquiry process by:

            1. Initializing the general inquiry agent.
            2. Assigning the inquiry task.
            3. Creating a Crew to coordinate and execute the inquiry.
            4. Running the Crew to generate a comprehensive answer.

            Returns:
                str: A comprehensive answer to the user's inquiry.
        """
        
        # Initialize agents and tasks
        agents = NewsAgents()
        tasks = NewsTasks()

        # Create agent instance
        inquiry_agent = agents.general_inquiry_agent()

        # Assign inquiry task to agent
        inquiry_task = tasks.general_inquiry(inquiry_agent, self.query)

        # Create and run the General Inquiry Crew
        inquiry_crew = Crew(
            agents=[inquiry_agent],
            tasks=[inquiry_task],
            verbose=True,
        )

        result = inquiry_crew.kickoff()
        return result
