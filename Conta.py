from Cliente import Cliente


class Conta:
    def __init__(self, cliente=Cliente, numero=int, agencia=str, saldo=float, historico=str):
        self._cliente = cliente
        self._numero = numero
        self._agencia = agencia
        self._saldo = saldo
        self._historico = historico

    def get_saldo(self):
        return self._saldo

    def nova_conta(self, cliente, numero):
        pass

    def sacar(self, valor):
        pass

    def depositar(self, valor):
        pass
