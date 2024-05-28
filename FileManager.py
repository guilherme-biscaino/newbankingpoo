from datetime import datetime
import csv
import os.path


class FileManager:

    @classmethod
    def salvar(cls, transacao, conta):
        try:
            with open("bank_historic.csv", "a", newline="") as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow([conta.cliente.cpf,
                                 conta.numero,
                                 transacao.__class__.__name__,
                                 transacao.valor,
                                 datetime.now()])
        except IOError as exc:
            print("testando escrita em arquivos")

    @classmethod
    def checkfiles(cls):
        if not os.path.isfile("bank_historic.csv"):
            cls.create_transaction_historic()
        if not os.path.isfile("accounts.csv"):
            cls.create_accounts()

    @staticmethod
    def create_transaction_historic():
        try:
            with open("bank_historic.csv", "w", newline="") as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(["cpf", "conta", "tipo_transação", "valor", "data"])
        except IOError as exce:
            print(f"Houve um erro ao criar arquivo de inicialização {exce}")

    @staticmethod
    def create_accounts():
        try:
            with open("accounts.csv", "w", newline="") as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(["cpf", "conta", "saldo"])
        except IOError as exce:
            print(f"Houve um erro ao criar arquivo de inicialização {exce}")

