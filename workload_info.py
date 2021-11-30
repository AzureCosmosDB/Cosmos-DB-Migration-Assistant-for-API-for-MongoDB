from database import Database
from collection import Collection
import csv
import pandas as pd
from rules.assess_unsupported_indexing_features import *
from rules.assess_no_of_collections_per_db import *
from rules.assess_partially_supported_indexing_features import *

class WorkloadInfo:
    def __init__(self, client):
        self.databases = []
        self.client = client

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
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["DB Name", "Collection Count", "Doc Count", "Avg Doc Size", "Data Size", "Index Count", "Index Size"])
                for db in self.databases:
                    writer.writerow([db.database_name, db.collection_count, db.document_count, db.average_doc_size, db.data_size, db.index_count, db.index_size])
        except BaseException as e:
            print('BaseException:', filename)

    def print_database_info(self):
        databases_df = pd.read_csv("workload_database_details.csv")
        databases_df.index+=1
        dfStyler = databases_df.style.set_properties(**{'text-align': 'left'})
        df = dfStyler.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
        display(df)

    
    def get_collection_info(self):
        for db in self.databases:
            col_cursor = self.client[db.database_name].list_collections()
            for col in col_cursor:
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
        assess_unsupported_indexing_features(self)

    def assess_partially_supported_features(self):
        assess_partially_supported_indexing_features(self)

    def assess_limits(self):
        assess_no_of_collections_per_db(self)