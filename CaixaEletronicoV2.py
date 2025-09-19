'''
Função Saque
argumentos apenas por nome
função (saque: saque)

Função Depósito
argumentos apenas por posição

Função Extrato
argumentos por nome e posição
posicional: saldo
nomeado: extrato

================

Novas funções

Função criar usuário
em lista com nome, data nascimento, cpf e endereço(string com logradouro[,nº] - bairro - cidade/sigla estado)
cpf somente número
não é possível cadastrar 2 cpf

Função criar conta
em lista com agencia, numero conta e usuario
numero conta é sequencial, numero agencia fixo em 0001
usuario pode ter multiplas contas
uma conta pertence somente a um usuário
contas necessitam de um usuário


Funções em estudo
            3 - Listar Contas
            4 - Listar Usuários
            5 - Excluir Conta
            6 - Excluir Usuário
'''

import unicodedata

# Padronizar opções para padrão unicode sem acentos
def padroniza(opcao):
    if (opcao.isdigit()):
        padronizado = int(opcao)
    else:
        padronizar = unicodedata.normalize('NFKD', opcao)
        padronizado = ''.join(c for c in padronizar if not unicodedata.combining(c)).lower()
    return padronizado

# Conversor para float Padrão Brasileiro pra Internacional
def converte_float(numero):

    try:
        padronizado = float(numero)

    except ValueError:

        try:
            padronizado = float(numero.replace(",", "."))

        except ValueError:
            padronizado = "Error"

    return padronizado

def entrada_numerica(entrada):

    try:
        padronizado = int(entrada)
        
    except ValueError:
        try:
            padronizado = float(entrada)

        except ValueError:

            try:
                padronizado = float(entrada.replace(",", "."))

            except ValueError:
                padronizado = "Error"

    return padronizado

# Mensagens para operações
class MSG:

    class Usuario:
        class Entrada:
            class Cadastro:
                nome = "\nInforme seu Nome\n>>> "
                cpf = "\nInforme seu CPF | Somente números\n>>> "
                endereco = "\nInforme seu endereço\n>>> "
                numero = "\nInforme o número da residencia\n>>> "
                bairro = "\nInforme seu bairro\n>>> "
                estado = "\nInforme seu Estado\n>>> "
                cidade = "\nInforme sua cidade\n>>> "
                data_nasc = "\nInforme sua data de nascimento\n>>> "
        class Erro:
            conta_existente = "\nUsuário já cadastrado"
            conta_inexistente = "\nUsuário não encontrado no sistema"
    
    # Mensagens para saque
    class Saque:
        bem_sucedido = "\nSaque realizado com sucesso"

        class Erro:
            sem_limite = "\nSem limite de saques disponíveis, limite diário é de 3 saques"
            saldo_insuficiente = "\nVocê não possui saldo suficiente para realizar a operação"
            acima_limite = "\nO Limite de saque é de 500, porfavor tente novamente"
            valor_invalido = "\nValor inválido, por favor tente novamente"
            saldo_zerado = "\nVocê não possui saldo em sua conta para saque"

    # Mensagens para desposito
    class Deposito:
        bem_sucedido = "\nDepósito realizado com sucesso"

        class Erro:
            invalido = "\nValor de deposito inválido, por favor tente novamente"

    # Mensagens para extrato
    class Extrato:
        sem_movimentacao = "\nNão foram realizadas movimentações"
        saldo_atualizado = "\nO salto atual da conta é"
        consulta = " Extrato ".center(15, '=')

    # Mensagens para Caixa
    class Caixa:
        sair = "\nObrigado por usar nossos serviços"
        
        class Erro:
            opcao_indisponivel = "\nOpção indisponível, por favor selecione uma opção válida\n"
    
    # Mensagens para erro geral
    class Erro:
        conversao = "\nValor inválido, tente novamente\n"
        sem_usuarios = "\nNão há usuários cadastrados no sistema\n"
        sem_conta = "\nNão há contas cadastradas no sistema para este usuário\n"
        entrada_numero = "\nSó é permitido entrada numérica"

    class Menu:
        titulo = " Caixa Eletrônico "
        class Cadastro:
            menu_pricipal = """
    Bem Vindo
    Porfavor escolha uma opção

    1 - Cadastrar novo Usuário
    2 - Cadastrar nova Conta
    3 - Realizar Movimentação

    4 - Sair
            """
        class Operacao:
            opcao = """
    Escolha uma operação

    1 - Saque
    2 - Depósito
    3 - Extrato
                    
    4 - Voltar
            """

