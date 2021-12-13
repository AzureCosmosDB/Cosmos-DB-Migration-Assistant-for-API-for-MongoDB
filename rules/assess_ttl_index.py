def assess_ttl_index(self):
    for db in self.databases:
        for col in db.collections:
            for index in col.indexes.values():
                # check if it is a ttl index
                if 'expireAfterSeconds' in index.keys():
                    # check if the field is other than _ts
                    if index['key'][0][0] != "_ts":
                        self.assessment_result_partially_supported.append(tuple(["TTL index",db.database_name,col.collection_name,index]))
                    