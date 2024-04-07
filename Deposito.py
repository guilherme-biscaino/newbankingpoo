from Conta import Conta
from Transacao import Transacao


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        sucesso_transacao = conta.depositar(self.valor)

        # FIXME: por algum motivo obscuro sucesso_transacao retorna "None" mesmo definindo o retorno na função deposito
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

