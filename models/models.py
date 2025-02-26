from pydantic import BaseModel, Field
from typing import List,Dict



class UploadData(BaseModel):
    graph: Dict[str, List[str]] = Field(..., description="Graph structure representing hierarchical relationships")