# Lado passivo/server

import re
from myserver import MyServer

def high_five(text_string):
    """ Metodo que retorna as 5 palavras que mais ocorrem dentro de um determinado texto. """
    try:
        contents = read_file(str(text_string, encoding='utf-8'));
        return ", ".join(high_words(word_count(contents), 5))
    except FileNotFoundError:
        return "Arquivo não encontrado."

def word_count(string):
    """ Metodo para contar as ocorrencias de cada palavra em um determinado texto """
    result = {}
    unique_words = set(re.split(r"\W+", string))
    for word in unique_words:
        result[word] = len(re.findall(r"^" + word + r"$|\W" + word + r"$|^" + word + r"\W|\W" + word + r"\W", string))
    del result[""]
    return result

def high_words(counted, amount=1):
    # ordena o dicionario por valor
    # pega os i primeiros em uma lista de tuplas
    # e retorna apenas uma lista com as chaves
    return dict(sorted(counted.items(), key=lambda item: item[1])[:amount]).keys()

def read_file(filename):
    with open(filename, "r") as f:
        return f.read()

def main():
    # passar hostname e porta aqui para conectar a alguem diferente
    with MyServer() as server:
        # configura a funcao a ser executada pelo servidor para processar as requisicoes
        server.set_external_method(high_five)
        # inicia o servidor
        server.run()

main()

"""
usado apenas para debug

def all_counts(text_string):
    try:
        contents = read_file(str(text_string, encoding='utf-8'));
        result = ""
        for key, value in word_count(contents).items():
            result += f"[{key}:{value}]"
        return result
    except FileNotFoundError:
        return "Arquivo não encontrado."
"""