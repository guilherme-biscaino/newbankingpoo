from Conta import Conta
from Saque import Saque


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        if valor > self.limite:
            print(f"O valor de saque ({valor})não pode ser maior que o limite ({self.limite})")
            return False
        elif numero_saques >= 3:
            print("Operação falhou, número de saques ultrapassou a quantidade diaria de saques")
        else:
            return super().sacar(valor)

    def depositar(self, valor: float):
        return super().depositar(valor)
