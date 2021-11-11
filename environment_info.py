
class EnvironmentInfo:
    def __init__(self, client):
        self.mongodb_version = ""
        self.replica_set_count = 0
        self.license_type = ""
        self.client = client

    def get_mongodb_version_and_license(self):
        self.mongodb_version = self.client.server_info()['version']
    
        if (self.client.server_info()['modules'] == []):
            self.license_type = "Community"
        elif ("enterprise" in  self.client.server_info()['modules']):
            self.license_type = "Enterprise"


    
