'''
Deposito somente número positivo

Saques 3 por dia e limitado a 500 por operação

Extrato todas as movimentações realizadas na conta
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

# Mensagens para operações
class MSG:
    
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

# Variáveis
opcao = 0

class Conta:
    saldo = 0    
    consulta_extrato=None
    class Limite: 
        saques = 3
        diario = 500

class Menu:
    titulo = " Caixa Eletrônico "
    opcao = """
    Escolha uma operação
 
    1 - Saque
    2 - Depósito
    3 - Extrato
        
    4 - Sair
    """

def entradas (tipo):

    mensagem = {
        "principal": f"\n{Menu.titulo.center(30, '#')}\n{Menu.opcao.center(30)}\n>>> ",
        "saque": "\nDigite um valor para sacar\n>>> ",
        "deposito": "\nDigite um valor para depositar\n>>> "
    }

    mensagem = mensagem.get(tipo, "\nDigite um valor\n>>>")
    entrada = input(mensagem)

    if tipo in ["saque", "deposito"]:
        entrada = converte_float(entrada)

    return entrada


# Operações bancárias
def main ():

    operacoes = {
        1: saque,
        "sacar": saque,
        2: deposito,
        "depositar": deposito,
        3: extrato,
        "extrato": extrato
    }

    if (Conta.consulta_extrato is None):
        Conta.consulta_extrato = []

    while True:
    
        opcao = entradas("principal")

        opcao_padronizada = padroniza(opcao)

        if opcao_padronizada in operacoes:
            dados = operacoes[opcao_padronizada]()
            Conta.consulta_extrato = dados["consulta_extrato"]
            if "saldo" in dados:
                Conta.saldo = dados["saldo"]
            if "limite_saques" in dados:
                Conta.Limite.saques = dados["limite_saques"]
        elif opcao_padronizada == "sair" or opcao_padronizada == 4:
            print(MSG.Caixa.sair)
            break
        else:
            print(MSG.Caixa.Erro.opcao_indisponivel)


# Código para saque
def saque ():

    while True:

        if (Conta.Limite.saques == 0):
            print(MSG.Saque.Erro.sem_limite)
            break

        valor_sacado = entradas("saque")

        if (valor_sacado == "Error"):
            print(MSG.Erro.conversao)
        
        elif (Conta.saldo == 0):
            print(MSG.Saque.Erro.saldo_zerado)
            break

        elif (valor_sacado > Conta.Limite.diario):
            print(MSG.Saque.Erro.acima_limite)
        
        elif (valor_sacado > Conta.saldo):
            print(MSG.Saque.Erro.saldo_insuficiente)

        elif (valor_sacado < 0):
            print(MSG.Saque.Erro.valor_invalido)

        else: 
            Conta.saldo-= valor_sacado
            Conta.Limite.saques-= 1
            Conta.consulta_extrato.append(f"-R$ {valor_sacado:.2f}")
            print(MSG.Saque.bem_sucedido)
            break

    return {"saldo": Conta.saldo, "consulta_extrato": Conta.consulta_extrato, "limite_saques": Conta.Limite.saques}

# Código para depósito
def deposito ():

    while True:

        valor_depositado = entradas("deposito")

        if (valor_depositado == "Error"):
            print(MSG.Erro.conversao)

        elif (valor_depositado <= 0):
            print(MSG.Deposito.Erro.invalido)

        else:
            Conta.saldo+= valor_depositado
            Conta.consulta_extrato.append(f"+R$ {valor_depositado:.2f}")
            break

    print(MSG.Deposito.bem_sucedido)
    return {"saldo": Conta.saldo, "consulta_extrato": Conta.consulta_extrato}

# Código para consultar extrato
def extrato ():
    if (len(Conta.consulta_extrato) == 0):
        print(MSG.Extrato.sem_movimentacao)

    else: 
        print(f"\n {MSG.Extrato.consulta}\n")

        for movimentacao in Conta.consulta_extrato:
            print(movimentacao)

        print(f"{MSG.Extrato.saldo_atualizado} R$ {Conta.saldo:.2f}")

    return {"consulta_extrato": Conta.consulta_extrato}

# Inicia o programa
main()
