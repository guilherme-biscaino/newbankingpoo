from Transacao import Transacao
from datetime import datetime
from FileManager import FileManager


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao, conta):

        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now(),
            }
        )
        FileManager.salvar(transacao, conta)


    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            try:
                if tipo_transacao.lower() == transacao['tipo'].lower():
                    yield transacao
            except AttributeError:
                yield transacao
