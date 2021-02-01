import os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient

def get_db_handle(db_name, host, port, username, password):
    client = MongoClient(host=host,
                         port=int(port),
                         username=username,
                         password=password
                        )
    db_handle = client[db_name]
    return db_handle, client

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
def get_logger_handle(collection_name):
    client = MongoClient(host=str(os.getenv('MONGO_HOST')),
                         port=int(os.getenv('MONGO_PORT')),
                         username=str(os.getenv('MONGO_USER')),
                         password=str(os.getenv('MONGO_PASSWORD'))
                        )
    db_handle = client[str(os.getenv('MONGO_DB'))]
    return db_handle[collection_name]