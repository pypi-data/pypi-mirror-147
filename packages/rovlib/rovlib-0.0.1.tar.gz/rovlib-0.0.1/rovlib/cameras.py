import socket
import cv2
import pickle

class RovCam():
    """The camera module responsible for all camera connections to ROV, based on reusable sockets and openCV."""

    # max length of a single packet (which is more than enough to send over a full frame)
    MAX_DATAGRAM = 120000
    FRONT = 0
    ARM = 1
    MISC1 = 2
    MISC2 = 3

    def __init__(self, cam):
        # TODO: validate input
        self.__cam = cam
        self.port = 5000 + (cam*100)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(("", self.port))
        print("ROV CAM : Connected successfully")

    def __str__(self):
        return f"ROV Camera instance connected on rov camera {self.__cam}"

    def read(self):
        # TODO: handle errors
        data, _ = self.s.recvfrom(self.MAX_DATAGRAM)
        data = pickle.loads(data)
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return frame