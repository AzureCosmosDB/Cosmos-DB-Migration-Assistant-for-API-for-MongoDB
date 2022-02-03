from database import Database
from collection import Collection
import csv
import pandas as pd
from rules.assess_unsupported_indexing_features import *
from rules.assess_no_of_collections_per_db import *
from rules.assess_partially_supported_indexing_features import *
from rules.assess_fixed_collection_size import *
import math

class WorkloadInfo:
    def __init__(self, client):
        self.databases = []
        self.client = client
        self.assessment_result_unsupported = []
        self.assessment_result_partially_supported = []
        self.assessment_result_limits = []

    def get_database_info(self):
        db_cursor = self.client.list_databases()
        for db in db_cursor:
            if db['name'] not in ['admin', 'config', 'local', 'auto']:
                db_stats = self.client.get_database(db['name']).command('dbStats')
                db_new = Database()
                db_new.database_name = db['name']
                if 'raw' in db_stats:
                    for shard in db_stats['raw']:
                        db_new.collection_count+=db_stats['raw'][shard]['collections']
                else:
                    db_new.collection_count = db_stats['collections']
                db_new.document_count = db_stats['objects']
                db_new.average_doc_size = int(db_stats['avgObjSize'])
                db_new.data_size = int(db_stats['dataSize'])
                db_new.index_count = db_stats['indexes']
                db_new.index_size = int(db_stats['indexSize'])
                self.databases.append(db_new)

    def save_database_info_to_csv(self):
        filename = 'workload_database_details.csv'
        total_collection_count = total_doc_count = total_data_size = total_index_size = 0
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["DB Name", "Collection Count", "Doc Count", "Avg Doc Size", "Data Size", "Index Count", "Index Size"])
                for db in self.databases:
                    total_collection_count += db.collection_count
                    total_doc_count += db.document_count
                    total_data_size += db.data_size
                    total_index_size += db.index_size
                    writer.writerow([db.database_name, db.collection_count, db.document_count, db.average_doc_size, db.data_size, db.index_count, db.index_size])
                total_data_size = self.convert_size(total_data_size)
                total_index_size = self.convert_size(total_index_size)
                writer.writerow([])
                writer.writerow(["TOTAL: ", total_collection_count, total_doc_count, "", total_data_size, "", total_index_size])
        except BaseException as e:
            print('BaseException:', filename)



    def print_database_info(self):
        databases_df = pd.read_csv("workload_database_details.csv", keep_default_na=False)
        databases_df.index+=1
        dfStyler = databases_df.style.set_properties(**{'text-align': 'left'})
        dfStyler = dfStyler.set_properties(subset=databases_df.index[-1], **{'font-weight': 'bold'})
        df = dfStyler.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
        display(df)

    
    def get_collection_info(self):
        for db in self.databases:
            col_cursor = self.client[db.database_name].list_collections()
            for col in col_cursor:
                if col['type'] != "view":
                    collStats = self.client[db.database_name].command('collStats', col['name'])
                    col_new = Collection()
                    col_new.collection_name = col['name']
                    if 'sharded' in collStats:
                        col_new.isSharded = collStats['sharded']
                    col_new.document_count = collStats['count']
                    if col_new.document_count != 0:
                        col_new.average_doc_size = int(collStats['avgObjSize'])
                    col_new.data_size = int(collStats['size'])
                    col_new.index_count= collStats['nindexes']
                    col_new.index_size = int(collStats['totalIndexSize'])

                    index_info = self.client[db.database_name][col['name']].index_information()
                    col_new.indexes = index_info

                    db.collections.append(col_new)
                else:
                    pass


    def save_collection_info_to_csv(self, isShardedEndpoint):
        filename = 'workload_collection_details.csv'
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                if isShardedEndpoint == False:
                    writer.writerow(["DB Name", "Collection Name", "Doc Count", "Avg Doc Size", "Data Size", "Index Count", "Index Size", "Indexes"])
                    for db in self.databases:
                        for col in db.collections:
                            writer.writerow([db.database_name, col.collection_name, col.document_count, col.average_doc_size, col.data_size, col.index_count, col.index_size, col.indexes])
                elif isShardedEndpoint == True:
                    writer.writerow(["DB Name", "Collection Name", "isSharded", "Doc Count", "Avg Doc Size", "Data Size", "Index Count", "Index Size", "Indexes"])
                    for db in self.databases:
                        for col in db.collections:
                            writer.writerow([db.database_name, col.collection_name, col.isSharded, col.document_count, col.average_doc_size, col.data_size, col.index_count, col.index_size, col.indexes])
        except BaseException as e:
            print('BaseException:', filename)

    def print_collection_info(self):
        collections_df = pd.read_csv("workload_collection_details.csv")
        collections_df.index+=1
        dfStyler = collections_df.style.set_properties(**{'text-align': 'left'})
        df = dfStyler.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
        display(df)


    def assess_unsupported_features(self):
        print("Assessment for unsupported features begins...")
        assess_unsupported_indexing_features(self)
        if self.assessment_result_unsupported == []:
            print("Assessment for unsupported features completed. There were no results found for the checks we ran.")
        else:
            print("Assessment for unsupported features completed. Some results were found and will be printed once all the assessments complete.")

    def save_assessment_result_unsupported(self):
        filename = 'assessment_result.csv'
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Category", "Sub-category", "DB Name", "Collection Name", "Index", "Message"])
                for tuple in self.assessment_result_unsupported:
                    if tuple[0] =="Text index":
                        text_index_msg = "Text indexes are not supported in Azure Cosmos DB API for MongoDB. "\
                            "Azure Cosmos DB is a crucial part of the Azure ecosystem and is well integrated with other Azure services like Azure Search which offer advanced search features like wildcard search etc. "\
                            "We recommend using Azure Search for full text search functionalities."
                        writer.writerow(["Unsupported feature",tuple[0],tuple[1],tuple[2],tuple[3],text_index_msg])
                f.close()
        except BaseException as e:
            print('BaseException:', filename)


    def assess_partially_supported_features(self):
        print("Assessment for partially supported features begins...")
        assess_partially_supported_indexing_features(self)
        if self.assessment_result_partially_supported == []:
            print("Assessment for partially supported features completed. There were no results found for the checks we ran.")
        else:
            print("Assessment for partially supported features completed. Some results were found and will be printed once all the assessments complete.")


    def save_assessment_result_partially_supported(self):
        filename = 'assessment_result.csv'
        try:
            with open(filename, 'a', newline='') as f:
                writer = csv.writer(f)
                for tuple in self.assessment_result_partially_supported:
                    if tuple[0] =="Unique index":
                        unique_index_msg = "Unique indexes can only be created on empty collections currently in Azure Cosmos DB API for MongoDB. "\
                            "Please make sure you migrate the data to Cosmos DB after creating the index. "\
                            "We are currently working on a fix to allow creating unique indexes on non-empty collections. This functionality will be available soon."
                        writer.writerow(["Partially supported feature",tuple[0],tuple[1],tuple[2],tuple[3],unique_index_msg])
                    elif tuple[0] == "Compound index with nested field":
                        compound_index_nested_msg = "Compound indexes with nested fields are not fully supported in Azure Cosmos DB API for MongoDB. "\
                            "If you are using compound index where the nested fields are docs (not arrays), you may raise a support ticket to enable the functionality."
                        writer.writerow(["Partially supported feature",tuple[0],tuple[1],tuple[2],tuple[3],compound_index_nested_msg])
                    elif tuple[0] == "Unique index with nested field":
                        unique_index_nested_msg = "Unique indexes with nested fields are not fully supported in Azure Cosmos DB API for MongoDB. "\
                            "If you are using unique index where the nested fields are docs (not arrays), you may raise a support ticket to enable the functionality."
                        writer.writerow(["Partially supported feature",tuple[0],tuple[1],tuple[2],tuple[3],unique_index_nested_msg])
                    elif tuple[0] == "TTL index":
                        ttl_index_msg = "Currently TTL indexes can only be created on _ts field in Azure Cosmos DB API for MongoDB. "\
                            "The _ts field is specific to Azure Cosmos DB and is not accessible from MongoDB clients. It is a reserved (system) property that contains the time stamp of the document's last modification. "\
                            "We will soon be supporting the creation of a TTL index on any field with a date object."
                        writer.writerow(["Partially supported feature",tuple[0],tuple[1],tuple[2],tuple[3],ttl_index_msg])
                f.close()
        except BaseException as e:
            print('BaseException:', filename)

    def assess_limits(self):
        print("Assessment for limits begins...")
        assess_no_of_collections_per_db(self)
        assess_fixed_collection_size(self)
        if self.assessment_result_limits == []:
            print("Assessment for limits completed. There were no results found for the checks we ran.")
        else:
            print("Assessment for limits completed. Some results were found.")


    def save_assessment_result_limits(self):
        filename = 'assessment_result.csv'
        try:
            with open(filename, 'a', newline='') as f:
                writer = csv.writer(f)
                for tuple in self.assessment_result_limits:
                    if tuple[0] =="Unsharded collection exceeds fixed collection size limit":
                        exceeds_fixed_collection_msg = "The maximum size of a fixed (unsharded) collection in Cosmos DB API for MongoDB is 20 GB. "\
                            "This unsharded collection exceeds the limit. "\
                            "You would either need to limit the data size of the unsharded collection to < 20GB or use sharded collection type."
                        writer.writerow(["Limit warning",tuple[0],tuple[1],tuple[2],"",exceeds_fixed_collection_msg])
                    elif tuple[0] == "Unsharded collection approaches fixed collection size limit":
                        approaches_fixed_collection_msg = "The maximum size of a fixed (unsharded) collection in Cosmos DB API for MongoDB is 20 GB. "\
                            "This unsharded collection is currently >15Gb in size and approaches the limit. "\
                            "You would either need to limit the data size of the unsharded collection to < 20GB or use sharded collection type."
                        writer.writerow(["Limit warning",tuple[0],tuple[1],tuple[2],"",approaches_fixed_collection_msg])
                    elif tuple[0] == "Db has >25 collections":
                        db_25_collections_msg = "We recommend a maximum of 25 collections per database if you are planning to use Shared database throughput. "\
                            "This allows for better throughput sharing across collections. "\
                            "You may increase the default limit of 25 collections in a Shared throughput database by raising a support request. "\
                            "If you are planning to use dedicated throughput however, you can have up to 500 collections per database."
                        writer.writerow(["Limit warning",tuple[0],tuple[1],"","",db_25_collections_msg])
                f.close()
        except BaseException as e:
            print('BaseException:', filename)

    def print_assessment_results(self):
        print("\n")
        print("Assessment results: ")
        results_df = pd.read_csv("assessment_result.csv", keep_default_na=False)
        results_df.index+=1
        dfStyler = results_df.style.set_properties(**{'text-align': 'left'})
        df = dfStyler.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
        display(df)

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])