import pymongo
import pandas as pd
import io

class EnvironmentInfo:
    def __init__(self, client):
        self.mongodb_version = ""
        self.license_type = ""
        self.client = client
        self.isShardedEndpoint = False
        self.shardList = []

    def get_mongodb_version_and_license(self):
        self.mongodb_version = self.client.server_info()['version']
    
        if (self.client.server_info()['modules'] == []):
            self.license_type = "Community"
        elif ("enterprise" in  self.client.server_info()['modules']):
            self.license_type = "Enterprise"

    def get_shard_details(self):
        try:
            list_shards_output = self.client.admin.command({'listShards': 1})
            self.isShardedEndpoint = True
            self.shardList = list_shards_output['shards']
        except pymongo.errors.OperationFailure:
            pass

    def print_shard_list(self):
        print("Shard details: ")
        pd.set_option('display.max_colwidth', None)
        df = pd.DataFrame(self.shardList)
        df.index+=1
        display(df)
