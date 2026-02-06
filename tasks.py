from crewai import Task
from textwrap import dedent

class NewsTasks:
    def analyze_articles(self, agent, topic, article_count, focus_areas):
        """
            Creates a task for the agent to analyze news articles on a specific topic.

            The task requires the agent to:
            - Find and analyze recent news articles on the specified topic.
            - Extract key information, quotes, and statistics from articles.
            - Identify different perspectives and viewpoints on the topic.
            - Summarize findings with actionable insights.

            The task parameters are:
            - Topic: The specific news topic to analyze.
            - Article Count: Number of articles to analyze.
            - Focus Areas: Specific aspects to focus on during analysis.

            Returns:
                Task: The fully defined task for news article analysis.
        """
        return Task(
                    description = dedent(f"""**Task**: Analyze News Articles on Specific Topic
                                    **Description**: Conduct a thorough analysis of recent news articles on {topic}. 
                                    Extract key information, identify different perspectives, analyze sentiment, and provide 
                                    a comprehensive summary with insights. Focus on credible sources and verify information 
                                    across multiple outlets to ensure accuracy and completeness.
                                    **Parameters**: 
                                    - Topic: {topic}
                                    - Article Count: {article_count}
                                    - Focus Areas: {focus_areas}"""),
                    agent=agent,
                    expected_output=dedent("""A structured analysis including:
                        - Key findings and insights
                        - Perspectives and sentiment overview
                        - Notable quotes and statistics
                        - Summary with actionable takeaways"""))
    

    def evaluate_sources(self, agent, topic, source_types, credibility_criteria):
        """
            Determines the most reliable news sources for a given topic.

            This task involves analyzing multiple news sources by evaluating their credibility, 
            bias levels, and reporting quality. The selected sources should provide comprehensive 
            and accurate coverage of the topic. The output should be a comprehensive report that includes:
            - Source credibility assessments
            - Bias analysis and political leanings
            - Quality of reporting and fact-checking
            - Coverage breadth and depth evaluation

            Parameters:
            - agent (Agent): The AI agent responsible for executing the task.
            - topic (str): The news topic to evaluate sources for.
            - source_types (list): Types of sources to evaluate (newspapers, TV, online, etc.).
            - credibility_criteria (list): Criteria for assessing source reliability.

            Returns:
            - Task: A CrewAI task assigned to the agent for news source evaluation.
        """
        return Task(description = dedent(f"""**Task**: Evaluate News Source Credibility and Reliability
                                     **Objective**: Analyze multiple news sources and assess their reliability 
                                     for covering {topic}. Provide rankings based on credibility and quality metrics.

                                     **Key Considerations**:
                                        - Assess source credibility, fact-checking standards, and editorial policies.
                                        - Analyze potential bias, political leanings, and reporting objectivity.
                                        - Evaluate coverage quality, depth, and journalistic standards.
                                        - Consider source track record and reputation in the industry.

                                     **Evaluation Details**:
                                        - Topic Focus: {topic}
                                        - Source Types: {source_types}
                                        - Credibility Criteria: {credibility_criteria}"""),
                    agent=agent,
                    expected_output=dedent("""A ranked list of sources with:
                        - Credibility scores and justifications
                        - Bias analysis and leanings
                        - Reporting quality notes
                        - Coverage breadth/depth assessment"""))

    

    def monitor_trending_topics(self, agent, categories, time_period, regions):
        """
            Monitors and analyzes trending news topics across different categories.

            This task involves tracking trending topics in news and social media to identify 
            emerging stories, viral content, and developing news events. The goal is to provide 
            real-time insights into what stories are gaining traction and why.

            Parameters:
            - agent (Agent): The AI agent responsible for monitoring and analyzing trends.
            - categories (list): News categories to monitor (politics, technology, sports, etc.).
            - time_period (str): The timeframe for trend analysis.
            - regions (list): Geographic regions to focus monitoring on.

            Returns:
            - Task: A CrewAI task assigned to the agent for trending topic monitoring.
        """

        return Task(description = dedent(f""" **Task**: Monitor and Analyze Trending News Topics  
                                    **Objective**: Track trending topics across {categories} to identify emerging stories,
                                    viral content, and developing news events. Provide insights into story momentum and public interest.
                                    **Key Insights to Include**:
                                            - Top trending topics and their growth patterns.
                                            - Social media engagement metrics and viral potential.
                                            - Geographic distribution of interest and regional variations.
                                            - Timeline analysis showing how topics develop and spread.
                                        **Monitoring Parameters**:
                                            - Categories: {categories}
                                            - Time Period: {time_period}
                                            - Regions: {regions}"""),
                    agent=agent,
                    expected_output=dedent("""A trends report including:
                        - Top trending topics with momentum
                        - Engagement metrics
                        - Regional interest patterns
                        - Timeline of development"""))

    def research_news(self, agent, topics):
        """
            Creates a task for the agent to research and gather news on specified topics.

            This task involves comprehensive news research that includes finding current news,
            analyzing trends, and providing insights on the given topics. The agent will:
            - Search for the latest news articles on each topic
            - Analyze key trends and developments
            - Summarize findings in a structured report
            - Identify important events and their implications

            Parameters:
            - agent (Agent): The AI agent responsible for news research
            - topics (list): List of topics to research

            Returns:
            - Task: A CrewAI task for comprehensive news research
        """
        return Task(
            description=dedent(f"""**Task**: Comprehensive News Research and Analysis
                            **Objective**: Research and analyze current news on the specified topics, providing 
                            a detailed report with insights, trends, and key developments.

                            **Research Requirements**:
                            - Search for the latest news articles on each topic
                            - Identify key trends, patterns, and developments
                            - Analyze the significance and implications of major events
                            - Summarize findings in a clear, structured format
                            - Include relevant dates, sources, and context

                            **Output Format**:
                            - Executive summary of key findings
                            - Detailed analysis for each topic
                            - Timeline of important events
                            - Trend analysis and implications
                            - Source citations and reliability assessment

                            **Research Parameters**:
                            - Topics: {topics}
                            - Focus: Current events and recent developments"""),
            agent=agent,
            expected_output=dedent("""A comprehensive report covering:
                - Executive summary
                - Topic-by-topic analysis
                - Event timeline
                - Trend implications
                - Source citations"""),
        )

    def general_inquiry(self, agent, query):
        """
            Creates a task for the agent to answer a general inquiry question.

            This task involves researching and answering questions on various topics
            that are not specifically news-related. The agent will:
            - Search for relevant information on the topic
            - Synthesize information from multiple sources
            - Provide a clear, comprehensive answer
            - Include context and relevant details

            Parameters:
            - agent (Agent): The AI agent responsible for answering the inquiry
            - query (str): The question or inquiry to answer

            Returns:
            - Task: A CrewAI task for general inquiry answering
        """
        return Task(
            description=dedent(f"""**Task**: Answer General Inquiry Question
                            **Objective**: Research and provide a comprehensive answer to the following question:
                            
                            {query}

                            **Requirements**:
                            - Search for accurate, relevant information
                            - Synthesize information from multiple reliable sources
                            - Provide clear, well-structured explanation
                            - Include context, examples, and relevant details
                            - Cite sources and maintain objectivity

                            **Output Format**:
                            - Direct answer to the question
                            - Supporting details and explanation
                            - Relevant context and examples
                            - Source citations"""),
            agent=agent,
            expected_output=dedent("""A comprehensive answer including:
                - Clear response to the inquiry
                - Supporting details and explanation
                - Relevant context and examples
                - Source citations"""),
        )