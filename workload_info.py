from database import Database
import csv
from tabulate import tabulate

class WorkloadInfo:
    def __init__(self, client):
        self.databases = []
        self.client = client

    def get_database_info(self):
        db_cursor = self.client.list_databases()
        for db in db_cursor:
            db_stats = self.client.get_database(db['name']).command('dbStats')
            db_new = Database()
            db_new.database_name = db['name']
            db_new.collection_count = db_stats['collections']
            db_new.document_count = db_stats['objects']
            db_new.average_doc_size = db_stats['avgObjSize']
            db_new.data_size = db_stats['dataSize']
            db_new.index_count = db_stats['indexes']
            db_new.index_size = db_stats['indexSize']
            self.databases.append(db_new)

    def save_database_info_to_csv(self):
        filename = 'database_workload_details.csv'
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Database Name", "Collection Count", "Document Count", "Average Doc Size", "Data Size", "Index Count", "Index Size"])
                for db in self.databases:
                    writer.writerow([db.database_name, db.collection_count, db.document_count, db.average_doc_size, db.data_size, db.index_count, db.index_size])
        except BaseException as e:
            print('BaseException:', filename)

