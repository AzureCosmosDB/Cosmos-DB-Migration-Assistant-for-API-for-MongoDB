def assess_compound_index_nested_field(self):
    for db in self.databases:
        for col in db.collections:
            for index in col.indexes.values():
                # check if it is a compound index
                if len(index['key']) > 1 and index['key'][0] != ('_fts', 'text'):
                    # look for nested field in the index
                    for i, index_condition in enumerate(index['key']):
                        index_field = index_condition[0]
                        if "." in index_field:
                            self.assessment_result_partially_supported.append(tuple(["Compound index with nested field",db.database_name,col.collection_name,index]))
                            break
