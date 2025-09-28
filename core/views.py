from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from .mongo_utils import get_collection, check_mongo_connection
from django.conf import settings

def home(request):
    return HttpResponse("Welcome to EduNexus! Visit /test-mongo/ to check MongoDB.")

def test_mongo(request):
    if check_mongo_connection():
        test_col = get_collection("test")
        test_doc = {"message": "Hello MongoDB"}
        test_col.insert_one(test_doc)
        doc = test_col.find_one({"message": "Hello MongoDB"}, {"_id": 0})
        return JsonResponse({"connected": True, "test_doc": doc})
    else:
        return JsonResponse({"connected": False})

def list_databases(request):
    try:
        dbs = settings.MONGO_CLIENT.list_database_names()
        return JsonResponse({"databases": dbs})
    except Exception as e:
        return JsonResponse({"error": str(e)})

