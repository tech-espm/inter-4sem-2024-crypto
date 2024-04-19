CREATE DATABASE crypto DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;
USE crypto;

CREATE TABLE currency (
  idcurrency INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(40) NOT NULL,
  sigla VARCHAR(10) NOT NULL,
  UNIQUE KEY un_currency_sigla (sigla)
);

CREATE TABLE leitura (
  idleitura INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  data DATETIME NOT NULL,
  UNIQUE KEY un_leitura_data (data)
);

CREATE TABLE ranking (
  idranking INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  idcurrency INT NOT NULL,
  idleitura INT NOT NULL,
  valor DECIMAL(16,9) NOT NULL,
  UNIQUE KEY un_ranking_idleitura_idcurrency (idleitura, idcurrency),
  KEY ix_ranking_idcurrency (idcurrency),
  FOREIGN KEY fk_ranking_idcurrency (idcurrency) REFERENCES currency(idcurrency),
  FOREIGN KEY fk_ranking_idleitura (idleitura) REFERENCES leitura(idleitura)
);
