from fastapi import APIRouter, HTTPException, status, Query
from models.models import UploadData
from services.relationship_service import upload_graph, fetch_relationships,validate_graph


router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_graph_endpoint(data: UploadData):
    try:
        # Validate the graph
        graph = validate_graph(data.graph)

        # Upload the graph to MongoDB
        return upload_graph(graph)
    except HTTPException as e:
        raise e

@router.get("/fetch")
async def fetch_relationships_endpoint(
    element_id: str,
    direction: str = Query(..., description="Direction of traceability (upward/downward)"),
    levels: int = Query(-1, description="Number of levels to trace (optional)"),
):
    try:
        # Fetch relationships from MongoDB
        return fetch_relationships(element_id, direction, levels)
    except HTTPException as e:
        raise e