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

    def print_environment_info(self):
        print("MongoDB version: ", self.environment_info.mongodb_version)
        print("License Type: ", self.environment_info.license_type)

    def get_workload_info(self):
        self.workload_info.get_database_info()


