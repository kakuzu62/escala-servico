-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS escala_servico CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE escala_servico;

-- Tabela de Usuários (Administradores do Sistema)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    perfil ENUM('administrador', 'criador_escala', 'visualizador') DEFAULT 'visualizador',
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de Funções/Serviços
CREATE TABLE funcoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    ativa BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de Pessoas
CREATE TABLE pessoas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    funcao_id INT NOT NULL,
    ativa BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (funcao_id) REFERENCES funcoes(id)
);

-- Tabela de Afastamentos
CREATE TABLE afastamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT NOT NULL,
    tipo ENUM('ferias', 'licenca_medica', 'missao', 'licenca_remunerada', 'outro') NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    observacoes TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
);

-- Tabela de Folgas (Histórico)
CREATE TABLE folgas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT NOT NULL,
    quantidade_folgas INT DEFAULT 0,
    data_ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
);

-- Tabela de Escalas
CREATE TABLE escalas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    funcao_id INT NOT NULL,
    pessoa_id INT NOT NULL,
    data_servico DATE NOT NULL,
    tipo_escala ENUM('preta', 'vermelha') NOT NULL,
    turno VARCHAR(50),
    criado_por INT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (funcao_id) REFERENCES funcoes(id),
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id),
    FOREIGN KEY (criado_por) REFERENCES usuarios(id),
    UNIQUE KEY unique_escala (funcao_id, pessoa_id, data_servico)
);

-- Tabela de Histórico de Escalas
CREATE TABLE historico_escalas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT NOT NULL,
    funcao_id INT NOT NULL,
    data_servico DATE NOT NULL,
    tipo_escala ENUM('preta', 'vermelha') NOT NULL,
    status ENUM('confirmado', 'cancelado', 'substituido') DEFAULT 'confirmado',
    motivo TEXT,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id),
    FOREIGN KEY (funcao_id) REFERENCES funcoes(id)
);

-- Tabela de Relatórios Gerados
CREATE TABLE relatorios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_relatorio DATE NOT NULL,
    conteudo LONGTEXT NOT NULL,
    gerado_por INT,
    data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (gerado_por) REFERENCES usuarios(id)
);

-- Índices para melhor performance
CREATE INDEX idx_pessoa_funcao ON pessoas(funcao_id);
CREATE INDEX idx_escala_data ON escalas(data_servico);
CREATE INDEX idx_escala_funcao ON escalas(funcao_id);
CREATE INDEX idx_afastamento_pessoa ON afastamentos(pessoa_id);
CREATE INDEX idx_afastamento_datas ON afastamentos(data_inicio, data_fim);
CREATE INDEX idx_folgas_pessoa ON folgas(pessoa_id);
CREATE INDEX idx_historico_pessoa ON historico_escalas(pessoa_id);
CREATE INDEX idx_historico_data ON historico_escalas(data_servico);
