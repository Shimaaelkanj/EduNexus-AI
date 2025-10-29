from django.conf import settings

def get_collection(name):
    return settings.MONGO_DB[name]

def check_mongo_connection():
    try:
        settings.MONGO_CLIENT.admin.command("ping")
        return True
    except Exception as e:
        print("MongoDB connection error:", e)
        return False
def get_list_databases():
    dbs = settings.MONGO_CLIENT.list_database_names()
    return dbs