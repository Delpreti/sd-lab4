import rpyc
import random
import threading
from rpyc.utils.server import ThreadedServer

class MyService(rpyc.Service):

	def __init__(self):
		super(MyService, self).__init__()
		self.connections = []
		self.value = random.randint(1,20)
		self.father = None
		self.name = None

	def exposed_conectar(self, ip_string, porta):
		c = rpyc.connect(ip_string, porta)
		self.connections.append(c)
		return c.root

	def exposed_set_name(self, namae):
		self.name = namae

	def exposed_leader_info(self, caller_name):
		if self.father is not None:
			return (self.name, 0)
		self.father = caller_name

		print(f"[{self.name}, {self.value}] Alcancado pelo node {caller_name}.")

		result = (self.name, self.value)
		for connection in self.connections:
			try:
				l_name, l_value = connection.root.leader_info(self.name)
				if l_value > self.value:
					if l_name != self.father:
						result = (l_name, l_value)
			except:
				print("estranho, mas vamo prosseguir")

		print(f"[{self.name}, {self.value}] Estou retornando {result}.")

		return result

	def exposed_find_leader(self):
		l_name, l_value = self.exposed_leader_info(self.name)
		if l_value < self.value:
			print("Eu era o lider esse tempo todo...")
			return
		print(f"Encontrei o lider: ({l_name}, {l_value})")

def start_service(port_number):
    t = ThreadedServer(MyService, port=port_number)
    t.start()

def main():
	# Lista de portas a serem utilizadas
	lista_node = [10001, 10002, 10003, 10004, 10005, 10006]

	# Inicializo os nos
	for n in lista_node:
		st = threading.Thread(target=start_service, args=(n,))
		#st.setDaemon(True)
		st.start()

	# Defino as conexoes e nomeio cada node
	# para o node A inicial eu uso o connect, as outras conexoes sao entre os nos
	n0 = rpyc.connect("localhost", 10001)
	n0.root.set_name("a")

	n1 = n0.root.conectar("localhost", 10002)
	n1.set_name("b")

	n2 = n1.conectar("localhost", 10003)
	n2.set_name("c")

	n3 = n2.conectar("localhost", 10004)
	n3.set_name("d")

	n4 = n3.conectar("localhost", 10005)
	n4.set_name("e")

	n5 = n1.conectar("localhost", 10006)
	n5.set_name("f")

	n6 = n5.conectar("localhost", 10005)
	n6.set_name("g")

	#Inicio a eleicao pelo no raiz, e recupero o resultado com essa conexao
	n0.root.find_leader()

main()