import unicodedata
from abc import ABC, abstractmethod

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

            class Sucesso:
                cadastro_realizado = "\nCadastro realizado com sucesso"
                conta_cadastrada = "\nConta cadastrada com sucesso"

    # Mensagens para saque
    class Saque:
        bem_sucedido = "\nSaque realizado com sucesso"

    # Mensagens para desposito
    class Deposito:
        bem_sucedido = "\nDepósito realizado com sucesso"

    # Mensagens para extrato
    class Extrato:
        sem_movimentacao = "\nNão foram realizadas movimentações"
        saldo_atualizado = "\nO salto atual da conta é"
        consulta = " Extrato ".center(15, '=')

    # Mensagens para Caixa
    class Caixa:
        sair = "\nObrigado por usar nossos serviços"
        desligar = "\nCaixa desligado para manutenção"
        
    # Mensagens para Erro
    class Erro:

        class Conversao:
            numero_invalido = "\nValor inválido, tente novamente\n"

        class Cadastro:
            sem_usuarios = "\nNão há usuários cadastrados no sistema\n"
            sem_conta = "\nNão há contas cadastradas no sistema para este usuário\n"
            entrada_numero = "\nSó é permitido entrada numérica"
            conta_existente = "\nUsuário já cadastrado"
            conta_inexistente = "\nUsuário não encontrado no sistema"
        
        class Entrada:
            cpf_invalido = "\nCPF inválido, tente novamente"
            data_invalida = "\nData inválida, tente novamente"
            campo_vazio = "\nCampo não pode ser vazio"
            numero_incorreto = "\nNúmero inválido, tente novamente"
            cpf_ja_cadastrado = "\nCPF já se encontra cadastrado no sistema"

        class Deposito:
            invalido = "\nValor de deposito inválido, por favor tente novamente"

        class Saque:
            sem_limite = "\nSem limite de saques disponíveis, limite diário é de 3 saques"
            saldo_insuficiente = "\nVocê não possui saldo suficiente para realizar a operação"
            acima_limite = "\nO Limite de saque é de 500, porfavor tente novamente"
            valor_invalido = "\nValor inválido, por favor tente novamente"
            saldo_zerado = "\nVocê não possui saldo em sua conta para saque"

        class Caixa:
            opcao_indisponivel = "\nOpção indisponível, por favor selecione uma opção válida\n"

    class Menu:
        
        titulo = " Caixa Eletrônico "
        
        class Cadastro:
            menu_pricipal = """
    Bem Vindo
    Porfavor escolha uma opção

    1 - Cadastrar nova Pessoa
    2 - Cadastrar novo Usuário
    3 - Cadastrar nova Conta
    4 - Realizar Movimentação

    5 - Sair
            """
        
        class Operacao:
            opcao = """
    Escolha uma operação

    1 - Saque
    2 - Depósito
    3 - Extrato
                    
    4 - Voltar
            """

class Padronizacao:

    # Padronizar opções para padrão unicode sem acentos
    @classmethod
    def Texto (opcao):
        
        if (opcao.isdigit()):
            padronizado = int(opcao)
        
        else:
            padronizar = unicodedata.normalize('NFKD', opcao)
            padronizado = ''.join(c for c in padronizar if not unicodedata.combining(c)).lower()
        
        return padronizado

    # Conversor numérico
    # Converte float Padrão Brasileiro para Internacional
    @classmethod
    def Numero (entrada):

        try:
            padronizado = int(entrada)
            
        except ValueError:

            try:
                padronizado = float(entrada)

            except ValueError:

                try:
                    padronizado = float(entrada.replace(",", "."))

                except ValueError:
                    padronizado = -1

        return padronizado

    # Validação da entrada de CPF
    @classmethod
    def CPF (entrada, usuarios):

        entrada = str(entrada)

        entrada = "".join(filter(str.isdigit, entrada))

        if (len(entrada) == 11 and entrada.isdigit()):

            for usuario in usuarios:

                if (usuario[0][0] == entrada):
                    return -3
                
            return entrada
        
        else:
            return -1

    # Conversor de datas
    @classmethod
    def Data (entrada):

        if len(entrada) == 8 and entrada.isdigit():
            return f"{entrada[:2]}/{entrada[2:4]}/{entrada[4:]}"
        
        else:
            return -1

# Entradas das operações
def entradas_validas (tipo_operacao, tipo, usuarios = ""):

    if tipo_operacao == "movimentacao":

        mensagem = {
            "principal": f"\n{MSG.Menu.titulo.center(30, '#')}\n{MSG.Menu.Operacao.opcao.center(30)}\n>>> ",
            "saque": "\nDigite um valor para sacar\n>>> ",
            "deposito": "\nDigite um valor para depositar\n>>> "
        }

        mensagem = mensagem.get(tipo, "\nDigite um valor\n>>>")

        while True:

            entrada = input(mensagem)

            entrada_convertida = Padronizacao.Numero(entrada)

            if entrada_convertida == -1:
                print(MSG.Erro.Conversao.numero_invalido)

            else:
                return entrada_convertida

    elif tipo_operacao == "cadastro":

        mensagem = {
            "cpf": f"\n{MSG.Usuario.Entrada.Cadastro.cpf}",
            "nome": f"\n{MSG.Usuario.Entrada.Cadastro.nome}",
            "nascimento": f"\n{MSG.Usuario.Entrada.Cadastro.data_nasc}",
            "endereco": f"\n{MSG.Usuario.Entrada.Cadastro.endereco}",
            "numero": f"\n{MSG.Usuario.Entrada.Cadastro.numero}",
            "bairro": f"\n{MSG.Usuario.Entrada.Cadastro.bairro}",
            "estado": f"\n{MSG.Usuario.Entrada.Cadastro.estado}",
            "cidade": f"\n{MSG.Usuario.Entrada.Cadastro.cidade}"
        }

        mensagem = mensagem.get(tipo, "\nDigite um valor\n>>>")

        while True:

            entrada = input(mensagem)

            if (entrada == ""):
                print(MSG.Usuario.Entrada.Erro.campo_vazio)
            
            elif tipo == "cpf":

                entrada = Padronizacao.CPF(entrada, usuarios)

                if (entrada == -1):
                    print(MSG.Erro.Entrada.cpf_invalido)

                elif (entrada == -3):
                    print(MSG.Erro.Entrada.cpf_ja_cadastrado)

                else:
                    return entrada

            elif tipo == "numero":

                entrada = Padronizacao.Numero(entrada)

                if (entrada != -1):
                    return entrada
                
                else:
                    print(MSG.Erro.Entrada.numero_incorreto)

            elif tipo == "nascimento":
                entrada = Padronizacao.data(entrada)

                if (entrada != -1):
                    return entrada
                
                else:
                    print(MSG.Erro.Entrada.data_invalida)

            else:
                entrada = Padronizacao.Texto(entrada)
                return entrada

