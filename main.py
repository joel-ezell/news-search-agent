from textwrap import dedent
from crew import NewsResearchCrew

if __name__ == "__main__":
    print("## Welcome to the News Research Crew")
    print('-------------------------------')

    topics = input(dedent("What news topics would you like to research? (separate multiple topics with commas)\n"))
    
    # Convert topics string to list
    topic_list = [topic.strip() for topic in topics.split(',')]

    news_crew = NewsResearchCrew(topic_list)
    result = news_crew.run()

    print("\n\n########################")
    print("## Here is your News Research Report")
    print("########################\n")
    print(result)
