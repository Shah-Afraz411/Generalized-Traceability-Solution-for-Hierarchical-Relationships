<<<<<<< HEAD


from fastapi import FastAPI
from routes.relationship_routes import router as relationship_router
from database.db import client

app = FastAPI()

# Include the relationship routes
app.include_router(relationship_router, prefix="/api")

# Close the MongoDB connection when the app shuts down
@app.on_event("shutdown")
def shutdown_db_client():
=======


from fastapi import FastAPI
from routes.relationship_routes import router as relationship_router
from database.db import client

app = FastAPI()

# Include the relationship routes
app.include_router(relationship_router, prefix="/api")

# Close the MongoDB connection when the app shuts down
@app.on_event("shutdown")
def shutdown_db_client():
>>>>>>> ab0d64793e4c444266f05392e3a5ed8a4ac226d7
    client.close()