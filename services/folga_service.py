from datetime import datetime, timedelta
from config.database import DatabaseConnection
from models.afastamento import Afastamento

class FolgaService:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def incrementar_folgas_diarias(self):
        """Incrementa folgas de todas as pessoas em 1 unidade por dia"""
        query = """
            UPDATE folgas
            SET quantidade_folgas = quantidade_folgas + 1
            WHERE pessoa_id IN (
                SELECT p.id FROM pessoas p WHERE p.ativa = TRUE
            )
        """
        resultado = self.db.execute_update(query)
        return resultado > 0
    
    def obter_folgas_pessoa(self, pessoa_id):
        """Obtém quantidade de folgas de uma pessoa"""
        query = "SELECT quantidade_folgas FROM folgas WHERE pessoa_id = %s"
        resultado = self.db.execute_query(query, (pessoa_id,))
        return resultado[0]['quantidade_folgas'] if resultado else 0
    
    def reduzir_folgas_pessoa(self, pessoa_id, quantidade=1):
        """Reduz folgas de uma pessoa quando ela tira serviço"""
        query = """
            UPDATE folgas
            SET quantidade_folgas = GREATEST(0, quantidade_folgas - %s)
            WHERE pessoa_id = %s
        """
        resultado = self.db.execute_update(query, (quantidade, pessoa_id))
        return resultado > 0
    
    def obter_pessoa_com_mais_folgas(self, funcao_id, data_servico):
        """Obtém a pessoa com mais folgas de uma função (não afastada)"""
        query = """
            SELECT p.id, p.nome, f.quantidade_folgas
            FROM pessoas p
            JOIN folgas f ON p.id = f.pessoa_id
            WHERE p.funcao_id = %s AND p.ativa = TRUE
            AND p.id NOT IN (
                SELECT a.pessoa_id FROM afastamentos a
                WHERE a.ativo = TRUE
                AND a.data_inicio <= %s AND a.data_fim >= %s
            )
            ORDER BY f.quantidade_folgas DESC, p.nome ASC
            LIMIT 1
        """
        resultado = self.db.execute_query(query, (funcao_id, data_servico, data_servico))
        return resultado[0] if resultado else None
    
    def obter_pessoas_com_folgas_ordenadas(self, funcao_id, data_servico=None):
        """Obtém todas as pessoas de uma função ordenadas por folgas (desc)"""
        query = """
            SELECT p.id, p.nome, f.quantidade_folgas
            FROM pessoas p
            JOIN folgas f ON p.id = f.pessoa_id
            WHERE p.funcao_id = %s AND p.ativa = TRUE
        """
        
        if data_servico:
            query += """
            AND p.id NOT IN (
                SELECT a.pessoa_id FROM afastamentos a
                WHERE a.ativo = TRUE
                AND a.data_inicio <= %s AND a.data_fim >= %s
            )
            """
            params = (funcao_id, data_servico, data_servico)
        else:
            params = (funcao_id,)
        
        query += " ORDER BY f.quantidade_folgas DESC, p.nome ASC"
        return self.db.execute_query(query, params)
    
    def resetar_folgas_pessoa(self, pessoa_id, quantidade=0):
        """Reseta folgas de uma pessoa para um valor específico"""
        query = """
            UPDATE folgas
            SET quantidade_folgas = %s
            WHERE pessoa_id = %s
        """
        resultado = self.db.execute_update(query, (quantidade, pessoa_id))
        return resultado > 0
