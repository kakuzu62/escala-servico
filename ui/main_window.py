import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QMessageBox, QMenuBar, QMenu
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon

from models.usuario import Usuario
from ui.dialogs import (
    LoginDialog, EscalaDialog, FuncaoDialog, PessoaDialog,
    AfastamentoDialog, RelatorioDialog
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.usuario_logado = None
        self.init_ui()
    
    def init_ui(self):
        """Inicializa a interface principal"""
        self.setWindowTitle('Sistema de Escala de Serviço')
        self.setGeometry(100, 100, 1200, 700)
        
        # Menu
        self.criar_menu()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Label de boas-vindas
        self.label_info = QLabel('Bem-vindo ao Sistema de Escala de Serviço')
        self.label_info.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(self.label_info)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Aba Escalas
        layout_escalas = QVBoxLayout()
        btn_nova_escala = QPushButton('Criar Nova Escala')
        btn_nova_escala.clicked.connect(self.abrir_escala)
        layout_escalas.addWidget(btn_nova_escala)
        
        widget_escalas = QWidget()
        widget_escalas.setLayout(layout_escalas)
        self.tabs.addTab(widget_escalas, 'Escalas')
        
        # Aba Funções
        layout_funcoes = QVBoxLayout()
        btn_nova_funcao = QPushButton('Criar Nova Função')
        btn_nova_funcao.clicked.connect(self.abrir_funcao)
        layout_funcoes.addWidget(btn_nova_funcao)
        
        widget_funcoes = QWidget()
        widget_funcoes.setLayout(layout_funcoes)
        self.tabs.addTab(widget_funcoes, 'Funções')
        
        # Aba Pessoas
        layout_pessoas = QVBoxLayout()
        btn_nova_pessoa = QPushButton('Adicionar Pessoa')
        btn_nova_pessoa.clicked.connect(self.abrir_pessoa)
        layout_pessoas.addWidget(btn_nova_pessoa)
        
        widget_pessoas = QWidget()
        widget_pessoas.setLayout(layout_pessoas)
        self.tabs.addTab(widget_pessoas, 'Pessoas')
        
        # Aba Relatórios
        layout_relatorios = QVBoxLayout()
        btn_gerar_relatorio = QPushButton('Gerar Relatório')
        btn_gerar_relatorio.clicked.connect(self.abrir_relatorio)
        layout_relatorios.addWidget(btn_gerar_relatorio)
        
        widget_relatorios = QWidget()
        widget_relatorios.setLayout(layout_relatorios)
        self.tabs.addTab(widget_relatorios, 'Relatórios')
        
        layout.addWidget(self.tabs)
        
        central_widget.setLayout(layout)
        
        # Mostrar login
        self.mostrar_login()
    
    def criar_menu(self):
        """Cria barra de menu"""
        menubar = self.menuBar()
        
        # Menu Arquivo
        menu_arquivo = menubar.addMenu('Arquivo')
        sair = menu_arquivo.addAction('Sair')
        sair.triggered.connect(self.close)
        
        # Menu Editar
        menu_editar = menubar.addMenu('Editar')
        
        # Menu Ajuda
        menu_ajuda = menubar.addMenu('Ajuda')
        sobre = menu_ajuda.addAction('Sobre')
        sobre.triggered.connect(self.mostrar_sobre)
    
    def mostrar_login(self):
        """Mostra diálogo de login"""
        dialog = LoginDialog(self)
        if dialog.exec_():
            self.usuario_logado = dialog.usuario
            self.label_info.setText(f'Bem-vindo, {self.usuario_logado["nome"]} ({self.usuario_logado["perfil"]})')
            self.atualizar_permissoes()
    
    def atualizar_permissoes(self):
        """Atualiza permissões baseadas no perfil do usuário"""
        perfil = self.usuario_logado['perfil']
        
        # Desabilita abas baseado no perfil
        if perfil == 'visualizador':
            # Apenas leitura
            pass
        elif perfil == 'criador_escala':
            # Pode criar escalas
            pass
        elif perfil == 'administrador':
            # Acesso total
            pass
    
    def abrir_escala(self):
        """Abre diálogo de escala"""
        dialog = EscalaDialog(self)
        dialog.exec_()
    
    def abrir_funcao(self):
        """Abre diálogo de função"""
        dialog = FuncaoDialog(self)
        dialog.exec_()
    
    def abrir_pessoa(self):
        """Abre diálogo de pessoa"""
        dialog = PessoaDialog(self)
        dialog.exec_()
    
    def abrir_relatorio(self):
        """Abre diálogo de relatório"""
        dialog = RelatorioDialog(self)
        dialog.exec_()
    
    def mostrar_sobre(self):
        """Mostra diálogo sobre"""
        QMessageBox.about(
            self,
            'Sobre',
            'Sistema de Escala de Serviço v1.0\n\nDesenvolvido por: kakuzu62'
        )
