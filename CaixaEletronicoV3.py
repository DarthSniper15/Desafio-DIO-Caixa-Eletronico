import unicodedata

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

class Conta:

    def __init__(self):
        pass

    def Cadastrar_Usuario (self, usuarios):
            
        endereco = []
        pessoa = []

        if usuarios is None:
            usuarios = []

        # Cria uma lista temporária da pessoa
        pessoa.append(entradas_validas("cadastro", "cpf", usuarios))
        pessoa.append(entradas_validas("cadastro", "nome"))
        pessoa.append(entradas_validas("cadastro", "nascimento"))

        # Cria uma lista temporária de endereço
        endereco.append(entradas_validas("cadastro", "endereco"))
        endereco.append(entradas_validas("cadastro", "numero"))
        endereco.append(entradas_validas("cadastro", "bairro"))
        endereco.append(entradas_validas("cadastro", "estado"))
        endereco.append(entradas_validas("cadastro", "cidade"))

        # Integra ambas as listas temporárias na lista do sistema
        usuarios.append([pessoa, endereco])

        print(MSG.Usuario.Entrada.Sucesso.cadastro_realizado)

        return {"lista_usuarios": usuarios}

    def Cadastrar_Conta (self, usuarios, numero_conta):
        numero_conta += 1

        while True:

            # Imprime na tela todos os usuários no sistema
            for i, usuario in enumerate(usuarios):
                print(f"{i} - {usuario[0][0]}")

            conta_usuario = Padronizacao.Texto(input("\nConta será criada para qual usuário?\n>>> "))

            cpf = usuarios[conta_usuario][0][0]

            for i, usuario in enumerate(usuarios):

                if usuario[0][0] == cpf:
                    index_usuario = i
                    break

                else:
                    index_usuario = None

            if index_usuario is not None:
                # conta = [agencia, numero conta, saldo, extrato, limite diario, limite saque]
                nova_conta = ["0001", str(numero_conta).zfill(10), 0.0, [], 500, 3]

                if len(usuarios[index_usuario]) < 3:
                    usuarios[index_usuario].append([nova_conta])  # inicia lista de contas

                else:
                    usuarios[index_usuario][2].append(nova_conta)  # adiciona nova conta

                break

            else:
                print(MSG.Erro.Cadastro.conta_inexistente)

        print(MSG.Usuario.Entrada.Sucesso.conta_cadastrada)

        return {"lista_usuarios": usuarios, "conta": numero_conta}

    def Saque (self, *, limite_saque, saldo, limite_diario, usuarios, usuario, conta):
            
        while True:

            if (limite_saque == 0):
                print(MSG.Erro.Saque.sem_limite)
                break

            valor_sacado = entradas_validas("movimentacao", "saque")

            if (valor_sacado == "Error"):
                print(MSG.Erro.Conversao.numero_invalido)
            
            elif (saldo == 0):
                print(MSG.Erro.Saque.saldo_zerado)
                break

            elif (valor_sacado > limite_diario):
                print(MSG.Erro.Saque.acima_limite)
            
            elif (valor_sacado > saldo):
                print(MSG.Erro.Saque.saldo_insuficiente)

            elif (valor_sacado < 0):
                print(MSG.Erro.Saque.valor_invalido)

            else: 
                saldo-= valor_sacado
                limite_saque-= 1            
                usuarios[usuario][2][conta][3].append(f"-R$ {valor_sacado:.2f}")
                print(MSG.Saque.bem_sucedido)
                break

        return {"saldo": saldo, "limite_saques": limite_saque}

    def Deposito (self, saldo, usuarios, usuario, conta):
            
        while True:

            valor_depositado = entradas_validas("movimentacao", "deposito")

            if (valor_depositado == "Error"):
                print(MSG.Erro.Conversao.numero_invalido)

            elif (valor_depositado <= 0):
                print(MSG.Erro.Deposito.invalido)

            else:
                saldo += valor_depositado
                usuarios[usuario][2][conta][3].append(f"+R$ {valor_depositado:.2f}")
                break

        print(MSG.Deposito.bem_sucedido)
        return {"saldo": saldo}

    def Extrato (self, log_extrato, *, saldo):
        
        if (len(log_extrato) == 0):
            print(MSG.Extrato.sem_movimentacao)

        else: 
            print(f"\n {MSG.Extrato.consulta}\n")

            for movimentacao in log_extrato:
                print(movimentacao)

            print(f"{MSG.Extrato.saldo_atualizado} R$ {saldo:.2f}")

        return {"consulta_extrato": log_extrato}