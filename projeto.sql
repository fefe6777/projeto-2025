USE RH;


CREATE TABLE funcionarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL,
    cargo VARCHAR(60) NOT NULL,
    email VARCHAR(50) NOT NULL,
    senha VARCHAR(15) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    endereco VARCHAR(100) NOT NULL,
    salario VARCHAR(200) NOT NULL,
    data_cont DATE NOT NULL,
    foto1 VARCHAR(70) NOT NULL,
    foto2 VARCHAR(70) NOT NULL,
    foto3 VARCHAR(70) NOT NULL,
    foto4 VARCHAR(70) NOT NULL,
    foto5 VARCHAR(70) NOT NULL,
    data_criacao DATE NOT NULL DEFAULT (CURRENT_DATE),
    ultimo_login DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE registros(
    idr INT AUTO_INCREMENT PRIMARY KEY,
    id INT,
    hora DATETIME,
    imagem VARCHAR(70),
    latitude VARCHAR(25),
    longitude VARCHAR(25),
    ultimo_registro DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES funcionarios(id)  -- Referência à chave primária de funcionarios
);


CREATE TABLE usuarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL,
    cargo VARCHAR(60) NOT NULL,
    email VARCHAR(50) NOT NULL,
    senha VARCHAR(15) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    endereco VARCHAR(100) NOT NULL,

);


INSERT INTO usuarios (nome, cargo, email, senha, telefone, endereco) VALUES ('Denirso', 'Funcionario', 'denilso@gmail.com', 'Senha123', '16997284917', 'Rua Sebastio da Silva 362');
