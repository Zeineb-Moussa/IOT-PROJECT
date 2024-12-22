import pymongo
import random
import time
from datetime import datetime

# MongoDB Atlas connection URI (example, replace with your actual URI)
uri = "mongodb+srv://username:password@cluster.example.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = pymongo.MongoClient(uri)

# Access the database and the collection
db = client["prevention_avc"]
patients_collection = db["patients"]

# Function to generate random biometric values
def generate_real_time_data():
    systolic = random.randint(90, 140)  # Systolic pressure in mmHg
    diastolic = random.randint(60, 90)  # Diastolic pressure in mmHg
    return {
        "blood_pressure": {"systolic": systolic, "diastolic": diastolic},
        "heart_rate": random.randint(60, 120),       # Heart rate in BPM
        "oxygen_saturation": random.randint(90, 100), # Oxygen saturation in %
        "temperature": round(random.uniform(36.0, 39.0), 1)  # Temperature in °C
    }

# Function to insert real-time data into MongoDB
def insert_real_time_data():
    patient_data = {
        "first_name": "patient_first_name",
        "last_name": "patient_last_name",
        "birth_date": datetime(1985, 5, 23),  
        "address": "123 Main Street",
        "emergency_contacts": ["0612345678", "0698765432"],
        "active_monitoring": True,
        "medical_history": ["hypertension", "diabetes"],
        "emergency_number": "112",
        "real_time_biometric_data": generate_real_time_data(),
        "timestamp": datetime.now()  # Add timestamp field for timeField
    }
    
    # Insert the document into the collection
    patients_collection.insert_one(patient_data)
    print("Real-time data inserted:", patient_data)

# Loop to generate and insert data every 10 seconds
try:
    while True:
        insert_real_time_data()
        time.sleep(10)
except KeyboardInterrupt:
    print("\nProgram stopped by the user.")

