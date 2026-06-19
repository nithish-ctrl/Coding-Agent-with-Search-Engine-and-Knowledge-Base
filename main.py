from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode
from Tools import Search_engine, wiki_knowledge_base, results_log, To_do, Notes_tool, Notes_from_Documents, Resume_Analyzer
from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI 
from Prompt_template import System_prompt
from langchain_mistralai import ChatMistralAI


load_dotenv()

llm = ChatMistralAI(model_name="mistral-medium-3-5")
Tools = [Search_engine, wiki_knowledge_base, results_log, To_do, Notes_tool, Notes_from_Documents, Resume_Analyzer]
llm = llm.bind_tools(tools=Tools)

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]


def Process_agent(state : AgentState) -> AgentState:
    system_prompt = System_prompt
    
    combined_messages = [
    SystemMessage(content=system_prompt),
    *state["messages"]
    ]
    
    response = llm.invoke(combined_messages)

    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")
    
    return {"messages" : [response]} 

def should_continue(state : AgentState) -> str:
    """
    To decide whether to continue or end it.
    """
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls : 
        return "continue"
    else : return "end"

graph = StateGraph(AgentState)
graph.add_node("AgentCall",Process_agent)


Toolnode = ToolNode(tools=Tools)
graph.add_node("ToolNode", Toolnode)

graph.add_edge(START, "AgentCall")
graph.add_conditional_edges(
    "AgentCall",
    should_continue,
    {
        "end" : END,
        "continue" : "ToolNode"
    }
)
graph.add_edge("ToolNode", "AgentCall")
agent = graph.compile()

def run_agent():
    print("______________________________________________________________________________________________________________")
    user_input = input("Enter the prompt : ")
    inputs = {"messages": [("user", user_input)]}

    for output in agent.stream(inputs, stream_mode="updates"):  # type: ignore
        
        if "AgentCall" in output:
            message = output["AgentCall"]["messages"][0]
            
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    print(f"\n[LLM]: Searching Tools for: \"{tool_call['args'].get('query')}\"")
            
            elif message.content:
                #print(f"\n[LLM]: {message.content[0]['text']}") This is extract the text from Google Gemini Model
                print(f'LLM : {message.content}')
        
        elif "ToolNode" in output:
            tool_message = output["ToolNode"]["messages"][0]
            print(f"\n[Tools]: Found search results. Sending data back to LLM...")
    
    print("___________________________________________________________________________________________________________________")

if __name__ == "__main__":
    run_agent()
    

  
    
