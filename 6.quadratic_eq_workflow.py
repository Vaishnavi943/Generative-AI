# CONDITIONAL WORKFLOW

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

# state
class QuadState(TypedDict):
    # input
    a: int
    b: int
    c: int

    # output
    equation: str
    discriminant: float
    result: str


# define nodes
def show_equation(state: QuadState) -> QuadState:

    equation = f'{state["a"]}x^2{state["b"]}x{state["c"]}'
    return {'equation':  equation}


def calculate_discriminant(state: QuadState):

    discriminant = (state['b']**2) - (4*state['a']*state['c'])
    return {'discriminant': discriminant}


def real_roots(state: QuadState):

    root1 = (-state['b'] + state['discriminant']**0.5)/2*(state['a'])
    root2 = (-state['b'] - state['discriminant']**0.5)/2*(state['a'])
    result = f'The roots are {root1} & {root2}'
    return {'result': result}


def repeated_roots(state: QuadState):

    root = (-state['b'])/2*(state['a'])
    result = f'Only repeating root is {root}'
    return {'result': result}


def no_real_roots(state: QuadState):

    result = f'No real roots'
    return {'result': result}


# function to check condition(if-else type)
def check_condition(state: QuadState) -> Literal['real_roots', 'repeated_roots', 'no_real_roots']:

    if state['discriminant'] > 0:
        return "real_roots"
    
    elif state['discriminant'] == 0:
        return "repeated_roots"
    
    else:
        return "no_real_roots"


# graph
graph = StateGraph(QuadState)

graph.add_node('show_equation', show_equation)
graph.add_node('calculate_discriminant', calculate_discriminant)
graph.add_node('real_roots', real_roots)
graph.add_node('repeated_roots', repeated_roots)
graph.add_node('no_real_roots', no_real_roots)


graph.add_edge(START, 'show_equation')
graph.add_edge('show_equation', 'calculate_discriminant')

graph.add_conditional_edges('calculate_discriminant', check_condition)
graph.add_edge('real_roots', END)
graph.add_edge('repeated_roots', END)
graph.add_edge('no_real_roots', END)


# compile
workflow = graph.compile()

initial_state = {
    'a': 4,
    'b': -5,
    'c': -4

}

print(workflow.invoke(initial_state))



















