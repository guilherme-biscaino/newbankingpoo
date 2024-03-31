from Conta import Conta
from ABC import ABC
class Transacao(ABC):
    def __init__(self):
        pass

    def valor(self):
        pass
    def registrar(self, conta: Conta):
        pass