# Variáveis
opcao = 0
usuarios = None
numero_conta = 0
agencia = "0001"
saldo = 0
consulta_extrato = None
limite_saques = 3
limite_diario = 500


# Entradas das operações
def entradas_operacao (tipo):

    mensagem = {
        "principal": f"\n{MSG.Menu.titulo.center(30, '#')}\n{MSG.Menu.Operacao.opcao.center(30)}\n>>> ",
        "saque": "\nDigite um valor para sacar\n>>> ",
        "deposito": "\nDigite um valor para depositar\n>>> "
    }

    mensagem = mensagem.get(tipo, "\nDigite um valor\n>>>")
    entrada = input(mensagem)

    if tipo in ["saque", "deposito"]:
        entrada = converte_float(entrada)

    return entrada

def pega_conta (usuarios):

    if usuarios == []:
        return -1
    
    if len(usuarios) == 2:
        return -2

    index_usuarios = 0

    while index_usuarios < len(usuarios):

        print(f"{index_usuarios} - {usuarios[index_usuarios][0][1]}")
        index_usuarios += 1

    while True:
        usuario_selecionado = entrada_numerica(input(f"\nQual o usuário deseja acessar?\n>>> "))

        if (usuario_selecionado == "Error"):
            print(MSG.Erro.entrada_numero)
        else:
            break

    try: 
        len(usuarios[usuario_selecionado][2])

    except IndexError:
        return -2
    
    for i, lista_contas in enumerate(usuarios[usuario_selecionado][2]):
        print(f"{i} - Conta Número: {lista_contas[1]}")

    while True:
        conta_selecionada = entrada_numerica(input(f"\nQual a conta que será movimentada?\n>>> "))

        if (conta_selecionada == "Error"):
            print(MSG.Erro.entrada_numero)
        else:
            break

    return {"conta": conta_selecionada, "usuario": usuario_selecionado}

# Operações bancárias
def main (usuarios, limite_saque, limite_diario, saldo, log_extrato, numero_conta):

    if usuarios is None:
        usuarios = []

    while True:

        opcao = input(f"\n{MSG.Menu.titulo.center(30, '#')}\n{MSG.Menu.Cadastro.menu_pricipal}\n>>> ")

        opcao_padronizada = padroniza(opcao)

        if opcao_padronizada == 1:
            dados = cadastrar_usuario(usuarios)
            if "lista_usuarios" in dados:
                usuarios = dados["lista_usuarios"]

        elif opcao_padronizada == 2:
            dados = cadastrar_conta(usuarios=usuarios, numero_conta=numero_conta)
            usuarios = dados["lista_usuarios"]
            numero_conta = dados["conta"]

        elif opcao_padronizada == 3:    
            dados_conta = pega_conta(usuarios)
            usuario = dados_conta["usuario"]
            conta = dados_conta["conta"]
            movimentacoes(limite_saque=limite_saque, limite_diario=limite_diario, saldo=usuarios[usuario][2][conta][2], log_extrato=usuarios[usuario][2][conta][3], usuarios=usuarios, usuario=usuario, conta=conta)

        elif opcao_padronizada == "printar":
            print(usuarios)

        elif opcao_padronizada == "printar contas":
            print(usuarios[0][2])

        elif opcao_padronizada == "sair" or opcao_padronizada == 4:
            print(MSG.Caixa.sair)
            break

        else:
            print(MSG.Caixa.Erro.opcao_indisponivel)

def movimentacoes (*, limite_saque, limite_diario, saldo, log_extrato, usuarios, usuario, conta):

    if conta == -1:
        print(MSG.Erro.sem_usuarios)
        return -1
    
    elif conta == -2:
        print(MSG.Erro.sem_conta)
        return -1

    if (log_extrato is None):
        log_extrato = []

    print(f"\nUsuário logado: {usuarios[usuario][0][1]}")

    while True:
        opcao = padroniza(entradas_operacao("principal"))

        if opcao == "saque" or opcao == 1:
            dados = saque(limite_saque=limite_saque, saldo=usuarios[usuario][2][conta][2], limite_diario=limite_diario, usuarios=usuarios, usuario=usuario, conta=conta)
            limite_saque = dados["limite_saques"]
            usuarios[usuario][2][conta][2] = dados["saldo"]


        elif opcao == "deposito" or opcao == 2:
            #(saldo | extrato)
            dados = deposito(usuarios[usuario][2][conta][2], usuarios, usuario, conta)
            usuarios[usuario][2][conta][2] = dados["saldo"]


        elif opcao == "extrato" or opcao == 3:
            dados = extrato(usuarios[usuario][2][conta][3], saldo=usuarios[usuario][2][conta][2])

        elif opcao == "voltar" or opcao == 4:
            print(MSG.Caixa.sair)
            break

        else:
            print(MSG.Caixa.Erro.opcao_indisponivel)

