def assess_unique_index(self):
    unique_index_count = 0
    for db in self.databases:
        for col in db.collections:
            for index in col.indexes.values():
                # check if it is a unique index
                if 'unique' in index.keys():
                    print("Collection",col.collection_name,"in Database",db.database_name,"is using unique index. ",index)
                    unique_index_count+=1

    if unique_index_count!=0:
        unique_index_msg = "Unique indexes can only be created on empty collections currently in Azure Cosmos DB API for MongoDB. "\
            "Please make sure you migrate the data to Cosmos DB after creating the index. "\
            "We are currently working on a fix to allow creating unique indexes on non-empty collections. This functionality will be available soon."
        print(unique_index_msg)
    print("\n")