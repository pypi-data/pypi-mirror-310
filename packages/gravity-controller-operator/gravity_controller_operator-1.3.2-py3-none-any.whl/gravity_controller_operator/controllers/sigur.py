import socket
from _thread import allocate_lock
from gravity_controller_operator.controllers_super import ControllerInterface, \
    RelayControllerInterface
from abc import abstractmethod
from socket import socket


class SigurContollerABC(ControllerInterface):
    sock = None
    mutex = allocate_lock()

    def get_phys_dict(self, *args, **kwargs):
        """ Получить состояние входов или выходов с контроллера.
        Перед возвратом привести в вид словаря,
        где ключ - это номер реле или di, значение - 0 или 1.
        """
        response_dict = {}
        for point in range(self.starts_with, self.map_keys_amount):
            response = self.contr_send('"GETAPINFO" {}'.format(point))
            response = response.decode()
            ap_info = response.split(" ")
            status = ap_info[-2]
            if status in ("ONLINE_UNLOCKED", "ONLINE_NORMAL"):
                status = 0
            else:
                status = 1
            response_dict[point] = status
        return response_dict

    def contr_send(self, command, get_response=True):
        self.mutex.acquire()
        command = f'{command}\r\n'
        self.sock.send(command.encode("utf-8"))
        if get_response:
            response = self.sock.recv(1024)
            self.mutex.release()
            return response
        self.mutex.release()

    def contr_get(self):
        self.mutex.acquire()
        response = self.sock.recv(1024)
        self.mutex.release()
        return response

    # @abstractmethod
    # def get_phys_points_states(self):
    #   return []

    def login(self, login="Administrator", password=""):
        return self.contr_send(
            '"LOGIN" 1.8 "{}" "{}"\r\n'.format(login, password))


class SigurDI(SigurContollerABC):
    map_keys_amount = 5
    starts_with = 3

    def __init__(self, sock):
        super(SigurDI, self).__init__(sock)
        self.sock = sock
        self.login()
        self.update_dict()


class SigurRelay(SigurContollerABC):
    map_keys_amount = 3
    starts_with = 1

    def __init__(self, sock):
        super().__init__(sock)
        self.sock = sock
        self.login()
        self.update_dict()

    def change_phys_relay_state(self, num, state: bool):
        pass


class Sigur:
    model = "sigur"

    def __init__(self, ip, port=3312, login="Administrator", password="",
                 name="Sigur", *args, **kwargs):
        sock = socket()
        sock.connect((ip, port))
        self.relay_interface = SigurRelay(sock)
        self.di_interface = SigurDI(sock)
