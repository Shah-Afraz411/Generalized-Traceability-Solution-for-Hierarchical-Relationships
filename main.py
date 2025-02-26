

from fastapi import FastAPI
from routes.relationship_routes import router as relationship_router
from database.db import client

app = FastAPI()

# Include the relationship routes
app.include_router(relationship_router, prefix="/api")

# Close the MongoDB connection when the app shuts down
@app.on_event("shutdown")
def shutdown_db_client():
    client.close()