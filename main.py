import datetime
import textwrap

from Cliente import Cliente
from ContaCorrente import ContaCorrente
from ContaIterator import ContaIterator
from Deposito import Deposito
from PessoaFisica import PessoaFisica
from Saque import Saque
from FileManager import FileManager


FileManager.checkfiles()


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
        funcao(*args, **kwargs)
        current_time = datetime.datetime.now()
        formated_time = current_time.strftime('%d-%m-%Y %H:%M:%S')
        print("=" * 100)
        print(f"Operação de {funcao.__name__}, executada as: {formated_time}")

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
def login(usuarios):
    try:
        attemp_user = input('digite seu cpf: \n')
        temp_dict = usuarios.__getitem__(attemp_user)
        if (temp_dict.__getitem__("senha") == input("digite a senha: \n")):
            return attemp_user
        else:
            print("usuario ou senha incorretos")
            login(usuarios)
    except KeyError:
        print("Usuário não existe")
        login(usuarios)


#  função responsavel por retornar prieiro cliente com o cpf passado
def filtrar_contas(cpf, clientes):
    filtro = [cliente for cliente in clientes if cliente._cpf == cpf]
    return filtro[0] if filtro else None
    # se cpf do cliente esta na variavel clientes retorne verdadeiro, caso não volte falso.


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
def criar_cliente(clientes):
    cpf = input("informe o cpf do cliente(somente numeros)")

    cliente = filtrar_contas(cpf, clientes)

    if cliente:
        print("já existe um cliente com este cpf!")
    nome = input("digite o nome completo")
    data_nascimento = input("digite a data de nascimento (dia-mes-ano)")
    endereco = input("digite seu endereço(logradouro, nro - bairro - cidade/estado)")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n Cliente criado com sucesso!")


def criar_conta(numero_da_conta, clientes, contas):
    cpf = input("Digite o cpf do cliente: \n")
    cliente = filtrar_contas(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!, fluxo de criação encerrado")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_da_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("Conta criada com sucesso!\n")


def get_current_user_in_contas(current_user, contas):
    for i in enumerate(contas):
        account_check = []
        account_check.append(contas[i[1]]["titular"] == current_user)
        return account_check


def listar_contas_do_usuario(contas):
    for conta in ContaIterator(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def sair(current_user):
    print("Obrigado por usar nosso sistema!")
    current_user = 0
    return current_user


def main():
    clientes = []
    contas = []
    numero_da_conta = 0

    while True:

        opcao = menu()

        if opcao == "d":
            deposito(clientes)

        elif opcao == "s":
            saque(clientes)

        elif opcao == "e":
            Extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_da_conta = len(contas) + 1
            criar_conta(numero_da_conta, clientes, contas)

        elif opcao == "l":
            listar_contas_do_usuario(contas)

        elif opcao == "q":
            break

        else:
            print("A opção escolhida não é compatível, por favor selecione uma opção disponivel no menu.")


# RFE: função de login, a ser apresentada antes de liberar menu principal.
def init(usuarios, contas, current_user, contas_no_banco):
    init_option = init_menu()

    if (init_option == "1" and current_user != "0"):
        current_user = login(usuarios)
        usuarios, contas, current_user, contas_no_banco = routine(usuarios, contas, current_user, contas_no_banco)


    elif (init_option == "2"):
        usuarios, current_user = criar_usuario(usuarios)
        current_user = login(usuarios)
        usuarios, contas, current_user, contas_no_banco = routine(usuarios, contas, current_user, contas_no_banco)

    elif (init_option == "10"):
        print("delisgando sistema")
        return usuarios, contas, current_user, contas_no_banco

    elif (init_option == "12"):
        for i in enumerate(contas):
            print(
                f"numero da conta: {contas[i[1]]['numero_da_conta']}, nome do titular: {contas[i[1]]['nome']}, agencia da conta: {contas[i[1]]['agencia']}, saldo: {contas[i[1]]['saldo']}")
            init(usuarios, contas, current_user, contas_no_banco)

    else:
        print("desculpe, a opção que escolheu não é valida")
    init(usuarios, contas, current_user, contas_no_banco)


main()

# TODO: realizar limpeza no codigo
# TODO: Refatorar função de login

