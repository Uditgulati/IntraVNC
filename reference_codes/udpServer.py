import socket



if __name__ == '__main__':
	host = '127.0.0.1'
	port = 5000

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host, port))

	print("Server started.")

	while True:
		data, addr = s.recvfrom(1024)
		print("From Connected user " + str(addr) + ": " + str(data.decode('utf-8')))
		data = str(data.decode('utf-8')).upper()
		print("Sending to " + str(addr) + ": " + str(data))
		s.sendto(data.encode('utf-8'), addr)
	s.close()