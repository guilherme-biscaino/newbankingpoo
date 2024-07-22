import sqlite3

con = sqlite3.connect("banco.db")
cursor = con.cursor()


def sacar(numero_conta, valor):
    cursor.execute("UPDATE contas SET saldo = (saldo - ?) WHERE numero_conta = ?", (valor, numero_conta))
    cursor.execute("INSERT INTO transacoes(tipo,valor,id_conta) VALUES (?,?,?)", ("saque", valor, numero_conta))
    con.commit()


def deposito(numero_conta, valor):
    cursor.execute("UPDATE contas SET saldo = (saldo + ?) WHERE numero_conta = ?", (valor, numero_conta))
    cursor.execute("INSERT INTO transacoes(tipo,valor,id_conta) VALUES (?,?,?)", ("deposito", valor, numero_conta))
    con.commit()


def extrato(numero_conta):
    cursor.execute("SELECT c.numero_conta, c.saldo, t.tipo, t.valor FROM"
                   " contas as c, transacoes as t WHERE c.id = ? or t.id = ?", (numero_conta,numero_conta))
    result = cursor.fetchone()
    print(result)



sacar(1, 50)
extrato(1)