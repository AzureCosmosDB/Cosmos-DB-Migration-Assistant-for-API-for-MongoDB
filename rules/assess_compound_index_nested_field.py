def assess_compound_index_nested_field(self):
    compound_index_nested_count = 0
    for db in self.databases:
        for col in db.collections:
            for index in col.indexes.values():
                # check if it is a compound index
                if len(index['key']) > 1 and index['key'][0] != ('_fts', 'text'):
                    # look for nested field in the index
                    for i, index_condition in enumerate(index['key']):
                        index_field = index_condition[0]
                        if "." in index_field:
                            print("Collection",col.collection_name,"in Database",db.database_name,"is using compound index with nested field.")
                            compound_index_nested_count+=1
                            break
                    
    if compound_index_nested_count!=0:
        compound_index_nested_msg = "Compound indexes with nested fields are not fully supported in Azure Cosmos DB API for MongoDB. "\
            "If you are using compound index where the nested fields are docs (not arrays), you may raise a support ticket to enable the functionality."
        print(compound_index_nested_msg)
    print("\n")