def assess_fixed_collection_size(self):
    col_count = 0
    for db in self.databases:
        for col in db.collections:
            # Check if collection is currently unsharded and exceeding fixed collection limit
            if col.data_size >=20000000000 and col.isSharded == False:
                print("Unsharded collection",col.collection_name,"in Database",db.database_name,"is exceeding the fixed collection size limit of 20 GB.")
                col_count+=1
            elif col.data_size >= 15000000000 and col.isSharded == False:
                print("Unsharded collection",col.collection_name,"in Database",db.database_name,"is currently > 15GB. It is approaching the fixed collection size limit of 20 GB.")
                col_count+=1
    if col_count!=0:
        fixed_collection_msg = "The maximum size of a fixed (unsharded) collection in Cosmos DB API for MongoDB is 20 GB. "\
            "You would either need to limit the data size of the unsharded collection to < 20GB or use sharded collection type."
        print(fixed_collection_msg)
    print("\n")