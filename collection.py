class Collection:
    def __init__(self):
        self.collection_name = ""
        self.isSharded = False
        self.document_count = 0
        self.average_doc_size = 0
        self.data_size = 0
        self.index_count = 0
        self.index_size = 0
        self.indexes = {}
