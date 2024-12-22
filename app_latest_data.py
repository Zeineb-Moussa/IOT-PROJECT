from flask import Flask, jsonify
from flask_cors import CORS  
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# MongoDB Atlas connection URI (example, replace with your actual URI)
uri = "mongodb+srv://username:password@cluster.example.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

# Connect to the database and collection
db = client["prevention_avc"]
patients_collection = db["patients"]

# Function to convert MongoDB documents for JSON serialization
def serialize_mongo_document(document):
    """
    Convert MongoDB documents to JSON-serializable format.
    """
    if document is None:
        return None
    serialized = {}
    for key, value in document.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()  
        else:
            serialized[key] = value
    return serialized

@app.route('/latest-data', methods=['GET'])
def get_latest_data():
    """
    Retrieve the latest inserted data from the collection.
    """
    try:
        # Find the most recently inserted document (sorted by descending timestamp)
        latest_document = patients_collection.find_one(sort=[("timestamp", -1)])
        
        if latest_document:
            # Convert the document to a JSON-serializable format
            serialized_data = serialize_mongo_document(latest_document)
            return jsonify({
                "success": True,
                "data": serialized_data
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "No data found."
            }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Server error: " + str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

