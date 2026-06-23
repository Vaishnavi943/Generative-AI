# PARALLEL WORKFLOW

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import TypedDict


# define state
class BatsmanState(TypedDict):
    # input
    runs: int
    balls: int
    four: int
    sixes: int

    # to calculate
    sr: float
    bpb: float
    boundary_percent: float
    summary: str


# define nodes fun
def calculate_strike_rate(state: BatsmanState) -> BatsmanState:

    sr = (state['runs']/state['balls'])*100

    return {'sr' : sr}


def calculate_bpb(state: BatsmanState) -> BatsmanState:

    bpb = state['balls'] / (state['four'] + state['sixes'])

    return {'bpb': bpb}


def calculate_boundary_percent(state: BatsmanState) -> BatsmanState:

    bp = (((state['four'] * 4) + (state['sixes'] * 6)) / state['runs']) * 100

    return {'boundary_percent': bp}


def summary(state: BatsmanState):

    summary = f"""
    Strike rate - {state['sr']} \n
    Balls per boundary - {state['bpb']} \n
    Boundary percent - {state['boundary_percent']} \n
    """
    return {'summary' : summary}



# graph
graph = StateGraph(BatsmanState)


# add nodes
graph.add_node('calculate_strike_rate', calculate_strike_rate)
graph.add_node('calculate_bpb', calculate_bpb)
graph.add_node('calculate_boundary_percent', calculate_boundary_percent)
graph.add_node('summary', summary)


# add edges
graph.add_edge(START, 'calculate_strike_rate')
graph.add_edge(START, 'calculate_bpb')
graph.add_edge(START, 'calculate_boundary_percent')

graph.add_edge('calculate_strike_rate', 'summary')
graph.add_edge('calculate_bpb', 'summary')
graph.add_edge('calculate_boundary_percent', 'summary')

graph.add_edge('summary' , END)


# compile
workflow = graph.compile()


initial_state = {
    'runs': 100,
    'balls': 50,
    'four': 6,
    'sixes': 4

}

output = workflow.invoke(initial_state)

print(output)



















