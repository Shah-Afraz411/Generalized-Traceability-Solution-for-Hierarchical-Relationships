from typing import Dict, List
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = "mongodb+srv://Afraz:wg4qDUehDmqXkS0f@cluster0.h4mm0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_URI)
db = client["hierarchy_db"]
collection = db["relationships"]

def insert_graph(graph: Dict[str, List[str]]):
    try:
        # Insert the graph into the collection
        collection.insert_one({
            "graph": graph

        })
        return True
    except Exception as e:
        print(f"Error inserting graph into MongoDB: {e}")
        return False

# Function to fetch graph data from MongoDB
def fetch_graph() -> Dict[str, List[str]]:
    try:
        # Retrieve the graph from the collection
        graph_data = collection.find_one({}, {"graph": 1})
        if not graph_data:
            return None
        return graph_data["graph"]
    except Exception as e:
        print(f"Error fetching graph from MongoDB: {e}")
        return None

