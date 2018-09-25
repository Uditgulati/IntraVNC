import socket
import cv2
from scipy.misc import imresize
import numpy as np
import pyscreenshot
import imutils
from cStringIO import StringIO
from pynput.mouse import Button, Controller
import subprocess



def getMyIP():
	mySock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	mySock.connect(('8.8.8.8', 80))
	ip = mySock.getsockname()[0]
	mySock.close()
	return ip


def sendNumpy(c, image):
		if not isinstance(image, np.ndarray):
			print 'not a valid numpy image'
			return
		f = StringIO()
		np.savez_compressed(f, frame=image)
		f.seek(0)
		out = f.read()
		val = "{0}:".format(len(f.getvalue()))  # prepend length of array
		out = val + out
		try:
			c.sendall(out)
		except Exception:
			exit()
		print 'image sent'


def getResolutionWidth():
	cmd = ['xrandr']
	cmd2 = ['grep', '*']
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
	p.stdout.close()

	resolution_string, junk = p2.communicate()
	resolution = resolution_string.split()[0]
	width, height = resolution.split('x')
	return width

def getResolutionHeight():
	cmd = ['xrandr']
	cmd2 = ['grep', '*']
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
	p.stdout.close()

	resolution_string, junk = p2.communicate()
	resolution = resolution_string.split()[0]
	width, height = resolution.split('x')
	return height


if __name__ == '__main__':
	host = ''
	port = 5007

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))

	ip = getMyIP()
	print('Server IP address: ' + str(ip))
	print('Port no.: ' + str(port))

	s.listen(1)
	print("Now listening: ")
	c, addr = s.accept()
	print("Connection recieved: " + str(addr))

	mouse = Controller()

	width = int(getResolutionWidth())
	height = int(getResolutionHeight())

	while True:
		data = c.recv(1024)
		if data[0] == '1':
			data = data[1:]
			mouse.press(Button.left)
			mouse.release(Button.left)
		val = [x.strip() for x in data.split(',')]
		print(val)
		val1 = (float(val[0][1:]), float(val[1][:-1]))
		v0 = val1[0] * height / 100.00
		v1 = val1[1] * width / 100.00
		print(v0, v1)
		mouse.position = (int(v0), int(v1))
		if not data:
			break
		print("From Connected user: " + str(data))
		image = pyscreenshot.grab()
		image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
		frame_resize = imresize(image, .5)
		print("Sending: ")
		sendNumpy(c, frame_resize)
	c.close()