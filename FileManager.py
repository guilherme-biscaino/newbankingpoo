from datetime import datetime
import csv
import os.path


class FileManager:

    @classmethod
    def save_client(cls, nome, data_nascimento, cpf, endereco, senha):
        try:
            with open("accounts.csv", "a", newline="") as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow([cpf,
                                 nome,
                                 data_nascimento,
                                 endereco,
                                 "conta",
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
        if not os.path.isfile("log.txt"):
            cls.create_log_file()

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
                                 "saldo",
                                 "senha"])
        except IOError as exce:
            print(f"Houve um erro ao criar arquivo de inicialização {exce}")

    @staticmethod
    def create_log_file():
        try:
            with open("log.txt", "w", encoding="utf-8"):
                pass
        except IOError as exec:
            print(f"Não foi possível criar o arquivo código de erro: {exec}")

    @staticmethod
    def get_account(cpf):
        try:
            with open("accounts.csv", "r", newline="") as arquivo:
                reader = csv.DictReader(arquivo)
                for row in reader:
                    if row["cpf"] == cpf:
                        print(row)
                        return row["contas"]
        except IOError as exece:
            print(f"erro {exece}")


    #fixme não funciona
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

    @classmethod
    def save_to_log(cls, formatted_time, funcao, resultado, *args, **kwargs):
        try:
            with open("log.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(f"[{formatted_time}] : Função {funcao} executada com os parametros {args} e {kwargs} gerando: {resultado} \n")
        except IOError as excep:
            print(f"falha: {excep}")