
def assess_text_index(self):
    text_index_col_count = 0
    for db in self.databases:
        for col in db.collections:
            for index in col.indexes.values():
                if index['key'][0] == ('_fts', 'text'):
                    print("Collection",col.collection_name,"in Database",db.database_name,"is using text index. ",index)
                    text_index_col_count+=1
    if text_index_col_count!=0:
        text_index_msg = "Text indexes are not supported in Azure Cosmos DB API for MongoDB. "\
            "Azure Cosmos DB is a crucial part of the Azure ecosystem and is well integrated with other Azure services like Azure Search which offer advanced search features like wildcard search etc. "\
            "We recommend using Azure Search for full text search functionalities."
        print(text_index_msg)
    print("\n")