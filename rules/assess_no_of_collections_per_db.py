def assess_no_of_collections_per_db(self):
    db_count = 0
    for db in self.databases:
        if len(db.collections) > 25:
            db_count+=1
            print("Database",db.database_name,"has more than 25 collections.")
    print("\n")
    if db_count!=0:
        db_25_collections_msg = "We recommend a maximum of 25 collections per database if you are planning to use Shared database throughput. "\
            "This allows for better throughput sharing across collections. "\
            "If you are planning to use dedicated throughput however, you can have up to 500 collections per database."
        print(db_25_collections_msg)
    print("\n\n")