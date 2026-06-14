from config.database import DatabaseConnection

class Afastamento:
    def __init__(self, id=None, pessoa_id=None, tipo=None, data_inicio=None, data_fim=None, observacoes=None):
        self.id = id
        self.pessoa_id = pessoa_id
        self.tipo = tipo
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.observacoes = observacoes
        self.db = DatabaseConnection()
    
    def criar(self):
        """Cria um novo afastamento no banco de dados"""
        query = """
            INSERT INTO afastamentos (pessoa_id, tipo, data_inicio, data_fim, observacoes, ativo)
            VALUES (%s, %s, %s, %s, %s, TRUE)
        """
        params = (self.pessoa_id, self.tipo, self.data_inicio, self.data_fim, self.observacoes)
        resultado = self.db.execute_update(query, params)
        return resultado > 0
    
    def atualizar(self):
        """Atualiza dados do afastamento"""
        query = """
            UPDATE afastamentos
            SET tipo = %s, data_inicio = %s, data_fim = %s, observacoes = %s
            WHERE id = %s
        """
        params = (self.tipo, self.data_inicio, self.data_fim, self.observacoes, self.id)
        resultado = self.db.execute_update(query, params)
        return resultado > 0
    
    def finalizar(self):
        """Marca afastamento como finalizado"""
        query = "UPDATE afastamentos SET ativo = FALSE WHERE id = %s"
        resultado = self.db.execute_update(query, (self.id,))
        return resultado > 0
    
    @staticmethod
    def obter_por_pessoa(pessoa_id):
        """Obtém todos os afastamentos de uma pessoa"""
        db = DatabaseConnection()
        query = "SELECT * FROM afastamentos WHERE pessoa_id = %s ORDER BY data_inicio DESC"
        return db.execute_query(query, (pessoa_id,))
    
    @staticmethod
    def obter_afastamentos_ativos():
        """Obtém todos os afastamentos ativos"""
        db = DatabaseConnection()
        query = "SELECT * FROM afastamentos WHERE ativo = TRUE ORDER BY data_inicio"
        return db.execute_query(query)
    
    @staticmethod
    def pessoa_esta_afastada(pessoa_id, data):
        """Verifica se uma pessoa está afastada em uma data específica"""
        db = DatabaseConnection()
        query = """
            SELECT COUNT(*) as total
            FROM afastamentos
            WHERE pessoa_id = %s AND ativo = TRUE
            AND data_inicio <= %s AND data_fim >= %s
        """
        resultado = db.execute_query(query, (pessoa_id, data, data))
        return resultado[0]['total'] > 0 if resultado else False
