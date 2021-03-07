import socket
import struct
import select
import time
class RCON:
    def __init__(self, host, password, port=25575):
        self.host = host
        self.password = password
        self.port = port
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.send(3, self.password)
    def __enter__(self):
        self.connect()
        return self
    def __exit__(self, exc_type, exc_value, trace):
        self.disconnect()
    def disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
    def send(self, output_type, output_data):
        """Sends packet,

        RCON PROTOCOL
        LENGTH      int     Length of remainder of packet.
        REQUESTID   int     Request ID of packet
        TYPE        int     3 login, 2 command, 0 multipacket response
        PAYLOAD     byte[]  NULL terminated ASCII text
        PAD         byte    NULL

        Args:
            output_type (int): Packet type
            output_data (str): Payload string

        Returns:
            Returns response
        """
        if self.socket is None:
            return False
        output_payload = (
            # <ii - Matches fields REQUESTID and TYPE respectively: 0 is REQUESTID and output_type is TYPE
            # output_data Matches fields PAYLOAD without NULL termination
            # \x00 characters match the termination and PAD of the packet
           struct.pack("<ii", 0, output_type) + output_data.encode("utf-8") + b"\x00\x00"
        )
        # Matches LENGTH field
        output_length = struct.pack("<i", len(output_payload))
        self.socket.send(output_length + output_payload)
        input_data = ""
        while True:
            (input_length,) = struct.unpack("<i", self.read(4))
            input_payload = self.read(input_length)
            input_id, input_type = struct.unpack("<ii", input_payload[:8])
            input_data_partial, input_padding = input_payload[8:-2], input_payload[-2:]

            if input_padding != b"\x00\x00":
                raise Exception("FAIL")
            if input_id == -1:
                raise Exception("Login failed")
            input_data += input_data_partial.decode("utf-8")
            if len(select.select([self.socket], [], [], 0)[0]) == 0:
                return input_data
    def read(self, length):
        data = b""
        while len(data) < length:
            data += self.socket.recv(length-len(data))
        return data
    def command(self, command):
        result = self.send(2, command)
        time.sleep(0.003)
        return result
if __name__ == "__main__":
    def test(output_type, output_data):
        output_payload = (
           struct.pack("<ii", 0, output_type) + output_data.encode("utf-8") + b"\x00\x00"
        )
        
        output_length = struct.pack("<i", len(output_payload))
        print(struct.pack("<i", 0))
        print(struct.pack("<ii", 0, 2))
        print(output_length)
        print(output_payload)
        print((output_length + output_payload))
    test(2, "gamemode 1")