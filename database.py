from collection import Collection

class Database:
    def __init__(self):
        self.database_name = ""
        self.collection_count = 0
        self.document_count = 0
        self.average_doc_size = 0
        self.data_size = 0
        self.index_count = 0
        self.index_size = 0
        self.collections = []