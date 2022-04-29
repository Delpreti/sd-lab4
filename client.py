# Lado ativo/client

import socket
import sys

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5001       # porta que o par passivo esta escutando

def main():

    # verifica se existe um argumento passado na entrada
    if len(sys.argv) != 2:
        print("O nome do arquivo deve ser passado como argumento")
        return

    result = ""
    # estabelece a conexao com o servidor
    with socket.create_connection((HOST, PORTA)) as s:
        s.sendall(bytes(sys.argv[1], 'utf-8')) # envia o nome do arquivo
        result = str(s.recv(1024),  encoding='utf-8') # recebe as 5 palavras em uma string de resposta

    if len(result) > 1: # verifica se a string voltou vazia (se algum erro ocorreu)
        # imprime o resultado
        print(f"As 5 palavras mais encontradas no arquivo {sys.argv[1]} foram: {result}")
    else:
        print("Erro, não foi possível obter os resultados.")

main()
