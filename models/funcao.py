from config.database import DatabaseConnection

class Funcao:
    def __init__(self, id=None, nome=None, descricao=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.db = DatabaseConnection()
    
    def criar(self):
        """Cria uma nova função no banco de dados"""
        query = """
            INSERT INTO funcoes (nome, descricao, ativa)
            VALUES (%s, %s, TRUE)
        """
        params = (self.nome, self.descricao)
        resultado = self.db.execute_update(query, params)
        return resultado > 0
    
    def atualizar(self):
        """Atualiza dados da função"""
        query = """
            UPDATE funcoes
            SET nome = %s, descricao = %s
            WHERE id = %s
        """
        params = (self.nome, self.descricao, self.id)
        resultado = self.db.execute_update(query, params)
        return resultado > 0
    
    @staticmethod
    def obter_por_id(funcao_id):
        """Obtém função pelo ID"""
        db = DatabaseConnection()
        query = "SELECT * FROM funcoes WHERE id = %s"
        resultado = db.execute_query(query, (funcao_id,))
        return resultado[0] if resultado else None
    
    @staticmethod
    def obter_todas():
        """Obtém todas as funções ativas"""
        db = DatabaseConnection()
        query = "SELECT * FROM funcoes WHERE ativa = TRUE ORDER BY nome"
        return db.execute_query(query)
    
    def deletar(self):
        """Marca função como inativa"""
        query = "UPDATE funcoes SET ativa = FALSE WHERE id = %s"
        resultado = self.db.execute_update(query, (self.id,))
        return resultado > 0