# Pega a conta do usuário
def pega_conta (usuarios):

    if usuarios == []:
        return  {"error": -1}

    index_usuarios = 0

    while index_usuarios < len(usuarios):

        print(f"{index_usuarios} - {usuarios[index_usuarios][0][1]}")
        index_usuarios += 1

    while True:
        usuario_selecionado = Padronizacao.Numero(input(f"\nQual o usuário deseja acessar?\n>>> "))

        if (usuario_selecionado == "Error"):
            print(MSG.Erro.Entrada.entrada_numero)
        else:
            break

    if len(usuarios[usuario_selecionado]) == 2:
        return {"error": -2}

    try: 
        len(usuarios[usuario_selecionado][2])

    except IndexError:
        return {"error": -2}
    
    for i, lista_contas in enumerate(usuarios[usuario_selecionado][2]):
        print(f"{i} - Conta Número: {lista_contas[1]}")

    while True:
        conta_selecionada = Padronizacao.Numero(input(f"\nQual a conta que será movimentada?\n>>> "))

        if (conta_selecionada == "Error"):
            print(MSG.Erro.Entrada.entrada_numero)

        else:
            return {"conta": conta_selecionada, "usuario": usuario_selecionado}

class Transacao (ABC):

    @abstractmethod
    def Depositar ():
        pass

    @abstractmethod
    def Sacar ():
        pass

class Pessoa_Fisica:
    
    def __init__(self, cpf, nome, data_nascimento):
        self._cpf = cpf # string
        self._nome = nome # string
        self._data_nascimento = data_nascimento # date

class Cliente (Pessoa_Fisica):
    
    def __init__(self, endereco, contas):
        self._endereco = endereco # string
        self._contas = contas # lista

class Conta (Cliente):

    def __init__ (self, saldo, numero, agencia, cliente, historico):
        self._saldo = saldo # float
        self._numero = numero # int
        self._agencia = agencia # str
        self._cliente = cliente
        self._historico = historico

    def Saldo (self):
        pass

    def Nova_Conta (self):
        pass

    def Sacar (self, valor):
        pass

    def Depositar (self, valor):
        pass

class Conta_Corrente (Conta):
    
    def __init__(self, limite, limite_saque):
        self._limite = limite # float
        self._limite_saques = limite_saque # int


class Movimentacao (Conta_Corrente, Transacao):

    def Sacar (self):
        pass

    def Depositar (self):
        pass

class Historico (Movimentacao):

    def Extrato (self):
        pass

def movimentacoes ():
    pass

def main (usuarios, numero_conta):

    if usuarios is None:
        usuarios = []

    while True:

        opcao = input(f"\n{MSG.Menu.titulo.center(30, '#')}\n{MSG.Menu.Cadastro.menu_pricipal}\n>>> ")

        opcao_padronizada = Padronizacao.Texto(opcao)

        if opcao_padronizada == 1:
            dados = Pessoa_Fisica.Cadastrar_Pessoa(usuarios)

        elif opcao_padronizada == 2:
            dados = Conta.Cadastrar_Usuario(usuarios)

            if "lista_usuarios" in dados:
                usuarios = dados["lista_usuarios"]

        elif opcao_padronizada == 3:
            dados = Conta.Cadastrar_Conta(usuarios=usuarios, numero_conta=numero_conta)
            usuarios = dados["lista_usuarios"]
            numero_conta = dados["conta"]

        elif opcao_padronizada == 4:

            dados_conta = pega_conta(usuarios)

            if "error" in dados_conta:

                if dados_conta["error"] == -1:
                    print(MSG.Erro.Cadastro.sem_usuarios)

                else:
                    print(MSG.Erro.Cadastro.sem_conta)
            else:
                usuario = dados_conta["usuario"]
                conta = dados_conta["conta"]
                movimentacoes(limite_diario=usuarios[usuario][2][conta][4], log_extrato=usuarios[usuario][2][conta][3], usuarios=usuarios, usuario=usuario, conta=conta)

        elif opcao_padronizada == "printar":
            print(usuarios)

        elif opcao_padronizada == "printar contas":
            print(usuarios[0][2])

        elif opcao_padronizada == "sair" or opcao_padronizada == 4:
            print(MSG.Caixa.desligar)
            break

        else:
            print(MSG.Erro.Caixa.opcao_indisponivel)