import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from config.database import DatabaseConnection

def main():
    # Testa conexão com banco de dados
    db = DatabaseConnection()
    if not db.connect():
        print("Erro: Não foi possível conectar ao banco de dados.")
        print("Verifique as configurações em config/config.ini")
        sys.exit(1)
    
    # Inicia aplicação
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
