import socket
import sys
import Image
import struct



pokemons = {'pokemon1':1,'pokemon2':2,'pokemon3':3}

#this method generates the trivia to send to the client
def createtrivia():
	with open("uno.png", "rb") as imageFile:
	  f = imageFile.read()
	  b = bytearray(f)
	imagesize= len(b)

	ba = bytearray()
	#el codigo par aindicar que se esta enviando la trivia
	ba.append(20)
	#send the code of the pokemon
	ba.append(1)
	#todo read the file and send the size:
	p = struct.pack("I", imagesize)
	s = bytearray(p)
	ba+= s
	#todo send the 3 names form the array
	ba+=bytearray('pokemon1'.ljust(15)[:15])
	ba+=bytearray('pokemon1'.ljust(15)[:15])
	ba+=bytearray('pokemon1'.ljust(15)[:15])
	#appending immage
	ba += b
	#return the content of the trivia to send
	return ba



def eval_trivia(respuesta):
	idpokemon=respuesta[1]
	resp_pok=respuesta[2]
	ba = bytearray()
	#appending the code for the protocol	
	ba.append(21)
	ba.append(idpokemon == resp_pok)
	return ba

#if the code is one of the specified in the projkect the proceed if not then close the connecgtion witht error
def comm(connection):
    try:
    	while True:
		    print  'connection from'+ str(client_address)
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
		   		connection.sendall(createtrivia())
		   	#hay que revisar la respuesta de la trivia
		   	elif byte_array[0] == 11:
		   		print 'me esta enviando su respuesta'
		   		connection.sendall(eval_trivia(byte_array))
		   	else:
		   		#todo: return error
		   		return None
	            
    finally:
        # Clean up the connection
        connection.close()



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
print  'starting up on %s port %s' % server_address
sock.bind(server_address)


# Listen for incoming connections
sock.listen(5)

while True:
    # Wait for a connection
    print  'waiting for a connection'
    connection, client_address = sock.accept()
    comm(connection)
