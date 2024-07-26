import datetime
import textwrap

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
        [nc] Criar novo usuário
        [nu] Criar nova conta
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
def deposito(clientes):
    cpf = input("digite o cpf do cliente: \n")
    cliente = filtrar_contas(cpf, clientes)

    if not cliente:
        print("cliente não encontrado")
        return
    valor = float(input("digite o valor do deposito: \n"))

    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)
    print(f"apos deposito {datetime.datetime.now()}")


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("cliente não possui conta")
        print(cliente)
        print(cliente.contas)
        return

    return cliente.contas[0]

@log_creator
def saque(clientes):

    cpf = input("Digite o cpf do cliente:")
    cliente = filtrar_contas(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado! \n")
        return

    valor = float(input("informe o valor do saque"))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


@log_creator
def Extrato(clientes):
    cpf = input("Digite o CPF do cliente: \n")
    cliente = filtrar_contas(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado! \n")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    extratoChoice = input(
    '''
    Digite "Saque" para obter o extrato dos seus saques
    Digite "Deposito" para obter o extrato dos seus depositos
    Caso queira obter o extrato completo deixe em branco
    ''')

    print("==========EXTRATO==========")
    transacoes = conta.historico.transacoes

    extrato = ""

    is_empty = True

    for transacao in conta.historico.gerar_relatorio(extratoChoice if extratoChoice != '' else None):
        is_empty = False
        print(f"{transacao['tipo']}: R$:{transacao['valor']} \n")

    if is_empty:
        extrato = "Não foram feitas transações!"
    print(extrato)
    print(f"Saldo: \n\tR$ {conta.saldo:.2f}")
    print("=============================")


@log_creator
def criar_usuario(usuarios):
    nome = input("digite seu nome: \n")
    cpf = input("digite seu cpf: \n")
    endereco = input("digite seu endereço: \n")
    nascimento = input("data de nascimento: \n")
    senha = input("digite uma senha: \n")
    if (cpf not in usuarios):
        usuarios.update({f"{cpf}": {"nome": nome, "nascimento": nascimento, "endereco": endereco, "senha": senha}})
        print("sua conta foi criada com sucesso!")
        return usuarios, cpf
    else:
        print("já existe uma conta com seu cpf \n tente fazer login com seu cpf!")
        init_menu()
        return usuarios, cpf


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


    FileManager.save_client(nome, data_nascimento, cpf, endereco, senha)
    DbClientsManager.cadastrar_cliente(nome,senha,cpf,data_nascimento,1)

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n Cliente criado com sucesso!")


@log_creator
def criar_conta():
    cpf = input("Digite o cpf do cliente: \n")
    cliente = filtrar_contas(cpf)

    if not cliente:
        print("Cliente não encontrado!, fluxo de criação encerrado")
        return
    DbClientsManager.cadastrar_conta(cliente[0])
    print("Conta criada com sucesso!\n")
    FileManager.create_account(cpf)

def get_current_user_in_contas(current_user, contas):
    for i in enumerate(contas):
        account_check = []
        account_check.append(contas[i[1]]["titular"] == current_user)
        return account_check


def listar_contas_do_usuario(cpf):
    print(DbClientsManager.get_accounts_from_client_cpf(cpf))


def sair(current_user):
    print("Obrigado por usar nosso sistema!")
    current_user = 0
    return current_user


def main(current_user):

    while True:

        opcao = menu()

        if opcao == "d":
            deposito()

        elif opcao == "s":
            saque()

        elif opcao == "e":
            Extrato()

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
# TODO: Refatorar função de login
# logar
# no momento que o login foi feito com sucesso retorna todas as contas do usuario e guarda em uma array
# provavelmente usando a função de listar contas
# checagem dos valores de deposito/saque são feitos em cima dessa array e não consultando direto no banco de dados
