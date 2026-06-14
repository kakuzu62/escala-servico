from datetime import datetime
from config.database import DatabaseConnection
from models.escala import Escala
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

class RelatorioService:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def gerar_relatorio_dia(self, data):
        """Gera relatório de escala para um dia específico"""
        escalas = Escala.obter_por_data(data)
        
        relatorio = {
            'data': data.strftime('%d/%m/%Y'),
            'dia_semana': self._obter_dia_semana(data),
            'escalas': escalas,
            'resumo': self._gerar_resumo(escalas)
        }
        
        return relatorio
    
    def gerar_relatorio_periodo(self, data_inicio, data_fim):
        """Gera relatório de um período"""
        from datetime import timedelta
        
        escalas_periodo = []
        data_atual = data_inicio
        
        while data_atual <= data_fim:
            escalas = Escala.obter_por_data(data_atual)
            if escalas:
                escalas_periodo.append({
                    'data': data_atual,
                    'escalas': escalas
                })
            data_atual += timedelta(days=1)
        
        return escalas_periodo
    
    def exportar_pdf(self, data, nome_arquivo):
        """Exporta relatório para PDF"""
        relatorio = self.gerar_relatorio_dia(data)
        
        doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Título
        titulo = Paragraph(
            f"<b>Escala de Serviço - {relatorio['dia_semana']}, {relatorio['data']}</b>",
            styles['Title']
        )
        elements.append(titulo)
        elements.append(Spacer(1, 0.3*inch))
        
        # Tabela de escalas
        dados_tabela = [['Função', 'Pessoa', 'Tipo Escala']]
        
        for escala in relatorio['escalas']:
            dados_tabela.append([
                escala['funcao_nome'],
                escala['pessoa_nome'],
                escala['tipo_escala'].upper()
            ])
        
        tabela = Table(dados_tabela)
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(tabela)
        doc.build(elements)
        
        return True
    
    def exportar_excel(self, data, nome_arquivo):
        """Exporta relatório para Excel"""
        try:
            import pandas as pd
            
            relatorio = self.gerar_relatorio_dia(data)
            
            dados = []
            for escala in relatorio['escalas']:
                dados.append({
                    'Função': escala['funcao_nome'],
                    'Pessoa': escala['pessoa_nome'],
                    'Tipo Escala': escala['tipo_escala']
                })
            
            df = pd.DataFrame(dados)
            df.to_excel(nome_arquivo, sheet_name='Escalas', index=False)
            
            return True
        except Exception as e:
            print(f"Erro ao exportar Excel: {e}")
            return False
    
    def _gerar_resumo(self, escalas):
        """Gera resumo da escala"""
        resumo = {}
        
        for escala in escalas:
            funcao = escala['funcao_nome']
            if funcao not in resumo:
                resumo[funcao] = []
            resumo[funcao].append(escala['pessoa_nome'])
        
        return resumo
    
    def _obter_dia_semana(self, data):
        """Obtém nome do dia da semana"""
        dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        return dias[data.weekday()]
