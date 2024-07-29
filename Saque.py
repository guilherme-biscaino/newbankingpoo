from Conta import Conta
from Transacao import Transacao


class Saque(Transacao):
    def __init__(self, valor, conta):
        self._valor = valor
        self._conta = conta

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        sucesso_transacao = Conta.sacar(self.valor, self._conta)

        #if sucesso_transacao:
        #    conta.historico.adicionar_transacao(self, conta)
