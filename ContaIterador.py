
class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""
            Nome do cliente: {conta.cliente.nome}
            Número da conta: {conta.numero}
            Agencia da conta: {conta.agencia}
            Saldo atual: {conta.saldo}"""

        except IndexError:
            raise StopIteration

        finally:
            self._index += 1
