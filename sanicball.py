import json
import requests
import socket


class ServerList:
    def __init__(self, url: str):
        self.url = url
        self.server_addresses: list[str] = requests.get(self.url).content.decode("utf-8")[:-4].split("<br>")
        self.servers: list[Server] = []
        for addr in self.server_addresses:
            try:
                self.servers.append(Server(addr))
            except socket.timeout:
                pass


class Server:
    def __init__(self, addr: str, timeout: int = 0.25):
        self.ip = addr.split(":")[0]
        self.port = int(addr.split(":")[1])
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.__socket.settimeout(timeout)
        try:
            self.__socket.sendto(b'\x88\x00\x00\x00\x00', (self.ip, self.port))
            data, _ = self.__socket.recvfrom(4096)
            info = json.loads(data[7:])

            # Put info into variables
            self.name = info["Config"]["ServerName"]
            self.max_players = info["Config"]["MaxPlayers"]
            self.players = info["Players"]
            self.is_racing = info["InRace"]
        except socket.timeout:
            raise socket.timeout(f"The server did not respond in {timeout} seconds")
