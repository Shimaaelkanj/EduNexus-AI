from django.conf import settings

def get_collection(name):
    return settings.MONGO_DB[name]

def check_mongo_connection():
    try:
        # Ping MongoDB
        settings.MONGO_CLIENT.admin.command('ping')
        return True
    except Exception as e:
        print("MongoDB connection error:", e)
        return False
