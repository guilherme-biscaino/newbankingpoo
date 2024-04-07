from Conta import Conta
from Transacao import Transacao


class Cliente:
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas = []
        pass

    def realizar_transacao(self, conta: Conta, trasacao: Transacao):
        trasacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self._contas.append(conta)

    @property
    def contas(self):
        return self._contas
