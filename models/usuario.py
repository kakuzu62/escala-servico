import hashlib
from config.database import DatabaseConnection

class Usuario:
    def __init__(self, id=None, nome=None, email=None, senha=None, perfil='visualizador'):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.perfil = perfil
        self.db = DatabaseConnection()
    
    @staticmethod
    def hash_senha(senha):
        """Cria hash SHA-256 da senha"""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def criar(self):
        """Cria um novo usuário no banco de dados"""
        query = """
            INSERT INTO usuarios (nome, email, senha, perfil, ativo)
            VALUES (%s, %s, %s, %s, TRUE)
        """
        senha_hash = self.hash_senha(self.senha)
        params = (self.nome, self.email, senha_hash, self.perfil)
        resultado = self.db.execute_update(query, params)
        return resultado > 0
    
    def atualizar(self):
        """Atualiza dados do usuário"""
        query = """
            UPDATE usuarios
            SET nome = %s, perfil = %s
            WHERE id = %s
        """
        params = (self.nome, self.perfil, self.id)
        resultado = self.db.execute_update(query, params)
        return resultado > 0
    
    @staticmethod
    def autenticar(email, senha):
        """Autentica um usuário"""
        db = DatabaseConnection()
        query = "SELECT * FROM usuarios WHERE email = %s AND ativo = TRUE"
        resultado = db.execute_query(query, (email,))
        
        if resultado and len(resultado) > 0:
            usuario = resultado[0]
            senha_hash = Usuario.hash_senha(senha)
            if usuario['senha'] == senha_hash:
                return usuario
        return None
    
    @staticmethod
    def obter_por_id(usuario_id):
        """Obtém usuário pelo ID"""
        db = DatabaseConnection()
        query = "SELECT * FROM usuarios WHERE id = %s"
        resultado = db.execute_query(query, (usuario_id,))
        return resultado[0] if resultado else None
    
    @staticmethod
    def obter_todos():
        """Obtém todos os usuários"""
        db = DatabaseConnection()
        query = "SELECT * FROM usuarios ORDER BY nome"
        return db.execute_query(query)
    
    def deletar(self):
        """Marca usuário como inativo"""
        query = "UPDATE usuarios SET ativo = FALSE WHERE id = %s"
        resultado = self.db.execute_update(query, (self.id,))
        return resultado > 0
