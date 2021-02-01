import os
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
from bson.json_util import dumps, loads

class Mongologger:
    def __init__(self):
        self.client = MongoClient(host=str(os.getenv('MONGO_HOST')),
                         port=int(os.getenv('MONGO_PORT')),
                         username=str(os.getenv('MONGO_USER')),
                         password=str(os.getenv('MONGO_PASSWORD'))
                        )
        self.db_handle = self.client[str(os.getenv('MONGO_DB'))]
        
    def logg(self, request):
        collection_handle = self.db_handle['loggs']
        try:
            collection_handle.insert({'IP': self.get_client_ip(request), 'Date': datetime.now(timezone.utc), 'User': str(request.user)})
        except:
            pass

    def drop(self):
        col = self.db_handle['loggs']
        col.drop()

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_querryset(self):
        collection_handle = self.db_handle['loggs']
        cursor = collection_handle.find()
        json_data = dumps(list(cursor), indent = 2) 
        print(json_data)
        return json_data