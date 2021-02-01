import os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient

def mongologger(request):
    try:
        collection_handle = get_logger_handle('loggs')
        collection_handle.insert({'IP': get_client_ip(request), 'Date': datetime.now(timezone.utc), 'User': str(request.user)})
    except:
        pass
    
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