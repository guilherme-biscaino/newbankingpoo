from Historico import Historico


class Conta:
    def __init__(self, cliente, numero: int):
        self._cliente = cliente
        self._numero = numero
        self._agencia = 1
        self._saldo = 0
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    def get_cliente(self):
        return self._cliente

    def get_numero(self):
        return self._numero

    def get_agencia(self):
        return self._agencia

    def get_historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero: int, ):
        return cls(cliente, numero)

    def sacar(self, valor: float) -> bool:

        saldo = self._saldo
        value_exceed_saldo = valor > saldo
        if value_exceed_saldo:
            print("O valor a sacar não pode exceder o saldo!")
            return False
        elif valor < 0:
            print("O valor sacado não pode ser negativo!")
            return False
        else:
            print(f"Foi sacado R${valor} da sua conta, \n obrigado por usar novos serviços.")
            self._saldo -= valor

        return True

    def depositar(self, valor: float) -> bool:
        if valor < 0:
            print("O valor que deseja depositar não pode ser negativo!")
            return False
        else:
            self._saldo += valor

        return True

    @property
    def historico(self):
        return self._historico
