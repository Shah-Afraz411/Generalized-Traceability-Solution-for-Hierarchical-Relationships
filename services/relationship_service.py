
from database.db import insert_graph, fetch_graph

from typing import Dict, List, Set
from collections import defaultdict
from fastapi import HTTPException, status

def detect_cycle(graph: Dict[str, List[str]], node: str, visited: Dict[str, bool], rec_stack: Dict[str, bool]) -> bool:
    """
    Helper function to detect cycles in the graph using DFS.
    """
    visited[node] = True
    rec_stack[node] = True

    for neighbor in graph.get(node, []):
        if not visited.get(neighbor, False):
            if detect_cycle(graph, neighbor, visited, rec_stack):
                return True
        elif rec_stack.get(neighbor, False):
            return True

    rec_stack[node] = False
    return False

def validate_graph(graph: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Validate the graph to ensure it is well-formed and free of errors.
    """
    # Check 1: Ensure all parent references exist in the graph
    all_nodes = set(graph.keys())
    child_nodes = set()

    for children in graph.values():
        child_nodes.update(children)

    # All child nodes must either be in the graph or have no children
    for child in child_nodes:
        if child not in all_nodes and graph.get(child, []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Parent reference does not exist for element: {child}",
            )

    # Check 2: Ensure no cycles in the graph
    visited = {node: False for node in graph}
    rec_stack = {node: False for node in graph}
    for node in graph:
        if not visited[node]:
            if detect_cycle(graph, node, visited, rec_stack):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cycle detected in relationships",
                )

    # Check 3: Ensure unique identifiers for all elements
    # Since the graph is a dictionary, keys are inherently unique.
    # No additional validation is needed for this.

    return graph
# Helper function to fetch upward relationships
def fetch_upward(graph: Dict[str, List[str]], element_id: str, levels: int) -> Dict[str, List[str]]:
    result = defaultdict(list)
    queue = [(element_id, 0)]
    visited = set()

    while queue:
        current, current_level = queue.pop(0)
        if current_level >= levels:
            break
        for parent, children in graph.items():
            if current in children and parent not in visited:
                visited.add(parent)
                result[current_level].append(parent)
                queue.append((parent, current_level + 1))

    return result

# Helper function to fetch downward relationships
def fetch_downward(graph: Dict[str, List[str]], element_id: str, levels: int) -> Dict[str, List[str]]:
    result = defaultdict(list)
    queue = [(element_id, 0)]
    visited = set()

    while queue:
        current, current_level = queue.pop(0)
        if current_level >= levels:
            break
        if current in graph:
            for child in graph[current]:
                if child not in visited:
                    visited.add(child)
                    result[current_level].append(child)
                    queue.append((child, current_level + 1))

    return result

# Function to upload graph to MongoDB
def upload_graph(graph: Dict[str, List[str]]):
    try:
        # Insert the graph into MongoDB
        if insert_graph(graph):
            return {"message": "Graph uploaded successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload graph to MongoDB",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )

# Function to fetch relationships from MongoDB
def fetch_relationships(element_id: str, direction: str, levels: int):
    try:
        # Retrieve the graph from MongoDB
        graph = fetch_graph()
        if not graph:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No graph data found",
            )

        # Fetch relationships based on direction
        if direction == "upward":
            result = fetch_upward(graph, element_id, levels)
        elif direction == "downward":
            result = fetch_downward(graph, element_id, levels)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid direction. Use 'upward' or 'downward'.",
            )

        return {element_id: {direction: result}}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
