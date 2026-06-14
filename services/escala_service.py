from datetime import datetime
from config.database import DatabaseConnection
from models.escala import Escala
from models.afastamento import Afastamento
from services.folga_service import FolgaService

class EscalaService:
    def __init__(self):
        self.db = DatabaseConnection()
        self.folga_service = FolgaService()
    
    def determinar_tipo_escala(self, data):
        """Determina se é escala preta (seg-sex) ou vermelha (fins de semana/feriados)"""
        # 0=seg, 1=ter, 2=qua, 3=qui, 4=sex, 5=sab, 6=dom
        dia_semana = data.weekday()
        
        if dia_semana >= 5:  # Sábado e domingo
            return 'vermelha'
        
        # Aqui você pode adicionar lógica para feriados
        # Por enquanto, consideramos apenas finais de semana como vermelha
        return 'preta'
    
    def gerar_escala_automatica(self, data_servico):
        """Gera escala automática para uma data baseada na contagem de folgas"""
        from models.funcao import Funcao
        
        funcoes = Funcao.obter_todas()
        escalas_geradas = []
        
        for funcao in funcoes:
            pessoa = self.folga_service.obter_pessoa_com_mais_folgas(funcao['id'], data_servico)
            
            if pessoa:
                tipo_escala = self.determinar_tipo_escala(data_servico)
                escala = Escala(
                    funcao_id=funcao['id'],
                    pessoa_id=pessoa['id'],
                    data_servico=data_servico,
                    tipo_escala=tipo_escala
                )
                
                if escala.criar():
                    self.folga_service.reduzir_folgas_pessoa(pessoa['id'], 1)
                    escalas_geradas.append({
                        'funcao': funcao['nome'],
                        'pessoa': pessoa['nome'],
                        'data': data_servico,
                        'tipo': tipo_escala
                    })
        
        return escalas_geradas
    
    def gerar_escala_manual(self, funcao_id, pessoa_id, data_servico):
        """Gera escala manual para uma pessoa/função em uma data"""
        # Verifica se pessoa está afastada
        if Afastamento.pessoa_esta_afastada(pessoa_id, data_servico):
            return False, "Pessoa está afastada nesta data"
        
        tipo_escala = self.determinar_tipo_escala(data_servico)
        escala = Escala(
            funcao_id=funcao_id,
            pessoa_id=pessoa_id,
            data_servico=data_servico,
            tipo_escala=tipo_escala
        )
        
        if escala.criar():
            self.folga_service.reduzir_folgas_pessoa(pessoa_id, 1)
            return True, "Escala criada com sucesso"
        else:
            return False, "Erro ao criar escala"
    
    def obter_escala_dia(self, data):
        """Obtém a escala de um dia inteiro"""
        return Escala.obter_por_data(data)
    
    def obter_escala_funcao_dia(self, funcao_id, data):
        """Obtém a escala de uma função em um dia"""
        return Escala.obter_por_funcao_data(funcao_id, data)
    
    def deletar_escala(self, escala_id):
        """Deleta uma escala e retorna folga para pessoa"""
        # Busca escala
        escalas = self.db.execute_query("SELECT * FROM escalas WHERE id = %s", (escala_id,))
        if escalas:
            escala = escalas[0]
            # Retorna folga para pessoa
            self.folga_service.reduzir_folgas_pessoa(escala['pessoa_id'], -1)  # Incrementa
            # Deleta escala
            escala_obj = Escala(id=escala_id)
            return escala_obj.deletar()
        return False
