def assess_unique_index(self):
    for db in self.databases:
        for col in db.collections:
            for index in col.indexes.values():
                # check if it is a unique index
                if 'unique' in index.keys():
                    self.assessment_result_partially_supported.append(tuple(["Unique index",db.database_name,col.collection_name,index]))