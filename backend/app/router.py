from langgraph.graph import StateGraph
from langgraph.prebuilt import create_llm_router
from langchain_openai import ChatOpenAI
from .agents.data_agent import DataAgent
from .agents.doc_agent import DocAgent

data_agent = None
doc_agent = None

def init_agents():
    global data_agent, doc_agent
    data_agent = DataAgent()
    doc_agent = DocAgent()

def shutdown_agents():
    global data_agent, doc_agent
    data_agent = None
    doc_agent = None

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

destinations = {
    "data": "Handles queries about groundwater statistics, state/year data, tables",
    "methodology": "Handles queries about GEC methodology, calculation rules, estimation process"
}

router = create_llm_router(destinations=destinations, llm=llm)

graph = StateGraph()

graph.add_node("router", router)

def data_agent_node(state):
    return {"output": data_agent.handle_query(state["input"], state.get("lang", "en"))}
graph.add_node("data", data_agent_node)

def doc_agent_node(state):
    return {"output": doc_agent.handle_query(state["input"], state.get("lang", "en"))}
graph.add_node("methodology", doc_agent_node)

graph.add_edge("router", "data", condition=lambda state: state["destination"] == "data")
graph.add_edge("router", "methodology", condition=lambda state: state["destination"] == "methodology")

graph.set_entry_point("router")

def handle_query(query: str, lang: str = "en"):
    result = graph.invoke({"input": query, "lang": lang})
    return result["output"]
