import csv
from pymongo import MongoClient
import settings

def export_mongo_to_csv(collection_name, output_file):
    """
    Fetches all documents from a Mongo collection and writes them to a CSV.
    Automatically handles dynamic headers for inconsistent attributes.
    """
    try:
        # 1. Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017")
        db = client['Fastnel']
        collection = db[collection_name]
        
        # 2. Fetch all data (excluding Mongo's internal _id)
        data = list(collection.find({}, {"_id": 0}))
        
        if not data:
            print("No data found in the collection to export.")
            return

        # 3. Dynamically identify the Header
        # We look through every document to find all unique keys.
        # This ensures that if one product has a 'material' but others don't, 
        # the column is still created.
        
        # Sort headers alphabetically for a consistent CSV layout

        headers = settings.CSV_HEADERS

        # 4. Write to CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            
            # Write column names
            writer.writeheader()
            
            # Write rows
            writer.writerows(data)
            
        print(f"Successfully exported {len(data)} records to {output_file}")

    except Exception as e:
        print(f"An error occurred during export: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    # Settings
    COLLECTION_TO_EXPORT = "pdp_final_data"
    FILE_NAME = "fastenal_2026_02_03.csv"
    
    export_mongo_to_csv("fastnel_electrical_data","fastenal_2026_02_04.csv")