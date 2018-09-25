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
	host = '192.168.225.46'
	port = 5006

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))

	mouse = Controller()

	mouse_listener = monitorMouse()

	width = int(getResolutionWidth())
	height = int(getResolutionHeight())

	message = raw_input('-> ')
	flag = False
	while(message.lower() != 'quit'):
		to_send = str()
		if mouse_listener.left_click:
			mouse_listener.left_click = False
			print('Left click detected.')
			to_send += str('1')
		scale_position = (mouse.position[0] * 100.00 / height,\
			mouse.position[1] * 100.00 / width)
		
		s.send(to_send)
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
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	s.close()