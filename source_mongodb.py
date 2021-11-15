from environment_info import EnvironmentInfo
from workload_info import WorkloadInfo
from pymongo import MongoClient
import pymongo

class SourceMongoDB:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.client = MongoClient(endpoint)
        self.environment_info = EnvironmentInfo(self.client)
        self.workload_info = WorkloadInfo(self.client)


    def get_environment_info(self):
        self.environment_info.get_mongodb_version_and_license()
        self.environment_info.get_shard_details()

    def print_environment_info(self):
        print("MongoDB version: ", self.environment_info.mongodb_version)
        print("License Type: ", self.environment_info.license_type)
        if self.environment_info.isShardedEndpoint == True:
            print("Is Sharded endpoint: Yes")
            self.environment_info.print_shard_list()
        elif self.environment_info.isShardedEndpoint == False:
            print("Is Sharded endpoint: No")

    def get_workload_info(self):
        self.workload_info.get_database_info()
        self.workload_info.get_collection_info()

    def save_workload_info_to_csv(self):
        self.workload_info.save_database_info_to_csv()
        self.workload_info.save_collection_info_to_csv(self.environment_info.isShardedEndpoint)

    def print_workload_info(self):
        print("Workload database details: ")
        self.workload_info.print_database_info()
        print("Workload collection details: ")
        self.workload_info.print_collection_info()
