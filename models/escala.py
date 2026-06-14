from config.database import DatabaseConnection

class Escala:
    def __init__(self, id=None, funcao_id=None, pessoa_id=None, data_servico=None, tipo_escala=None, turno=None, criado_por=None):
        self.id = id
        self.funcao_id = funcao_id
        self.pessoa_id = pessoa_id
        self.data_servico = data_servico
        self.tipo_escala = tipo_escala
        self.turno = turno
        self.criado_por = criado_por
        self.db = DatabaseConnection()
    
    def criar(self):
        """Cria uma nova escala no banco de dados"""
        query = """
            INSERT INTO escalas (funcao_id, pessoa_id, data_servico, tipo_escala, turno, criado_por)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (self.funcao_id, self.pessoa_id, self.data_servico, self.tipo_escala, self.turno, self.criado_por)
        resultado = self.db.execute_update(query, params)
        return resultado > 0
    
    def deletar(self):
        """Deleta uma escala"""
        query = "DELETE FROM escalas WHERE id = %s"
        resultado = self.db.execute_update(query, (self.id,))
        return resultado > 0
    
    @staticmethod
    def obter_por_data(data_servico):
        """Obtém todas as escalas de uma data específica"""
        db = DatabaseConnection()
        query = """
            SELECT e.*, f.nome as funcao_nome, p.nome as pessoa_nome
            FROM escalas e
            JOIN funcoes f ON e.funcao_id = f.id
            JOIN pessoas p ON e.pessoa_id = p.id
            WHERE e.data_servico = %s
            ORDER BY f.nome, p.nome
        """
        return db.execute_query(query, (data_servico,))
    
    @staticmethod
    def obter_por_funcao_data(funcao_id, data_servico):
        """Obtém escalas de uma função em uma data específica"""
        db = DatabaseConnection()
        query = """
            SELECT e.*, p.nome as pessoa_nome
            FROM escalas e
            JOIN pessoas p ON e.pessoa_id = p.id
            WHERE e.funcao_id = %s AND e.data_servico = %s
            ORDER BY p.nome
        """
        return db.execute_query(query, (funcao_id, data_servico))
    
    @staticmethod
    def obter_todas():
        """Obtém todas as escalas"""
        db = DatabaseConnection()
        query = """
            SELECT e.*, f.nome as funcao_nome, p.nome as pessoa_nome
            FROM escalas e
            JOIN funcoes f ON e.funcao_id = f.id
            JOIN pessoas p ON e.pessoa_id = p.id
            ORDER BY e.data_servico DESC
        """
        return db.execute_query(query)
