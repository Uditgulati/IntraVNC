from pynput.mouse import Listener
import threading
import numpy as np



class monitorMouse():
	def __init__(self):
		self.left_click = False
		self.double_click = False
		self.right_click = False
		streamer = threading.Thread(target = self.startMonitoring)
		streamer.start()

	def startMonitoring(self):
		with Listener(
		on_click=self.on_click,
		on_scroll=self.on_scroll) as listener:
			listener.join()

	def on_click(x, y, button, pressed):
		print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
		self.left_click = True

	def on_scroll(x, y, dx, dy):
		print('Scrolled {0}'.format((x, y)))