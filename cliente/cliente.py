import socket
import sys
import struct
import webbrowser

#este metdo lee la trivia, descarga la imagen y recive la respuesta del usuario
def read_trivia(data):
    print 'pokemon id:'+ str(data[1])
    size = struct.unpack('I',data[2:6])
    #print 'image size:'+ str(size[0])
    print 'QUIEN ES ESTE POKEMON?'

    image = data[51:51+size[0]]
    f = open('test.png','wb')
    f.write(image)
    f.close()
    webbrowser.open('test.png')
    answer = 0
    while answer not in {1,2,3}:
        print 'opcion 1:'+ str(data[6:21])
        print 'opcion 2:'+ str(data[21:36])
        print 'opcion 3:'+ str(data[36:51])  
        answer = input("ingresa el numero de la opcion valido: ")
    return answer

def read_eval(data):
    if data[1]:
        print 'lo adivinaste'
    else:
        print 'no lo adivinaste'


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.settimeout(3)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 9999)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)


try:
    
    # Send data
    s = bytearray()
    #solicitando la trivia
    s.append(10)
    sock.sendall(s)
    data = bytearray()
    count = 0
    answer = 0
    size = None
    while True:
        aux = sock.recv(16)
        if aux:
            data += bytearray(aux)
            #keeping a track on when to stop recieving info 
            count +=16

            if data[0] == 20:
                if size == None:
                    size = struct.unpack('I',data[2:6])
                elif size[0]+ 51<= count:
                    answer = read_trivia(data)
                    break
            else:
                print 'no se esta mandando la trivia correctament'

        else:
            break
    print 'evaluando la respuesta'
    
    #se va a enviar la respuesta
    s = bytearray()
    #solicitando la trivia
    s.append(11)
    s.append(data[1])
    s.append(answer)
    sock.sendall(s)
    data = bytearray()
    count = 0
    while True:
        aux = sock.recv(16)
        if aux:
            data += bytearray(aux)
            #keeping a track on when to stop recieving info 
            count +=16

            if data[0] == 21:
                print "antes de read eval "
                answer = read_eval(data)
                print 'despues del eval'
                break
            else:
                print 'error de comunicacion'

        else:
            print 'en el brak'
            break

finally:
    print  'closing socket'
    sock.close()

