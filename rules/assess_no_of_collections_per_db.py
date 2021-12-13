def assess_no_of_collections_per_db(self):
    for db in self.databases:
        if len(db.collections) > 25:
            self.assessment_result_limits.append(tuple(["Db has >25 collections",db.database_name,]))
