import os
import pymongo
from ensure import ensure_annotations
from pymongo.mongo_client import MongoClient
import pandas as pd
from pymongo.errors import ConnectionFailure
import json 
from typing import Optional , Any


class mongodb_operation:
    @ensure_annotations 
    def __init__(self,client_url: str):
        self.client_url = client_url
        self.client = None
 
    @ensure_annotations 
    def create_client(self):
        """Create a MongoDB client."""
        try:
            self.client = MongoClient(self.client_url)
            # Check if the client is connected by pinging the server
            self.client.admin.command('ping')
            print("Connected to MongoDB database")
            return client
        except ConnectionFailure as e:
            print(f"Error while connecting to MongoDB: {e}")
            self.client = None

    @ensure_annotations
    def create_database(self,database_name:Optional[str] = None):
        """Create or access a MongoDB database."""
        if not self.client:
            self.create_client()
        if self.client:
            database = self.client[database_name]
            print(f"Database '{database_name}' initialized.")
            return database
        else:
            print("Failed to create MongoDB client. Database not initialized.")
            return None
        
    @ensure_annotations
    def create_collection(self,database_name:Optional[str] = None,collection_name:Optional[str]=None):
        database = self.create_database(database_name)
        if database is not None:
            collection = database[collection_name]
            print(f"Collection '{collection_name}' initialized in database '{database_name}'.")
            return collection
        else:
            print("Failed to initialize collection.")
            return None

    @ensure_annotations
    def insert_single_record(self, record: dict, database_name: Optional[str] = None, collection_name: Optional[str] = None):
        """
        Insert a single record into a MongoDB collection.
        """
        if not isinstance(record, dict):
            raise TypeError("Record must be a dictionary for insert_record.")
        
        collection = self.create_collection(database_name, collection_name)
        if collection is not None:
            collection.insert_one(record)
            print("Inserted a single record successfully.")
        else:
            print("Failed to insert record. Collection not initialized.")

    @ensure_annotations
    def insert_multiple_records(self, records: list, database_name: Optional[str] = None, collection_name: Optional[str] = None):
        """
        Insert multiple records into a MongoDB collection.
        """
        if not all(isinstance(record, dict) for record in records):
            raise TypeError("All records must be dictionaries for insert_multiple_records.")
        
        collection = self.create_collection(database_name, collection_name)
        if collection is not None:
            collection.insert_many(records)
            print("Inserted multiple records successfully.")
        else:
            print("Failed to insert records. Collection not initialized.")

    @ensure_annotations    
    def bulk_insert(self, datafile: str, database_name: Optional[str] = None, collection_name: Optional[str] = None, unique_field: Optional[str] = None):
        """
        Insert multiple records into MongoDB from a CSV or XLSX file.
        """
        if not os.path.exists(datafile):
            print(f"Error: File {datafile} does not exist.")
            return

        # Load data based on the file type (CSV or XLSX)
        try:
            if datafile.endswith('.csv'):
                data = pd.read_csv(datafile, encoding='utf-8')
            elif datafile.endswith('.xlsx'):
                data = pd.read_excel(datafile, encoding='utf-8')
            else:
                print("Error: Unsupported file type. Please provide a CSV or XLSX file.")
                return
        except Exception as e:
            print(f"Error while reading the file: {e}")
            return

        # Convert data to JSON format
        data_json = json.loads(data.to_json(orient='records'))

        # Create collection using the provided database and collection names
        collection = self.create_collection(database_name, collection_name)

        if collection is not None:
            if unique_field:
                for record in data_json:
                    if collection.count_documents({unique_field: record.get(unique_field)}) == 0:
                        collection.insert_one(record)
                        print(f"Inserted record with {unique_field}={record.get(unique_field)}.")
                    else:
                        print(f"Record with {unique_field}={record.get(unique_field)} already exists. Skipping insertion.")
            else:
                collection.insert_many(data_json)
                print(f"Inserted {len(data_json)} records successfully.")
        else:
            print("Failed to initialize the collection. Insert operation aborted.")

    @ensure_annotations
    def find(self, query: dict = {}, database_name: Optional[str] = None,collection_name: Optional[str] = None):
        collection = self.create_collection(database_name,collection_name)
        results = collection.find(query)
        return list(results)
    
    @ensure_annotations
    def update(self, query: dict = {}, new_values: dict = {}, database_name: Optional[str] = None,collection_name: Optional[str] = None):
        collection = self.create_collection(database_name,collection_name)
        collection.update_many(query, {"$set": new_values})
        
    @ensure_annotations
    def delete(self, query: dict = {}, database_name: Optional[str] = None,collection_name: Optional[str] = None):
        collection = self.create_collection(database_name,collection_name)
        collection.delete_many(query)
    
