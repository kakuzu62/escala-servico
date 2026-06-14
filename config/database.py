import mysql.connector
from mysql.connector import Error
import configparser
import os

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.connection = None
        self.load_config()
    
    def load_config(self):
        """Carrega configurações do arquivo config.ini"""
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        config.read(config_path)
        
        self.host = config.get('DATABASE', 'host')
        self.port = config.getint('DATABASE', 'port')
        self.user = config.get('DATABASE', 'user')
        self.password = config.get('DATABASE', 'password')
        self.database = config.get('DATABASE', 'database')
    
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            return self.connection
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None
    
    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def get_cursor(self):
        """Retorna um cursor para executar queries"""
        if self.connect():
            return self.connection.cursor(dictionary=True)
        return None
    
    def execute_query(self, query, params=None):
        """Executa uma query SELECT"""
        cursor = self.get_cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao executar query: {e}")
            return None
        finally:
            cursor.close()
    
    def execute_update(self, query, params=None):
        """Executa uma query INSERT, UPDATE ou DELETE"""
        cursor = self.get_cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.rowcount
        except Error as e:
            self.connection.rollback()
            print(f"Erro ao executar update: {e}")
            return 0
        finally:
            cursor.close()
