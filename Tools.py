from langchain.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper


@tool
def Search_engine(query : str)-> str:
    """
    Search the internet for current information.
    Use this tool whenever:
    - the user asks about current events
    - the user asks for recent information
    - the user asks for live prices
    - the answer is not likely in training data
    Args:
        query: Optimized search keywords
    """
    search = DuckDuckGoSearchAPIWrapper(max_results=3)
    return search.run(query)
    
@tool 
def wiki_knowledge_base(query : str) -> str:
    """
    Search the knowledge base for the information,
    Use the tool whenever : 
    - To confirm the response is correct.
    - To extract relaible information and facts.
    - The answer is not likely in the training data.
    Args : 
        query : obtimised search keywords
    """
    wiki_wrapper = WikipediaAPIWrapper(
        top_k_results=2,
        doc_content_chars_max=500)
    
    wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)
    
    return wiki_tool.run(query)

@tool
def results_log():
    """
    
    """
    return 

@tool 
def Coding_agent():
    """

    """
    return 
  

