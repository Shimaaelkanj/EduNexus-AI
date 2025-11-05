from django.shortcuts import render
from django.http import JsonResponse
from .mongo_utils import get_collection, check_mongo_connection, get_list_databases


def users_list(request):
    users_col = get_collection("users")
    users = list(users_col.find({}, {"_id": 0}))
    return JsonResponse(users, safe=False)


def test_mongo(request):
    status = check_mongo_connection()

    if status:
        # Try inserting and reading back
        test_col = get_collection("test")
        test_doc = {"message": "Hello MongoDB"}
        test_col.insert_one(test_doc)

        doc = test_col.find_one({"message": "Hello MongoDB"}, {"_id": 0})
        return JsonResponse({"connected": True, "test_doc": doc})
    else:
        return JsonResponse({"connected": False})

def list_databases(request):
    dbs = get_list_databases()
    if dbs:
        return JsonResponse({"databases": dbs})
    return JsonResponse({"databases": []})
