from datetime import datetime
import csv
import os.path


class FileManager:

    @classmethod
    def save_client(cls, nome, data_nascimento, cpf, endereco, senha):
        contas = {}
        try:
            with open("accounts.csv", "a", newline="") as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow([cpf,
                                 nome,
                                 data_nascimento,
                                 endereco,
                                 contas,
                                 senha])
        except IOError:
            print("erro ao criar usuario")

    @classmethod
    def save_transaction(cls, transacao, conta):
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
            cls.create_transaction_history_file()
        if not os.path.isfile("accounts.csv"):
            cls.create_accounts_file()

    @staticmethod
    def create_transaction_history_file():
        try:
            with open("bank_historic.csv", "w", newline="") as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(["cpf", "conta", "tipo_transação", "valor", "data"])
        except IOError as exce:
            print(f"Houve um erro ao criar arquivo de inicialização {exce}")

    @staticmethod
    def create_accounts_file():
        try:
            with open("accounts.csv", "w", newline="") as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(["cpf",
                                 "nome",
                                 "data_nascimento",
                                 "endereco",
                                 "contas",
                                 "senha"])
        except IOError as exce:
            print(f"Houve um erro ao criar arquivo de inicialização {exce}")

    @staticmethod
    def get_account(cpf):
        try:
            with open("accounts.csv", "r", newline="") as arquivo:
                reader = csv.DictReader(arquivo)
                #writer = csv.DictWriter(arquivo, fildnames="contas")
                for row in reader:
                    if row["cpf"] == cpf:
                        print(row)
                        return row["contas"]
        except IOError as exece:
            print(f"erro {exece}")

    @classmethod
    def create_account(cls, cpf):
        try:
            with open("accounts.csv", "r", newline="") as arquivo:
                reader = csv.DictReader(arquivo)
                for row in reader:
                    if row["cpf"] == cpf:
                        row["contas"]

                #cls.get_account(cpf)

        except IOError as exece:
            print(f"erro {exece}")
