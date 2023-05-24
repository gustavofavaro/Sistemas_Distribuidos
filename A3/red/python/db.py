from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Tratar erros
class MovieDatabase:
    def __init__(self):
        uri = open('uri.env', 'r').read()
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['sample_mflix']['movies']
    
    def create(self, packed_data):
        # data[n][0] = campo / data[n][1] = valor
        new_data = {}
        for data in packed_data:
            if not self.db.is_valid_key(data[0]):
                return False
            new_data[data[0]] = data[1]
        
        result = self.db.insert_one(new_data)
        if result.inserted_id:
            return True
        return False

    def query(self, key, data):
        query = {key: data}
        return list(self.db.find(query))

    def update(self, movie_name, new_data):
        movie = self.query("title", movie_name)
        if not movie: return False
        update = {'$set': {new_data[0] : new_data[1]}}

        result = self.db.update_one(movie[0], update)
        return result.modified_count

    def remove(self, movie_name):
        movie = self.query("title", movie_name)
        result = self.db.delete_one(movie[0])
        return result.deleted_count