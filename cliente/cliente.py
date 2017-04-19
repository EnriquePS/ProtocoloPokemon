import socket
import sys




# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)


try:
    
    # Send data
    s = bytearray()
    #s.append(10)
    s.append(11)
    s.append(10)
    s.append(10)
    sock.sendall(s)

    # Look for the response
    amount_received = 0
    amount_expected = len(s)
    
    while True:
        data = sock.recv(16)
        print  'received "%s"' % data
        if not data: break

finally:
    print  'closing socket'
    sock.close()

