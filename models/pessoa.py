from config.database import DatabaseConnection

class Pessoa:
    def __init__(self, id=None, nome=None, email=None, telefone=None, funcao_id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.funcao_id = funcao_id
        self.db = DatabaseConnection()
    
    def criar(self):
        """Cria uma nova pessoa no banco de dados"""
        query = """
            INSERT INTO pessoas (nome, email, telefone, funcao_id, ativa)
            VALUES (%s, %s, %s, %s, TRUE)
        """
        params = (self.nome, self.email, self.telefone, self.funcao_id)
        resultado = self.db.execute_update(query, params)
        
        if resultado > 0:
            # Cria registro de folgas para a pessoa
            query_folga = """
                INSERT INTO folgas (pessoa_id, quantidade_folgas)
                VALUES (LAST_INSERT_ID(), 0)
            """
            self.db.execute_update(query_folga)
        
        return resultado > 0
    
    def atualizar(self):
        """Atualiza dados da pessoa"""
        query = """
            UPDATE pessoas
            SET nome = %s, email = %s, telefone = %s, funcao_id = %s
            WHERE id = %s
        """
        params = (self.nome, self.email, self.telefone, self.funcao_id, self.id)
        resultado = self.db.execute_update(query, params)
        return resultado > 0
    
    @staticmethod
    def obter_por_id(pessoa_id):
        """Obtém pessoa pelo ID"""
        db = DatabaseConnection()
        query = "SELECT * FROM pessoas WHERE id = %s"
        resultado = db.execute_query(query, (pessoa_id,))
        return resultado[0] if resultado else None
    
    @staticmethod
    def obter_por_funcao(funcao_id):
        """Obtém todas as pessoas de uma função"""
        db = DatabaseConnection()
        query = "SELECT * FROM pessoas WHERE funcao_id = %s AND ativa = TRUE ORDER BY nome"
        return db.execute_query(query, (funcao_id,))
    
    @staticmethod
    def obter_todas():
        """Obtém todas as pessoas ativas"""
        db = DatabaseConnection()
        query = "SELECT * FROM pessoas WHERE ativa = TRUE ORDER BY nome"
        return db.execute_query(query)
    
    def deletar(self):
        """Marca pessoa como inativa"""
        query = "UPDATE pessoas SET ativa = FALSE WHERE id = %s"
        resultado = self.db.execute_update(query, (self.id,))
        return resultado > 0
