import socket
import random
import sys
import Image
import struct
from multiprocessing import Pool
import threading

class Server(object):
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.pokemons = {'pokemon1':1,'pokemon2':2,'pokemon3':3}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
    def eval_trivia(self,respuesta):
		idpokemon=respuesta[1]
		resp_pok=respuesta[2]
		ba = bytearray()
		#appending the code for the protocol	
		ba.append(21)
		ba.append(idpokemon == resp_pok)
		return ba

    def trivia(self):
		pok = random.randint(1,3)
		if pok == 1:
			im_name = 'uno.png'
		elif pok == 2:
			im_name = 'dos.png'
		else:
			im_name = 'tres.png'
		with open(im_name, "rb") as imageFile:
		  f = imageFile.read()
		  b = bytearray(f)
		imagesize= len(b)

		ba = bytearray()
		#el codigo par aindicar que se esta enviando la trivia
		ba.append(20)
		#send the code of the pokemon
		ba.append(pok)
		#todo read the file and send the size:
		p = struct.pack("I", imagesize)
		s = bytearray(p)
		ba+= s
		#todo send the 3 names form the array
		ba+=bytearray('pokemon1'.ljust(15)[:15])
		ba+=bytearray('pokemon2'.ljust(15)[:15])
		ba+=bytearray('pokemon3'.ljust(15)[:15])
		#appending imsmage
		ba += b
		#return the content of the trivia to send
		return ba



    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, connection, address):
	    try:
	    	progress = True
	    	while progress:
			    print  'connection from'+ str(address)
			    data = '' 
			    # Receive the data in small chunks and retransmit it
			    while True:
			        aux = connection.recv(32)
			        if aux:
			        	data += aux
			        else:
			        	break

			    #aqui ya se temrno de recibir el mensaje
			   	byte_array = bytearray(data)
			   	#se solicita la tirivia
			   	if byte_array[0] == 10:
			   		print 'me estan pidiendo la trivia'
			   		connection.sendall( self.trivia() )
			   		print 'ya le mande la trivia'
			   		break
			   	#hay que revisar la respuesta de la trivia
			   	elif byte_array[0] == 11:
			   		print 'me esta enviando su respuesta'
			   		connection.sendall( self.eval_trivia(byte_array))
			   		progress = False
			   		print 'ya le respondi'
			   		break
			   	else:
			   		#todo: return error
			   		print 'cerrando conexion'
	        		connection.close()
		            
	    finally:
	        # Clean up the connection
	        print 'cerrando conexion'
	        connection.close()


# Create a TCP/IP socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
#server_address = ('localhost', 10000)
#print  'starting up on %s port %s' % server_address
#sock.bind(server_address)


# Listen for incoming connections
#sock.listen(5)

while True:
    # Wait for a connection
    #print  'waiting for a connection'
    #connection, client_address = sock.accept()
    #comm(connection)
    port_num = int(sys.argv[1])
    Server('',port_num).listen()
