import socket
import sys




def read_trivia(data):

    print 'pokemon id:'+ str(data[1])
    print 'image size:'+ struct.unpack('I',data[2:7])
    print 'opcion 1:'+ str(data[7:24])
    print 'opcion 2:'+ str(data[24:41])
    print 'opcion 3:'+ str(data[41:58])  



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.settimeout(3)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)


try:
    
    # Send data
    s = bytearray()
    #s.append(10)
    s.append(10)
    sock.sendall(s)

    # Look for the response
    amount_received = 0
    amount_expected = len(s)
    data = ''
    while True:
        aux = sock.recv(1024)
        data += aux
        print aux
        if not aux:
            print 'aiura'
            break
        else:
            print 'not aiura'
    print 'ya se salio'
    message = data
    if message[0] == 20:
        read_trivia(message)
    elif message[0] == 21:
        print 21

finally:
    print  'closing socket'
    sock.close()

