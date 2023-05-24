from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Precisa tratar erros acho
class MovieDatabase:
    def __init__(self):
        # Autenticação com o URI de acesso ao banco
        uri = open('uri.env', 'r').read()
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Atribui o acesso ao banco de filmes
        self.db = self.client['sample_mflix']['movies']
    
    # Criação de um dado novo no banco (filme)
    # * packed_data: dados empacotados para inserção
    def create(self, packed_data):
        # Dict para a inserção de um filme novo
        new_data = {}

        # Cada dado do packed_data é inserido no dict new_data
        for key, data in packed_data:
            # Verifica se a chave é válida para inserção
            if not self.db.is_valid_key(key):
                return False
            new_data[key] = data
        
        # Insere o dict na base de dados
        result = self.db.insert_one(new_data)

        # ID de inserção para verificar o funcionamento da operação
        if result.inserted_id:
            return True
        return False

    # Busca por um dado no banco
    # * key: nome do atributo
    # * data: dado do atributo
    def query(self, key, data):
        # Dict com os dados para a busca
        query = {key: data}

        # Retorna lista de elementos encontrados
        return list(self.db.find(query))

    # Atualiza um dado no banco
    # * movie_name: nome do filme
    # * new_data: lista de dois elementos com dados novos
    def update(self, movie_name, new_data):
        # Busca o filme pelo nome
        movie = self.query("title", movie_name)
        if not movie: return False

        # Dict para a execução da atualização
        update = {'$set': {new_data[0] : new_data[1]}}

        # Atualiza os dados do filme no banco    
        result = self.db.update_one(movie[0], update)

        # Retorna número de elementos modificados
        return result.modified_count

    # Remove um filme do banco
    # * movie_name: nome do filme
    def remove(self, movie_name):
        # Busca o filme pelo nome
        movie = self.query("title", movie_name)
        if not movie: return False

        # Remove o filme do banco
        result = self.db.delete_one(movie[0])

        # Retorna o número de elementos modificados
        return result.deleted_count