from pymongo import MongoClient, UpdateOne
import json, os, datetime, pytz


class DatabaseHandler:
    def __init__(self):
        # Load the connection data from the config
        with open("../database/mongodb/credentials.json", "r") as creds_file:
            creds = json.load(creds_file)
        username = creds['username']
        password = creds['password']
        # Create the connection string
        connection_string = f"mongodb+srv://{username}:{password}@main.etprg3f.mongodb.net/"
        self.client = MongoClient(connection_string)

        # Add commonly used collections
        self.channels_collection = self.client['channels']['channels']
        self.guild_collection = self.client['clients']['clients']

    def get_active_channels( self ) -> list:
        return [ channel['_id'] for channel in self.channels_collection.find() ]
    

    def get_channel_data( self, channel_id: str ):
        """This method gets the channel info like type, and identifer from the DB"""
        channel_data: dict = self.channels_collection.find_one({"_id": str(channel_id)})
        return channel_data

    def get_active_guilds( self ) -> list:
        return [ guild['_id'] for guild in self.guild_collection.find() ]
    

    def get_guild_data( self, guild_id: str ):
        """This method gets the guild info like plan, and identifer from the DB"""
        guild_data: dict = self.guild_collection.find_one({"_id": str(guild_id)})
        return guild_data