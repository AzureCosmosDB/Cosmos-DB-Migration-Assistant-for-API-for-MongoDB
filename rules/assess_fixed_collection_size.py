def assess_fixed_collection_size(self):
    for db in self.databases:
        for col in db.collections:
            # Check if collection is currently unsharded and exceeding fixed collection limit
            if col.data_size >=20000000000 and col.isSharded == False:
                self.assessment_result_limits.append(tuple(["Unsharded collection exceeds fixed collection size limit",db.database_name,col.collection_name,]))
            elif col.data_size >= 15000000000 and col.isSharded == False:
                self.assessment_result_limits.append(tuple(["Unsharded collection approaches fixed collection size limit",db.database_name,col.collection_name,]))
