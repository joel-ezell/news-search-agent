from crewai import Agent, LLM
from textwrap import dedent
import os
from dotenv import load_dotenv

# Correctly import the tool classes
from tools.search_news import SearchNews
from tools.search_tools import SearchTools
from tools.calculator_tools import CalculatorTools

# Instantiate the tools to make them available to the agents
search_news_tool = SearchNews()
search_tool = SearchTools()
calculator_tool = CalculatorTools()


class NewsAgents:
    def __init__(self):
        """
        Initializes the NewsAgents class by setting up the Groq LLM model.
        This model will be used by all the news agents in the crew.
        """
        # Load environment variables
        load_dotenv()
        groq_api_key = os.getenv("GROQ_API_KEY")

        # Configure CrewAI's native LLM provider to Groq to avoid OpenAI fallback
        # This ensures all agent calls use Groq's API directly.
        self.llm = LLM(
            provider="groq",
            model="groq/llama-3.3-70b-versatile",
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )

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
                search_tool
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
            tools=[search_tool, search_news_tool],
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
            tools=[search_news_tool, search_tool],
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
            tools=[search_news_tool, search_tool],
            verbose=True,
            llm=self.llm,
        )
