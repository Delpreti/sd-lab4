# Lado passivo/server

import socket, re

HOST = ''     # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5001  # porta onde chegarao as mensagens para essa aplicacao

def word_count(string):
    """ Metodo para contar as ocorrencias de cada palavra em um determinado texto """
    result = {}
    unique_words = set(re.split(r"\W+", string))
    for word in unique_words:
        result[word] = len(re.findall(r" ?" + word + r"\w", string))
    return result

def high_words(counted, i=1):
    # ordena o dicionario por valor
    # pega os i primeiros em uma lista de tuplas
    # e retorna apenas uma lista com as chaves
    return dict(sorted(counted.items(), key=lambda item: item[1])[:i]).keys()

def read_file(filename):
    # realiza a leitura do arquivo
    with open(filename, "r") as f:
        return f.read()

def main():

    # inicializa o servidor
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORTA))
        s.listen(1)
        print(f"Server started, listening on port {PORTA}")

        while True:
            # Aguarda uma nova conexao
            conn, addr = s.accept()
            with conn:
                # Informa quem conectou
                print("Accepted connection from", addr)

                # Recebe os dados enviados pelo cliente
                data = conn.recv(1024)
                print(data)
                if not data:
                    break

                try:
                    # tenta realizar a leitura do arquivo
                    contents = read_file(str(data, encoding='utf-8'));
                    # se der certo, conta as palavras e envia o resultado pro cliente
                    conn.sendall(bytes(", ".join(high_words(word_count(contents), 5)), 'utf-8'))
                except FileNotFoundError:
                    # se der errado, envia para o cliente uma string vazia
                    conn.sendall(bytes("Arquivo não existe", 'utf-8'))

main()
