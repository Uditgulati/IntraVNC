# IntraVNC

An implementation of VNC server and client that works over local network.


## Introduction to VNC

In computing, Virtual Network Computing (VNC) is a graphical desktop sharing system that uses the Remote Frame Buffer protocol (RFB) to remotely control another computer. It transmits the keyboard and mouse events from one computer to another, relaying the graphical screen updates back in the other direction, over a network.

VNC is platform-independent – there are clients and servers for many GUI-based operating systems and for Java. Multiple clients may connect to a VNC server at the same time. Popular uses for this technology include remote technical support and accessing files on one's work computer from one's home computer, or vice versa. 

-wikipedia


## Installation and setup

Connect client and server machine to the same network and run the following commands.

```

git clone https://github.com/Uditgulati/IntraVNC.git

cd IntraVNC/

pip2 install -r requirements.txt

```

+	**On server machine:** `python2 server.py`

+	**On client machine:** `python2 client.py`

+	Press 'q' on client machine to exit.


## Contributing

Any kind of improvements are welcome. Feel free to fork and open a pull request.