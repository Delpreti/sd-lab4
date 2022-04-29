# Lado passivo/server

import socket, re
import select
import sys
import threading

HOST = ''     # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  # porta onde chegarao as mensagens para essa aplicacao

#define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]
#armazena as conexoes ativas
conexoes = {}
#lock para acesso do dicionario 'conexoes'
lock = threading.Lock()

def atendeCliente(conn, addr):
    lock.acquire()
    conexoes[conn] = addr
    lock.release()
    print("Accepted connection from: ", addr)
    while True:
        # Recebe os dados enviados pelo cliente
        print("Awating orders from: ", addr)
        data = conn.recv(1024)
        print("Teste")
        if not data:
            print(str(addr) + '-> encerrou')
            lock.acquire()
            del conexoes[conn] #retira o cliente da lista de conexoes ativas
            lock.release()
            conn.close() # encerra a conexao com o cliente
            return

        try:
            # tenta realizar a leitura do arquivo
            contents = read_file(str(data, encoding='utf-8'));
            # se der certo, conta as palavras e envia o resultado pro cliente
            conn.sendall(bytes(", ".join(high_words(word_count(contents), 5)), 'utf-8'))
        except FileNotFoundError:
            # se der errado, envia para o cliente uma string vazia
            conn.sendall(bytes("Arquivo não existe", 'utf-8'))

def word_count(string):
    """ Metodo para contar as ocorrencias de cada palavra em um determinado texto """
    result = {}
    unique_words = set(re.split(r"\W+", string))
    for word in unique_words:
        result[word] = len(re.findall(r" ?" + word + r"\w", string))
    return result

def high_words(counted, amount=1):
    # ordena o dicionario por valor
    # pega os i primeiros em uma lista de tuplas
    # e retorna apenas uma lista com as chaves
    return dict(sorted(counted.items(), key=lambda item: item[1])[:amount]).keys()

def read_file(filename):
    # realiza a leitura do arquivo
    with open(filename, "r") as f:
        return f.read()

def main():

    # inicializa o servidor
    with socket.socket() as s:
        # configura o socket
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORTA))
        s.listen(5)
        s.setblocking(False)
        entradas.append(s)

        print(f"Server started, listening on port {PORTA}")

        while True:
            leitura, escrita, excecao = select.select(entradas, [], [])
            for pronto in leitura:
                if pronto == s:
                    cliente = threading.Thread(target=atendeCliente, args=s.accept())
                    cliente.start()
                elif pronto == sys.stdin: #entrada padrao
                    cmd = input()
                    if cmd == 'fim': #solicitacao de finalizacao do servidor
                        if not conexoes: #somente termina quando nao houver clientes ativos
                            s.close()
                            sys.exit()
                        else: print("ha conexoes ativas")
                    elif cmd == 'hist': #outro exemplo de comando para o servidor
                        print(str(conexoes.values()))

main()
