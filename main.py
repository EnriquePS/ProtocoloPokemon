from cliente.cliente import socketcliente

def main ():
	cliente = socketcliente()
	cliente.connect('facebook.com',443)
	cliente.send('aiura')


if __name__=="__main__":
	main()