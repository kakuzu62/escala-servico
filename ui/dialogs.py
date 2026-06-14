from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QMessageBox, QTableWidget, QTableWidgetItem, QSpinBox
)
from PyQt5.QtCore import QDate
from models.usuario import Usuario
from models.funcao import Funcao
from models.pessoa import Pessoa
from models.escala import Escala
from models.afastamento import Afastamento
from services.escala_service import EscalaService
from services.relatorio_service import RelatorioService
from datetime import datetime

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.usuario = None
        self.init_ui()
    
    def init_ui(self):
        """Inicializa o diálogo de login"""
        self.setWindowTitle('Login - Sistema de Escala')
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()
        
        # Email
        layout.addWidget(QLabel('Email:'))
        self.input_email = QLineEdit()
        layout.addWidget(self.input_email)
        
        # Senha
        layout.addWidget(QLabel('Senha:'))
        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_senha)
        
        # Botões
        layout_botoes = QHBoxLayout()
        
        btn_login = QPushButton('Entrar')
        btn_login.clicked.connect(self.fazer_login)
        layout_botoes.addWidget(btn_login)
        
        btn_cancelar = QPushButton('Cancelar')
        btn_cancelar.clicked.connect(self.reject)
        layout_botoes.addWidget(btn_cancelar)
        
        layout.addLayout(layout_botoes)
        self.setLayout(layout)
    
    def fazer_login(self):
        """Realiza autenticação"""
        email = self.input_email.text()
        senha = self.input_senha.text()
        
        if not email or not senha:
            QMessageBox.warning(self, 'Aviso', 'Preencha email e senha!')
            return
        
        usuario = Usuario.autenticar(email, senha)
        if usuario:
            self.usuario = usuario
            self.accept()
        else:
            QMessageBox.critical(self, 'Erro', 'Email ou senha incorretos!')

class EscalaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.escala_service = EscalaService()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa o diálogo de escala"""
        self.setWindowTitle('Criar Escala')
        self.setGeometry(100, 100, 500, 300)
        
        layout = QVBoxLayout()
        
        # Função
        layout.addWidget(QLabel('Função:'))
        self.combo_funcao = QComboBox()
        funcoes = Funcao.obter_todas()
        for funcao in funcoes:
            self.combo_funcao.addItem(funcao['nome'], funcao['id'])
        layout.addWidget(self.combo_funcao)
        
        # Pessoa
        layout.addWidget(QLabel('Pessoa:'))
        self.combo_pessoa = QComboBox()
        layout.addWidget(self.combo_pessoa)
        
        # Data
        layout.addWidget(QLabel('Data:'))
        self.input_data = QDateEdit()
        self.input_data.setDate(QDate.currentDate())
        layout.addWidget(self.input_data)
        
        # Botões
        layout_botoes = QHBoxLayout()
        
        btn_criar = QPushButton('Criar')
        btn_criar.clicked.connect(self.criar_escala)
        layout_botoes.addWidget(btn_criar)
        
        btn_cancelar = QPushButton('Cancelar')
        btn_cancelar.clicked.connect(self.reject)
        layout_botoes.addWidget(btn_cancelar)
        
        layout.addLayout(layout_botoes)
        self.setLayout(layout)
        
        # Carrega pessoas da função selecionada
        self.combo_funcao.currentIndexChanged.connect(self.atualizar_pessoas)
        self.atualizar_pessoas()
    
    def atualizar_pessoas(self):
        """Atualiza combobox de pessoas"""
        funcao_id = self.combo_funcao.currentData()
        self.combo_pessoa.clear()
        
        pessoas = Pessoa.obter_por_funcao(funcao_id)
        for pessoa in pessoas:
            self.combo_pessoa.addItem(pessoa['nome'], pessoa['id'])
    
    def criar_escala(self):
        """Cria a escala"""
        funcao_id = self.combo_funcao.currentData()
        pessoa_id = self.combo_pessoa.currentData()
        data = self.input_data.date().toPyDate()
        
        sucesso, mensagem = self.escala_service.gerar_escala_manual(funcao_id, pessoa_id, data)
        
        if sucesso:
            QMessageBox.information(self, 'Sucesso', mensagem)
            self.accept()
        else:
            QMessageBox.critical(self, 'Erro', mensagem)

class FuncaoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa o diálogo de função"""
        self.setWindowTitle('Criar Função')
        self.setGeometry(100, 100, 400, 250)
        
        layout = QVBoxLayout()
        
        # Nome
        layout.addWidget(QLabel('Nome da Função:'))
        self.input_nome = QLineEdit()
        layout.addWidget(self.input_nome)
        
        # Descrição
        layout.addWidget(QLabel('Descrição:'))
        self.input_descricao = QLineEdit()
        layout.addWidget(self.input_descricao)
        
        # Botões
        layout_botoes = QHBoxLayout()
        
        btn_criar = QPushButton('Criar')
        btn_criar.clicked.connect(self.criar_funcao)
        layout_botoes.addWidget(btn_criar)
        
        btn_cancelar = QPushButton('Cancelar')
        btn_cancelar.clicked.connect(self.reject)
        layout_botoes.addWidget(btn_cancelar)
        
        layout.addLayout(layout_botoes)
        self.setLayout(layout)
    
    def criar_funcao(self):
        """Cria a função"""
        nome = self.input_nome.text()
        descricao = self.input_descricao.text()
        
        if not nome:
            QMessageBox.warning(self, 'Aviso', 'Preencha o nome da função!')
            return
        
        funcao = Funcao(nome=nome, descricao=descricao)
        if funcao.criar():
            QMessageBox.information(self, 'Sucesso', 'Função criada com sucesso!')
            self.accept()
        else:
            QMessageBox.critical(self, 'Erro', 'Erro ao criar função!')

class PessoaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa o diálogo de pessoa"""
        self.setWindowTitle('Adicionar Pessoa')
        self.setGeometry(100, 100, 450, 350)
        
        layout = QVBoxLayout()
        
        # Nome
        layout.addWidget(QLabel('Nome:'))
        self.input_nome = QLineEdit()
        layout.addWidget(self.input_nome)
        
        # Email
        layout.addWidget(QLabel('Email:'))
        self.input_email = QLineEdit()
        layout.addWidget(self.input_email)
        
        # Telefone
        layout.addWidget(QLabel('Telefone:'))
        self.input_telefone = QLineEdit()
        layout.addWidget(self.input_telefone)
        
        # Função
        layout.addWidget(QLabel('Função:'))
        self.combo_funcao = QComboBox()
        funcoes = Funcao.obter_todas()
        for funcao in funcoes:
            self.combo_funcao.addItem(funcao['nome'], funcao['id'])
        layout.addWidget(self.combo_funcao)
        
        # Botões
        layout_botoes = QHBoxLayout()
        
        btn_adicionar = QPushButton('Adicionar')
        btn_adicionar.clicked.connect(self.adicionar_pessoa)
        layout_botoes.addWidget(btn_adicionar)
        
        btn_cancelar = QPushButton('Cancelar')
        btn_cancelar.clicked.connect(self.reject)
        layout_botoes.addWidget(btn_cancelar)
        
        layout.addLayout(layout_botoes)
        self.setLayout(layout)
    
    def adicionar_pessoa(self):
        """Adiciona a pessoa"""
        nome = self.input_nome.text()
        email = self.input_email.text()
        telefone = self.input_telefone.text()
        funcao_id = self.combo_funcao.currentData()
        
        if not nome or not funcao_id:
            QMessageBox.warning(self, 'Aviso', 'Preencha nome e função!')
            return
        
        pessoa = Pessoa(nome=nome, email=email, telefone=telefone, funcao_id=funcao_id)
        if pessoa.criar():
            QMessageBox.information(self, 'Sucesso', 'Pessoa adicionada com sucesso!')
            self.accept()
        else:
            QMessageBox.critical(self, 'Erro', 'Erro ao adicionar pessoa!')

class AfastamentoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa o diálogo de afastamento"""
        self.setWindowTitle('Criar Afastamento')
        self.setGeometry(100, 100, 450, 350)
        
        layout = QVBoxLayout()
        
        # Pessoa
        layout.addWidget(QLabel('Pessoa:'))
        self.combo_pessoa = QComboBox()
        pessoas = Pessoa.obter_todas()
        for pessoa in pessoas:
            self.combo_pessoa.addItem(pessoa['nome'], pessoa['id'])
        layout.addWidget(self.combo_pessoa)
        
        # Tipo
        layout.addWidget(QLabel('Tipo:'))
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(['Férias', 'Licença Médica', 'Missão', 'Licença Remunerada', 'Outro'])
        layout.addWidget(self.combo_tipo)
        
        # Data Início
        layout.addWidget(QLabel('Data Início:'))
        self.input_data_inicio = QDateEdit()
        self.input_data_inicio.setDate(QDate.currentDate())
        layout.addWidget(self.input_data_inicio)
        
        # Data Fim
        layout.addWidget(QLabel('Data Fim:'))
        self.input_data_fim = QDateEdit()
        self.input_data_fim.setDate(QDate.currentDate())
        layout.addWidget(self.input_data_fim)
        
        # Botões
        layout_botoes = QHBoxLayout()
        
        btn_criar = QPushButton('Criar')
        btn_criar.clicked.connect(self.criar_afastamento)
        layout_botoes.addWidget(btn_criar)
        
        btn_cancelar = QPushButton('Cancelar')
        btn_cancelar.clicked.connect(self.reject)
        layout_botoes.addWidget(btn_cancelar)
        
        layout.addLayout(layout_botoes)
        self.setLayout(layout)
    
    def criar_afastamento(self):
        """Cria o afastamento"""
        pessoa_id = self.combo_pessoa.currentData()
        tipo = self.combo_tipo.currentText().lower().replace(' ', '_')
        data_inicio = self.input_data_inicio.date().toPyDate()
        data_fim = self.input_data_fim.date().toPyDate()
        
        if data_fim < data_inicio:
            QMessageBox.warning(self, 'Aviso', 'Data fim não pode ser anterior à data início!')
            return
        
        afastamento = Afastamento(
            pessoa_id=pessoa_id,
            tipo=tipo,
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        
        if afastamento.criar():
            QMessageBox.information(self, 'Sucesso', 'Afastamento criado com sucesso!')
            self.accept()
        else:
            QMessageBox.critical(self, 'Erro', 'Erro ao criar afastamento!')

class RelatorioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.relatorio_service = RelatorioService()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa o diálogo de relatório"""
        self.setWindowTitle('Gerar Relatório')
        self.setGeometry(100, 100, 600, 500)
        
        layout = QVBoxLayout()
        
        # Data
        layout.addWidget(QLabel('Data:'))
        self.input_data = QDateEdit()
        self.input_data.setDate(QDate.currentDate())
        layout.addWidget(self.input_data)
        
        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(3)
        self.tabela.setHorizontalHeaderLabels(['Função', 'Pessoa', 'Tipo Escala'])
        layout.addWidget(self.tabela)
        
        # Botões
        layout_botoes = QHBoxLayout()
        
        btn_gerar = QPushButton('Gerar')
        btn_gerar.clicked.connect(self.gerar_relatorio)
        layout_botoes.addWidget(btn_gerar)
        
        btn_exportar_pdf = QPushButton('Exportar PDF')
        btn_exportar_pdf.clicked.connect(self.exportar_pdf)
        layout_botoes.addWidget(btn_exportar_pdf)
        
        btn_fechar = QPushButton('Fechar')
        btn_fechar.clicked.connect(self.reject)
        layout_botoes.addWidget(btn_fechar)
        
        layout.addLayout(layout_botoes)
        self.setLayout(layout)
    
    def gerar_relatorio(self):
        """Gera e exibe o relatório"""
        data = self.input_data.date().toPyDate()
        relatorio = self.relatorio_service.gerar_relatorio_dia(data)
        
        self.tabela.setRowCount(0)
        
        for escala in relatorio['escalas']:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            
            self.tabela.setItem(row, 0, QTableWidgetItem(escala['funcao_nome']))
            self.tabela.setItem(row, 1, QTableWidgetItem(escala['pessoa_nome']))
            self.tabela.setItem(row, 2, QTableWidgetItem(escala['tipo_escala'].upper()))
    
    def exportar_pdf(self):
        """Exporta relatório para PDF"""
        data = self.input_data.date().toPyDate()
        nome_arquivo = f"Relatorio_Escala_{data.strftime('%d_%m_%Y')}.pdf"
        
        if self.relatorio_service.exportar_pdf(data, nome_arquivo):
            QMessageBox.information(self, 'Sucesso', f'PDF exportado: {nome_arquivo}')
        else:
            QMessageBox.critical(self, 'Erro', 'Erro ao exportar PDF!')
