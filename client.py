# Lado ativo/client

import socket
import sys

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5000       # porta que o par passivo esta escutando

def main():

    # estabelece a conexao com o servidor
    with socket.create_connection((HOST, PORTA)) as s:

        while True: 
            msg = input("Write a message ('exit' to end):")
            if msg == 'exit':
                break

            s.sendall(bytes(msg, 'utf-8')) # envia o nome do arquivo
            result = str(s.recv(1024),  encoding='utf-8') # recebe as 5 palavras em uma string de resposta

            if len(result) > 1: # verifica se a string voltou vazia (se algum erro ocorreu)
                # imprime o resultado
                print(f"As 5 palavras mais encontradas no arquivo {msg} foram: {result}")
            else:
                print("Erro, não foi possível obter os resultados.")

main()
