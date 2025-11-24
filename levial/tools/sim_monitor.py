import socket
import struct
import logging
import threading
import time

logger = logging.getLogger("sim_monitor")

class SimMonitor:
    def __init__(self, ip="127.0.0.1", port=49000):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False
        self.latest_data = {}

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._loop)
        self.thread.daemon = True
        self.thread.start()
        logger.info(f"Listening for X-Plane on {self.ip}:{self.port}")

    def stop(self):
        self.running = False

    def _loop(self):
        self.sock.bind((self.ip, self.port))
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                self._parse_packet(data)
            except Exception as e:
                logger.error(f"UDP Error: {e}")
                time.sleep(1)

    def _parse_packet(self, data):
        # Header is 5 bytes: 'DATA' + \0
        if data[:5] != b'DATA\0':
            return

        # Data follows in 36-byte chunks (4 byte int index + 8 floats)
        # We need to map X-Plane data refs to indices.
        # This is a simplified parser assuming standard X-Plane UDP output.
        # Real implementation needs to know which index maps to what.
        # For MVP, we just log that we got data.
        pass

    def get_telemetry(self):
        return self.latest_data

if __name__ == "__main__":
    # Test run
    logging.basicConfig(level=logging.INFO)
    mon = SimMonitor()
    mon.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mon.stop()
