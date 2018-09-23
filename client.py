import socket
import cv2
import numpy as np
import pyscreenshot
import imutils
from cStringIO import StringIO
import subprocess
from pynput.mouse import Button, Controller
from mouse_input import monitorMouse



def recieveNumpy(c):

		length = None
		ultimate_buffer = ""
		while True:
			data = c.recv(1024)
			ultimate_buffer += data
			if len(ultimate_buffer) == length:
				break
			while True:
				if length is None:
					if ':' not in ultimate_buffer:
					    break
					# remove the length bytes from the front of ultimate_buffer
					# leave any remaining bytes in the ultimate_buffer!
					length_str, ignored, ultimate_buffer = ultimate_buffer.partition(':')
					length = int(length_str)
				if len(ultimate_buffer) < length:
					break
				# split off the full message from the remaining bytes
				# leave any remaining bytes in the ultimate_buffer!
				ultimate_buffer = ultimate_buffer[length:]
				length = None
				break
		final_image = np.load(StringIO(ultimate_buffer))['frame']
		print 'frame received'
		return final_image

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


if __name__ == '__main__':
	host = '192.168.225.54'
	port = 5005

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))

	mouse = Controller()

	mouse_listener = monitorMouse()

	width = int(getResolutionWidth())
	height = 0

	message = raw_input('-> ')
	flag = False
	while(message.lower() != 'quit'):
		if mouse_listener.left_click:
			mouse_listener.left_click = False
			print('Left click recorded.')
		s.send(str(mouse.position))
		frame = recieveNumpy(s)
		h, w, channels = frame.shape
		height = width * h / w
		print("Recieved from server: ")
		frame_scaled = cv2.resize(frame, (width, height))
		if flag == False:
			cv2.namedWindow('Frame', cv2.WND_PROP_FULLSCREEN)
			cv2.setWindowProperty('Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
			flag = True
		cv2.imshow('Frame', frame_scaled)
		if cv2.waitKey(5) & 0xFF == ord('q'):
			break
	s.close()