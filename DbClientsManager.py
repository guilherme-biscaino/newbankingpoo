import sqlite3


class DbClientsManager:

    con = sqlite3.connect("banco.db")
    con.execute('PRAGMA foreign_keys = ON')
    cursor = con.cursor()

    # CRIAÇÃO DAS TABELAS CASO NÃO HAJAM NO SISTEMA
    # TÁ UMA PORCARIA, OTIMIZAR DEPOIS (USANDO EXECUTE MANY, SE CONSEGUIR)
    @classmethod
    def set_up_tables(cls):
        # CRIA A TABELA DE CLIENTES
        cls.cursor.execute("CREATE TABLE clientes("
                           "id INTEGER PRIMARY KEY,"
                           "nome VARCHAR(50),"
                           "senha VARCHAR(15),"
                           "cpf VARCHAR(11),"
                           "nascimento VARCHAR(8),"
                           "agencia INT NOT NULL )")

        # CRIA A TABELA DE CONTAS
        cls.cursor.execute("CREATE TABLE contas("
                           "id INTEGER PRIMARY KEY,"
                           "numero_conta VARCHAR(12),"
                           "id_cliente INT,"
                           "saldo FLOAT,"
                           "FOREIGN KEY(id_cliente) REFERENCES clientes(id))")

        # CRIA A TABELA DE LOG DE TRANSAÇÕES
        cls.cursor.execute("CREATE TABLE transacao("
                           "id PRIMARY KEY,"
                           "tipo VARCHAR(10),"
                           "valor FLOAT,"
                           "id_conta INTEGER)")

        cls.con.commit()

    @classmethod
    def cadastrar_cliente(cls, nome, senha, cpf, nascimento, agencia):
        cls.cursor.execute("INSERT INTO clientes (nome, senha, cpf, nascimento, agencia) VALUES (?,?,?,?,?)",
                           (nome, senha, cpf, nascimento, agencia))
        cls.con.commit()

    @classmethod
    def cadastrar_conta(cls, numero_conta, id_cliente):
        cls.cursor.execute("INSERT INTO contas (numero_conta, id_cliente, saldo) VALUES (?,?,?)",
                           (numero_conta, id_cliente, 0.0))
        cls.con.commit()


DbClientsManager.set_up_tables()
DbClientsManager.cadastrar_cliente("guilherme", 123, 1234, 000, 1)
DbClientsManager.cadastrar_conta(1, 1)
