import sys
import struct
import Image
#from cliente.cliente import socketcliente

def main ():


	#print struct.unpack('I',p)	
	#print "{:<15}".format('si')+'s'
	s = bytearray()
	s.append(10)
	#s.append(bytearray('megalol'))
	for c in s: print(c)

if __name__=="__main__":
	main()