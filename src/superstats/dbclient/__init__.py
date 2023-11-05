from pymongo import MongoClient, UpdateOne
import json, os, datetime, pytz


class DatabaseHandler:
    def __init__(self):
        # Load the connection data from the config
        # with open("../../database/mongodb/credentials.json", "r") as creds_file:
        #     creds = json.load(creds_file)
        username = "frkxb"
        password = "ri9jcokAJLgHndfp"
        # Create the connection string
        connection_string = f"mongodb+srv://{username}:{password}@main.etprg3f.mongodb.net/"
        self.client = MongoClient(connection_string)

        # Add commonly used collections
        self.external_tasks_database = self.client['tasks']

    def get_new_active_tasks( self ) -> list:
        tasks_collection: object = self.external_tasks_database['new_active_tasks']
        new_tasks = tasks_collection.find().sort("_id", 0).limit(2)

        for doc in new_tasks:
            tasks_collection.delete_one({"_id": doc["_id"]})
            
        return new_tasks
        