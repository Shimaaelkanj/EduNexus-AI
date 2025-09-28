from django.conf import settings

def get_collection(name):
    """Return a collection object by name."""
    return settings.MONGO_DB[name]

def check_mongo_connection():
    """Ping MongoDB server and return True if connected."""
    try:
        settings.MONGO_CLIENT.admin.command("ping")
        return True
    except Exception as e:
        print("MongoDB connection error:", e)
        return False
