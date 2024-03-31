from Conta import Conta


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float):
        super().sacar(valor)

    def depositar(self, valor: float):
        super().depositar(valor)
