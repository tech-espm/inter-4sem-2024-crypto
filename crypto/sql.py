from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from datetime import datetime
from config import connection_string

engine = create_engine(connection_string)

def criarLeitura():
    with Session(engine) as sessao, sessao.begin():
        sessao.execute(text("INSERT INTO leitura (data) VALUES (curdate())"))

        resultado = sessao.execute(text("SELECT last_insert_id() idleitura"))
        return resultado.fetchone()[0]

def criarCurrency(nome, sigla):
    with Session(engine) as sessao, sessao.begin():
        obra = {
            'nome': nome,
            'sigla': sigla
        }

        sessao.execute(text("INSERT INTO currency (nome, sigla) VALUES (:nome, :sigla)"), obra)

        resultado = sessao.execute(text("SELECT last_insert_id() idcurrency"))
        return resultado.fetchone()[0]

def criarRanking(idleitura, idcurrency, valor):
    with Session(engine) as sessao, sessao.begin():
        ranking = {
            'idcurrency': idcurrency,
            'valor': valor,
            'idleitura': idleitura
        }
        sessao.execute(text("INSERT INTO ranking (idcurrency, valor, idleitura) VALUES (:idcurrency, :valor, :idleitura)"), ranking)

def obter_idcurrency(sigla):
    with engine.connect() as conexao:
        consulta = text("SELECT idcurrency FROM currency WHERE sigla = :sigla")
        
        resultado = conexao.execute(consulta, {'sigla': sigla})
        idcurrency = resultado.fetchone()

        if idcurrency:
            return idcurrency[0]  
        else:
            return None 
