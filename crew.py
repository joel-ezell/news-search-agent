from crewai import Crew
from agents import NewsAgents       # Updated to use NewsAgents class
from tasks import NewsTasks         # Updated to use NewsTasks class

from dotenv import load_dotenv
load_dotenv()

class NewsResearchCrew:
    def __init__(self, topics, search_depth="comprehensive"):
        self.topics = topics
        self.search_depth = search_depth
    
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
            self.topics,
            self.search_depth
        )

        # Create and run the News Research Crew
        news_crew = Crew(
            agents=[news_researcher],
            tasks=[news_research_task],
            verbose=True,
        )

        result = news_crew.kickoff()
        return result


