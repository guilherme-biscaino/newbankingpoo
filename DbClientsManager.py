import sqlite3


class DbClientsManager:

    con = sqlite3.connect("banco.db")
    # COMANDO PARA HABILITAR O USO DE FK NO SQLITE
    con.execute('PRAGMA foreign_keys = ON')
    cursor = con.cursor()

    # CRIAÇÃO DAS TABELAS CASO NÃO HAJAM NO SISTEMA
    # TÁ UMA PORCARIA, OTIMIZAR DEPOIS (USANDO EXECUTE MANY, SE CONSEGUIR)
    @classmethod
    def set_up_tables(cls):
        try:
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
            cls.cursor.execute("CREATE TABLE transacoes("
                            "id INTEGER PRIMARY KEY,"
                            "tipo VARCHAR(10),"
                            "valor FLOAT,"
                            "id_conta INTEGER,"
                            "FOREIGN KEY(id_conta) REFERENCES contas(id))")
        except sqlite3.OperationalError:
            pass
        except:
            print("Houve algo errado ao iniciar o banco de dados")
        cls.con.commit()

    @classmethod
    def cadastrar_cliente(cls, nome, senha, cpf, nascimento, agencia):
        cls.cursor.execute("INSERT INTO clientes (nome, senha, cpf, nascimento, agencia) VALUES (?,?,?,?,?)",
                           (nome, senha, cpf, nascimento, agencia))
        cls.con.commit()

    @classmethod
    def cadastrar_conta(cls, id_cliente):
        cls.cursor.execute("SELECT count(*) FROM contas")

        a = cls.cursor.fetchone()

        cls.cursor.execute("INSERT INTO contas (numero_conta, id_cliente, saldo) VALUES (?,?,0)", (a[0]+1, id_cliente))

        cls.con.commit()

    @classmethod
    def get_cliente(cls, cpf):
        cls.cursor.execute("SELECT * FROM clientes WHERE cpf = ?", (cpf,))
        return cls.cursor.fetchone()

    @classmethod
    def get_accounts_from_client_cpf(cls, cpf):
        cls.cursor.execute("SELECT numero_conta, saldo FROM contas "
                           "WHERE (SELECT id FROM clientes WHERE cpf = ?) = id_cliente", (cpf,))
        return cls.cursor.fetchall()



#DbClientsManager.cadastrar_cliente("guilherme", 123, 1, 000, 1)
#DbClientsManager.cadastrar_conta(1, 1)
#print("?")
#DbClientsManager.get_accounts_from_client_cpf("1")
#if DbClientsManager.get_cliente(2):
#    print("tem coisa")
#else:
#    print(DbClientsManager.get_cliente(2))
