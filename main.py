import datetime
import textwrap

import Conta
import DbTrasactionManager
from Cliente import Cliente
from ContaCorrente import ContaCorrente
from ContaIterator import ContaIterator
from DbClientsManager import DbClientsManager
from Deposito import Deposito
from PessoaFisica import PessoaFisica
from Saque import Saque
from FileManager import FileManager


FileManager.checkfiles()
DbClientsManager.set_up_tables()


# menu principal
def menu():

    menu = """
    ***Menu***
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair
        [nu] Criar novo usuário
        [nc] Criar nova conta
        [l] Listar suas contas
    ********
    """
    return input(menu)
def log_creator(funcao):

    def envelope(*args, **kwargs):
        resultado = funcao(*args, **kwargs)
        current_time = datetime.datetime.now()
        formated_time = current_time.strftime('%d-%m-%Y %H:%M:%S')
        print("=" * 100)
        print(f"dentro do logger {datetime.datetime.now()}")
        print(f"Operação de {funcao.__name__}, executada as: {formated_time}")
        FileManager.save_to_log(formated_time, funcao.__name__, resultado, *args, **kwargs)
        print(f"{formated_time} : Função {funcao.__name__} executada com os parametros {args} e {kwargs} gerando: {resultado}")

    return envelope
# RFE: Menu de login
def init_menu():
    log_menu = """
                Bem vindo ao NewBanking
                selecione a opção (1) caso queira fazer login na sua conta.
                selecione a opção (2) caso deseje criar uma nova conta.
    """
    return input(log_menu)


# RFE: deprecated, função de login.. atualizar para conformar com poo
def login():
    try:
        print("por favor faça login na sua conta.")
        cpf = input('Digite seu cpf: \n')
        pw = input("Digite sua senha: \n")
        client_info = DbClientsManager.get_cliente(cpf)
        if cpf == client_info[3] and pw == client_info[2]:
            return client_info
        else:
            print("usuario ou senha incorretos")
            login()
    except KeyError:
        print("Usuário não existe")
        login()


#  função responsavel por retornar priMeiro cliente com o cpf passado
def filtrar_contas(cpf):
    return DbClientsManager.get_cliente(cpf) if DbClientsManager.get_cliente(cpf) else None
    # se cpf do cliente esta presente no bd clientes retorna info sobre o cliente, caso não volte falso.


@log_creator
# poo v2
def deposito(cliente):

    conta = input("Digite o numero da conta que deseja depositar")

    valor = float(input("digite o valor do deposito: \n"))

    transacao = Deposito(valor, conta)

    Cliente.realizar_transacao(conta, transacao)

#@log_creator
def saque(cliente):

    # cpf = input("Digite o cpf do cliente:")
    # cliente = filtrar_contas(cpf)

    #if not cliente:
    #    print("Cliente não encontrado! \n")
    #    return
    conta = input("Digite o número da conta que deseja sacar o dinheiro")
    valor = float(input("informe o valor do saque"))
    transacao = Saque(valor, conta)

    #conta = recuperar_conta_cliente(cliente)
    #if not conta:
    #    return

    Cliente.realizar_transacao(conta, transacao)


#@log_creator
def Extrato(cliente):

    account_nun = input("digite o numero da conta que deseja obter o extrato")
    extratoChoice = input(
    '''
    Digite "Saque" para obter o extrato dos seus saques
    Digite "Deposito" para obter o extrato dos seus depositos
    Caso queira obter o extrato completo deixe em branco
    ''')

    print("==========EXTRATO==========")
    transacoes = DbTrasactionManager.DbTransactionManager.extrato(account_nun)

    extrato = ""

    is_empty = True

    for transacao in transacoes:
        is_empty = False
        print(f"efetuada a operação de: \n\t{transacao[2]}\nno valor de: \n\tR${transacao[3]} \n")

    if transacoes:
        print(f"Saldo atual: \n\tR${transacoes[0][1]}")
    else:
         print("Não foram feitas transações!")

    print("=============================")

@log_creator
# poo v2
def criar_cliente():
    cpf = input("informe o cpf do cliente(somente numeros)")

    cliente = filtrar_contas(cpf)
    if cliente:
        print("já existe um cliente com este cpf!")
        return

    nome = input("digite o nome completo")
    data_nascimento = input("digite a data de nascimento (dia-mes-ano)")
    endereco = input("digite seu endereço(logradouro, nro - bairro - cidade/estado)")
    senha = input("digite uma senha")

    DbClientsManager.cadastrar_cliente(nome,senha,cpf,data_nascimento,1)
    print("\n Cliente criado com sucesso!")


@log_creator
def criar_conta():
    cpf = input("Digite o seu cpf: \n")
    cliente = filtrar_contas(cpf)

    if not cliente:
        print("Cliente não encontrado!, fluxo de criação encerrado")
        return
    DbClientsManager.cadastrar_conta(cliente[0])
    print("Conta criada com sucesso!\n")
    print(f"o numero da sua nova conta é: {DbClientsManager.get_accounts_from_client_cpf(cpf)[-1][0]}")
    input("\npressione qualquer tecla para continuar!")

def listar_contas_do_usuario(cpf):
    contas = DbClientsManager.get_accounts_from_client_cpf(cpf)
    print("="*50)
    for conta in contas:
        print(f"numero da conta: {conta[0]}, saldo: {conta[1]} \n")
    print("="*50)

def sair(current_user):
    print("Obrigado por usar nosso sistema!")
    current_user = 0
    return current_user


def main(current_user):
    a = DbClientsManager.get_accounts_from_client_cpf(current_user[3])
    if not a:
        print("Bem vindo novo usuário, iremos criar uma conta para você!")
        criar_conta()

    while True:

        opcao = menu()

        if opcao == "d":
            deposito(current_user[3])

        elif opcao == "s":
            saque(current_user[3])

        elif opcao == "e":
            Extrato(current_user[3])

        # elif opcao == "nu":
        #     criar_cliente()

        elif opcao == "nc":
            criar_conta()

        elif opcao == "l":
            listar_contas_do_usuario(current_user[3])

        elif opcao == "q":
            break

        else:
            print("A opção escolhida não é compatível, por favor selecione uma opção disponivel no menu.")


# RFE: função de login, a ser apresentada antes de liberar menu principal.
def initiate():
    init_option = init_menu()
    if (init_option == "1"):
        current_user = login()
        main(current_user)

    elif (init_option == "2"):
        criar_cliente()
        current_user = login()
        main(current_user)

    elif (init_option == "10"):
        print("delisgando sistema")
        input()

    elif (init_option == "12"):
        for i in enumerate(contas):
            print(
                f"numero da conta: {contas[i[1]]['numero_da_conta']}, nome do titular: {contas[i[1]]['nome']}, agencia da conta: {contas[i[1]]['agencia']}, saldo: {contas[i[1]]['saldo']}")
            init(usuarios, contas, current_user, contas_no_banco)

    else:
        print("desculpe, a opção que escolheu não é valida")
    init(usuarios, contas, current_user, contas_no_banco)

initiate()

# TODO: realizar limpeza no codigo

#please someone help me this code looks like shit and idk what i'm doing