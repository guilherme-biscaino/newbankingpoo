import DbTrasactionManager
from Historico import Historico
from DbClientsManager import DbClientsManager
from DbTrasactionManager import DbTransactionManager


class Conta:
    def __init__(self, cliente, numero: int):
        self._cliente = cliente
        self._numero = numero
        self._agencia = 1
        self._saldo = 0

    @property
    def saldo(self):
        return self._saldo

    @property
    def cliente(self):
        return self._cliente

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @classmethod
    def nova_conta(cls, cliente, numero: int, ):
        return cls(cliente, numero)

    @classmethod
    def sacar(cls, valor: float, conta) -> bool:
        print(conta)
        saldo = DbClientsManager.get_saldo(conta)[0]

        value_exceed_saldo = valor > saldo
        if value_exceed_saldo:
            print("O valor a sacar não pode exceder o saldo!")
            return False
        elif valor < 0:
            print("O valor sacado não pode ser negativo!")
            return False
        else:
            print(f"Foi sacado R${valor} da sua conta, \n obrigado por usar novos serviços.")
            DbTransactionManager.sacar(conta, valor)

        return True

    @classmethod
    def depositar(self, valor: float, conta) -> bool:
        if valor < 0:
            print("O valor que deseja depositar não pode ser negativo!")
            return False
        else:
            DbTransactionManager.depositar(conta,valor)

        return True

    @classmethod
    def get_historico(cls, conta):
        print(conta)
        input()
        return DbTransactionManager.extrato(conta)
