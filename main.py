from pymongo import MongoClient
import pandas as pd
from cryptography.fernet import Fernet


def pega_chave():
    key = ""
    with open("chave.key", "rb") as chave:
        key = chave.readline()

    fe = Fernet(key)

    return fe

def conecta_banco():
    client = MongoClient("mongodb://localhost:27017")

    db = client["trabalho_nosql"]

    collection = db["countries"]

    return collection

def insere_dados(conexao):

    df = pd.read_csv("encrypted.csv", sep=",")

    data = df.to_dict("records")

    conexao.insert_many(data)


def descriptografa(fe, cidade):
    return fe.decrypt(cidade).decode()


def lista_cidades_pais(fe, cidades):
    pais:str = input("Digite o pais que deseja ver: ")
    
    for item in cidades.find({"country":pais}):
        cidade = bytes(item['city'].replace("b'", "").replace("'", ""), encoding="utf-8")
        print(descriptografa(fe, cidade))

def pesquisa_por_nome(fe, cidades):
    pais:str = input("Digite o nome do pais: ")
    cidade:str = input("Digite a cidade que deseja consultar: ")
    for item in cidades.find({"country": pais}): 
        teste = bytes(item['city'].replace("b'", "").replace("'", ""), encoding="utf-8")
        if(descriptografa(fe, teste)) == cidade:
            print(descriptografa(fe, teste))
    

def mais_populoso(fe, cidades):
    teste = cidades.find().sort("population",-1).limit(1)
    for item in teste:
        print("Pais: " + item["country"] + 
        "\nCidade: " + descriptografa(fe, bytes(item['city'].replace("b'", "").replace("'", ""), encoding="utf-8")) +
        "\nPopulação: " + str(item["population"]))

def pesquisa_regiao(fe, cidades):
    try:
        region = int(input("Digite a regiao: "))
    except ValueError:
        print("Digite um número!")
        return 
    teste = cidades.find({"region": region})
    for item in teste:
        print("Pais: " + item["country"] + 
        " - Cidade: " + descriptografa(fe, bytes(item['city'].replace("b'", "").replace("'", ""), encoding="utf-8"))
        )

if __name__ == "__main__":
    cidades = conecta_banco()
    fe = pega_chave()
    #insere_dados(cidades)
    lista_cidades_pais(fe, cidades)
    pesquisa_por_nome(fe, cidades)
    mais_populoso(fe, cidades)
    pesquisa_regiao(fe, cidades)
