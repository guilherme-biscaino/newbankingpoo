from Cliente import Cliente
from datetime import date


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    def nascimento(self):
        return self._nascimento
