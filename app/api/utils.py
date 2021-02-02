import os
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
from bson.json_util import dumps, loads

class Mongologger:
    def __init__(self):
        """
            Creacion de clase helper que usa pymongo
            Cliente: host, port, username, password y db definidos en variables de entorno
        """
        self.client = MongoClient(host=str(os.getenv('MONGO_HOST')),
                         port=int(os.getenv('MONGO_PORT')),
                         username=str(os.getenv('MONGO_USER')),
                         password=str(os.getenv('MONGO_PASSWORD'))
                        )
        self.db_handle = self.client[str(os.getenv('MONGO_DB'))]
        
    def log(self, request):
        """Sistema de log que almacena cada registro en coleccion logs, se almacena ip, fecha UTC y usuario que uso el API 

        Args:
            request ([type]): [description]
        """
        collection_handle = self.db_handle['logs']
        try:
            doc_body ={
                'ip': str(self.get_client_ip(request)),
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'user': str(request.user)
            }
            r = collection_handle.insert_one(doc_body)
        except:
            pass

    def drop(self):
        """Elimina la coleccion logs
        """
        col = self.db_handle['logs']
        col.drop()

    def get_client_ip(self, request):
        """Obtiene a direccion IP del usuario aun cuando este se encuentre detras de un reverse proxy cuando se usa nginx o gunicorn

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_querryset(self):
        """Retorna los registros almacenados en la coleccion logs en formato JSON

        Returns:
            [type]: [description]
        """
        collection_handle = self.db_handle['logs']
        cursor = collection_handle.find()
        json_dump = dumps(cursor)
        json_object = loads(json_dump)
        return json_object