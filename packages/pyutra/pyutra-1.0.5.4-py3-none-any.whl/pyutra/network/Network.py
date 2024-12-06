import socket
import re
import uuid

class Network:
    def get_device_ip(self):
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return False

    def get_mac_address(self):
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))