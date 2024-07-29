import sqlite3


class DbTransactionManager:

    con = sqlite3.connect("banco.db")
    cursor = con.cursor()

    @classmethod
    def sacar(cls, numero_conta, valor):
        cls.cursor.execute("UPDATE contas SET saldo = (saldo - ?) WHERE numero_conta = ?", (valor, numero_conta))
        cls.cursor.execute("INSERT INTO transacoes(tipo,valor,id_conta) VALUES (?,?,?)", ("saque", valor, numero_conta))
        cls.con.commit()

    @classmethod
    def depositar(cls, numero_conta, valor):
        cls.cursor.execute("UPDATE contas SET saldo = (saldo + ?) WHERE numero_conta = ?", (valor, numero_conta))
        cls.cursor.execute("INSERT INTO transacoes(tipo,valor,id_conta) VALUES (?,?,?)", ("deposito", valor, numero_conta))
        cls.con.commit()

    @classmethod
    def extrato(cls, numero_conta):
        cls.cursor.execute("SELECT c.numero_conta, c.saldo, t.tipo, t.valor FROM"
                       " contas as c, transacoes as t WHERE c.numero_conta = ? or t.id_conta = ?", (numero_conta, numero_conta))
        return cls.cursor.fetchall()


