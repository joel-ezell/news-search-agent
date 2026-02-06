from crewai import Agent
# Provide a compatibility layer: prefer `LLM` if available, otherwise fall back to ChatOpenAI
from textwrap import dedent
import os
from dotenv import load_dotenv

try:
    from crewai import LLM as CrewLLM
    def _make_llm(model, api_key, base_url, timeout=30):
        return CrewLLM(provider="groq", model=model, api_key=api_key, base_url=base_url, timeout=timeout)
except Exception:
    from crewai.agent import ChatOpenAI
    def _make_llm(model, api_key, base_url, timeout=30):
        return ChatOpenAI(model=model, api_key=api_key, base_url=base_url, timeout=timeout)

# Import tool instances (Tool objects) exported by the modules
from tools.search_news import search_news_tool
from tools.search_internet import search_internet_tool
from tools.calculator_tools import calculator_tool


class NewsAgents:
    def __init__(self):
        """
        Initializes the NewsAgents class by setting up the Groq LLM model.
        This model will be used by all the news agents in the crew.
        """
        # Load environment variables
        load_dotenv()
        groq_api_key = os.getenv("GROQ_API_KEY")

        # Configure LLM (use compatibility factory to choose the available client)
        model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.llm = _make_llm(model_name, groq_api_key, "https://api.groq.com/openai/v1", timeout=30)

    def news_analyst(self):
        """
        Sets up a 'News Analyst' to analyze and interpret news articles and trends.
        """
        return Agent(
            role="News Analyst",
            backstory=f"""I'm a seasoned expert in news analysis and interpretation. With years of experience in journalism and media analysis, I specialize in breaking down complex news stories and identifying key trends and implications.""",
            goal=f"""Analyze news articles, identify key trends, extract meaningful insights, and provide comprehensive analysis of current events and their broader implications.""",
            # Pass the instantiated tool methods to the agent
            tools=[
                search_news_tool,
                search_internet_tool
            ],
            verbose=True,
            llm=self.llm,
        )

    def source_verification_specialist(self):
        """
        Creates a 'Source Verification Specialist' agent to evaluate news source credibility and fact-check information.
        """
        return Agent(
            role="Source Verification Specialist",
            backstory=dedent(f"""A professional fact-checker and source verification expert who specializes in evaluating 
                                    the credibility of news sources and verifying the accuracy of information."""),
            goal=dedent(f"""
                        Verify the credibility of news sources, fact-check information, assess bias levels, and ensure 
                        the reliability of news content before it's reported or analyzed."""
                       ),
            # Pass the instantiated tool method to the agent
            tools=[search_internet_tool, search_news_tool],
            verbose=True,
            llm=self.llm,
        )

    def trending_topics_monitor(self):
        """
        Sets up a 'Trending Topics Monitor' agent to track viral news and emerging stories.
        """
        return Agent(
            role="Trending Topics Monitor",
            backstory=dedent(f"""
                                     A social media and news trend expert who specializes in identifying viral content,
                                     emerging stories, and breaking news across multiple platforms and sources."""),
            goal=dedent(f"""
                                Monitor trending topics, identify viral news stories, track story development over time,
                                and provide insights into what content is gaining traction and why."""),
            # Pass the instantiated tool method to the agent
            tools=[search_news_tool, search_internet_tool],
            verbose=True,
            llm=self.llm,
        )

    def news_researcher(self):
        """
        Sets up the primary news researcher agent for comprehensive news gathering and research.
        """
        return Agent(
            role="News Researcher",
            backstory=dedent(f"""
                                    A comprehensive news research specialist with expertise in gathering information from multiple sources,
                                    synthesizing complex topics, and providing thorough analysis of current events."""),
            goal=dedent(f"""
                                Conduct thorough research on specified topics, gather information from multiple reliable sources,
                                and provide comprehensive, well-structured reports on current events and news topics."""),
            # Pass the instantiated tool method to the agent
            tools=[search_news_tool, search_internet_tool],
            verbose=True,
            llm=self.llm,
        )
