def assess_unique_index_nested_field(self):
    unique_index_nested_count = 0
    for db in self.databases:
        for col in db.collections:
            for index in col.indexes.values():
                # check if it is a unique index
                if 'unique' in index.keys():
                    # look for nested field in the index - works for single or compound unique index
                    for i, index_condition in enumerate(index['key']):
                        index_field = index_condition[0]
                        if "." in index_field:
                            print("Collection",col.collection_name,"in Database",db.database_name,"is using unique index with nested field. ",index)
                            unique_index_nested_count+=1
                            break

    if unique_index_nested_count!=0:
        unique_index_nested_msg = "Unique indexes with nested fields are not fully supported in Azure Cosmos DB API for MongoDB. "\
            "If you are using unique index where the nested fields are docs (not arrays), you may raise a support ticket to enable the functionality."
        print(unique_index_nested_msg)
    print("\n")