'''
Entradas para criação de usuário
estrutura usuario [pessoa, endereco]
estrutura pessoa [cpf, nome, data nascimento]
estrutura endereco [endereco, numero, bairro, estado, cidade]
estrutura de acesso usuarios[usuario][dado da pessoa][dado do endereco]
'''
def cadastrar_usuario (usuarios):

    endereco = []
    pessoa = []

    if usuarios is None:
        usuarios = []

    pessoa.append(input(MSG.Usuario.Entrada.Cadastro.cpf))
    pessoa.append(input(MSG.Usuario.Entrada.Cadastro.nome))
    pessoa.append(input(MSG.Usuario.Entrada.Cadastro.data_nasc))
    endereco.append(input(MSG.Usuario.Entrada.Cadastro.endereco))
    endereco.append(input(MSG.Usuario.Entrada.Cadastro.numero))
    endereco.append(input(MSG.Usuario.Entrada.Cadastro.bairro))
    endereco.append(input(MSG.Usuario.Entrada.Cadastro.estado))
    endereco.append(input(MSG.Usuario.Entrada.Cadastro.cidade))
    usuarios.append([pessoa, endereco])

    return {"lista_usuarios": usuarios}

# Entradas para criação de conta
def cadastrar_conta (*, usuarios, numero_conta):

    numero_conta += 1

    while True:

        cpf = input("\nConta será criada para qual usuário?\nDigite o CPF | Somente número\n>>> ")

        for i, usuario in enumerate(usuarios):
            if usuario[0][0] == cpf:
                index_usuario = i
                break
            else:
                index_usuario = None

        if index_usuario is not None:
            nova_conta = ["0001", str(numero_conta).zfill(10), 0.0, []]

            if len(usuarios[index_usuario]) < 3:
                usuarios[index_usuario].append([nova_conta])  # inicia lista de contas

            else:
                usuarios[index_usuario][2].append(nova_conta)  # adiciona nova conta

            break

        else:
            print(MSG.Usuario.Erro.conta_inexistente)

    return {"lista_usuarios": usuarios, "conta": numero_conta}

# Código para saque
def saque (*, limite_saque, saldo, limite_diario, usuarios, usuario, conta):

    while True:

        if (limite_saque == 0):
            print(MSG.Saque.Erro.sem_limite)
            break

        valor_sacado = entradas_operacao("saque")

        if (valor_sacado == "Error"):
            print(MSG.Erro.conversao)
        
        elif (saldo == 0):
            print(MSG.Saque.Erro.saldo_zerado)
            break

        elif (valor_sacado > limite_diario):
            print(MSG.Saque.Erro.acima_limite)
        
        elif (valor_sacado > saldo):
            print(MSG.Saque.Erro.saldo_insuficiente)

        elif (valor_sacado < 0):
            print(MSG.Saque.Erro.valor_invalido)

        else: 
            saldo-= valor_sacado
            limite_saque-= 1            
            usuarios[usuario][2][conta][3].append(f"-R$ {valor_sacado:.2f}")
            print(MSG.Saque.bem_sucedido)
            break

    return {"saldo": saldo, "limite_saques": limite_saque}

# Código para depósito
def deposito (saldo, usuarios, usuario, conta):

    while True:

        valor_depositado = entradas_operacao("deposito")

        if (valor_depositado == "Error"):
            print(MSG.Erro.conversao)

        elif (valor_depositado <= 0):
            print(MSG.Deposito.Erro.invalido)

        else:
            saldo += valor_depositado
            usuarios[usuario][2][conta][3].append(f"+R$ {valor_depositado:.2f}")
            break

    print(MSG.Deposito.bem_sucedido)
    return {"saldo": saldo}

# Código para consultar extrato
def extrato (log_extrato, *, saldo):
    if (len(log_extrato) == 0):
        print(MSG.Extrato.sem_movimentacao)

    else: 
        print(f"\n {MSG.Extrato.consulta}\n")

        for movimentacao in log_extrato:
            print(movimentacao)

        print(f"{MSG.Extrato.saldo_atualizado} R$ {saldo:.2f}")

    return {"consulta_extrato": log_extrato}

# Inicia o programa
main(usuarios, limite_saques, limite_diario, saldo, consulta_extrato, numero_conta)
