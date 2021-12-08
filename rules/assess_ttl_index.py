def assess_ttl_index(self):
    ttl_index_count = 0
    for db in self.databases:
        for col in db.collections:
            for index in col.indexes.values():
                # check if it is a ttl index
                if 'expireAfterSeconds' in index.keys():
                    # check if the field is other than _ts
                    if index['key'][0][0] != "_ts":
                        print("Collection",col.collection_name,"in Database",db.database_name,"is using TTL index on a field. ",index)
                        ttl_index_count+=1
                    
    if ttl_index_count!=0:
        ttl_index_msg = "Currently TTL indexes can only be created on _ts field in Azure Cosmos DB API for MongoDB. "\
            "The _ts field is specific to Azure Cosmos DB and is not accessible from MongoDB clients. It is a reserved (system) property that contains the time stamp of the document's last modification. "\
            "We will soon be supporting TTL indexes on all fields."
        print(ttl_index_msg)
    print("\n")