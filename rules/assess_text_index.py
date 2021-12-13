
def assess_text_index(self):
    for db in self.databases:
        for col in db.collections:
            for index in col.indexes.values():
                if index['key'][0] == ('_fts', 'text'):
                    self.assessment_result_unsupported.append(tuple(["Text index",db.database_name,col.collection_name,index]))
