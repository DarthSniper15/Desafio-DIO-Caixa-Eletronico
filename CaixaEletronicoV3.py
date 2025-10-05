import unicodedata
from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

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
                conta = "\nConta será criada para qual usuário?\n>>> "

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
        saldo_atualizado = "\nO salto atual da conta é R$ "
        consulta = " Extrato ".center(30, '=')

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
            conta_existente = "\nUsuário já cadastrado"
            conta_inexistente = "\nUsuário não encontrado no sistema"
            contas_nao_dicio = "\nContas não é um dicionário como esperado"
        
        class Entrada:
            cpf_invalido = "\nCPF inválido, tente novamente"
            data_invalida = "\nData inválida, tente novamente"
            campo_vazio = "\nCampo não pode ser vazio"
            numero_incorreto = "\nNúmero inválido, tente novamente"
            cpf_ja_cadastrado = "\nCPF já se encontra cadastrado no sistema"
            entrada_numero = "\nSó é permitido entrada numérica"

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

        class Movimentacao:
            usuario_nao_encontrado = "\nUsuário não encontrado, tente novamente"
            conta_nao_encontrada = "\nConta não encontrada, tente novamente\n"

    class Menu:
        
        titulo = " Caixa Eletrônico ".center(30, '#')
        
        class Cadastro:
            menu_pricipal = textwrap.dedent("""
                Bem Vindo
                Porfavor escolha uma opção

                1 - Cadastrar nova Usuário
                2 - Cadastrar nova Conta
                3 - Realizar Movimentação

                4 - Sair
                """)
        
        class Operacao:
            opcao = textwrap.dedent("""
                Escolha uma operação

                1 - Sacar
                2 - Depósitar
                3 - Tirar Extrato
                4 - Verificar Saldo
                                
                5 - Voltar
                        """)

class Padronizacao:

    # Padronizar opções para padrão unicode sem acentos
    def Texto (opcao):
        
        if (opcao.isdigit()):
            padronizado = int(opcao)
        
        else:
            padronizar = unicodedata.normalize('NFKD', opcao)
            padronizado = ''.join(c for c in padronizar if not unicodedata.combining(c)).lower()
        
        return padronizado

    # Conversor numérico
    # Converte float Padrão Brasileiro para Internacional
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
    def CPF (entrada, usuarios):
        entrada = str(entrada)
        entrada = "".join(filter(str.isdigit, entrada))
        if (len(entrada) == 11 and entrada.isdigit()):
            for i, (chave, lista_de_usuarios) in enumerate(usuarios.items()):
                if (lista_de_usuarios["usuario"].cpf == entrada):
                    return -3                
            return entrada        
        else:
            return -1

    # Conversor de datas
    def Data (entrada):

        if len(entrada) == 8 and entrada.isdigit():
            return f"{entrada[:2]}/{entrada[2:4]}/{entrada[4:]}"
        
        else:
            return -1

# Entradas das operações
def entradas_validas (tipo_operacao, tipo, usuarios = ""):

    if tipo_operacao == "movimentacao":

        mensagem = {
            "principal": f"\n{MSG.Menu.titulo}\n{MSG.Menu.Operacao.opcao}\n>>> ",
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
                print(MSG.Erro.Entrada.campo_vazio)
            
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
                entrada = Padronizacao.Data(entrada)

                if (entrada != -1):
                    return entrada
                
                else:
                    print(MSG.Erro.Entrada.data_invalida)

            else:
                entrada = Padronizacao.Texto(entrada)
                return entrada

class Cliente:
    
    def __init__(self, endereco):
        self._endereco = endereco # string
        self._contas = [] # lista

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)
    
    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas

class Pessoa_Fisica(Cliente):    
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def nascimento(self):
        return self._data_nascimento

class Conta:

    def __init__(self, numero, cliente):
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    def Consultar_Saldo(self):
        print(f"{MSG.Extrato.saldo_atualizado}{self._saldo}")

    @classmethod
    def Nova_Conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def Sacar (self, valor):
        if (self.limite_saque == 0):
            print(MSG.Erro.Saque.sem_limite)
            return False
        if (valor == "Error"):
            print(MSG.Erro.Conversao.numero_invalido)
            return False
        elif (self.saldo == 0):
            print(MSG.Erro.Saque.saldo_zerado)
            return False
        elif (valor > self.limite):
            print(MSG.Erro.Saque.acima_limite)
            return False
        elif (valor > self.saldo):
            print(MSG.Erro.Saque.saldo_insuficiente)
            return False
        elif (valor < 0):
            print(MSG.Erro.Saque.valor_invalido)
            return False
        else:
            self._saldo -= valor
            self._limite_saques -= 1
            print(MSG.Saque.bem_sucedido)
            return True

    def Depositar (self, valor):
        if (valor == "Error"):
            print(MSG.Erro.Conversao.numero_invalido)
            return False
        elif (valor <= 0):
            print(MSG.Erro.Deposito.invalido)
            return False
        else:
            self._saldo += valor
            print(MSG.Deposito.bem_sucedido)
            return True


class Conta_Corrente(Conta):
    
    def __init__(self, numero, cliente, limite = 500, limite_saque = 3, saldo = 0):
        super().__init__(numero, cliente)
        self._limite = limite # float
        self._limite_saques = limite_saque # int
        self._saldo = saldo

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saque(self):
        return self._limite_saques
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def extrato(self):
        mensagem = []
        for i, transacoes in enumerate(self._transacoes):
            mensagem.append(textwrap.dedent(f"""
                Tipo de Transação: {transacoes["tipo"]}
                Valor: R$ {transacoes["valor"]}
                Data da Movimentação:{transacoes["data"]}
                """))
        if mensagem == []:
            mensagem = MSG.Extrato.sem_movimentacao
            return {"sem_movimentacao": mensagem}
        else:
            return {"com_movimentacao": mensagem}

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.Depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.Sacar(self.valor)

        if sucesso_transacao:
            print(MSG.Saque.bem_sucedido)
            conta.historico.adicionar_transacao(self)

# Variaveis
usuarios = {}
numero_conta = 0

def cadastrar_usuario (usuarios):
    endereco = {}
    
    if usuarios is None:
        usuarios = []

    # Dados do usuario
    cpf = (entradas_validas("cadastro", "cpf", usuarios))
    nome = (entradas_validas("cadastro", "nome"))
    data_nascimento = (entradas_validas("cadastro", "nascimento"))
    # Dados do endereço completo 
    logradouro = (entradas_validas("cadastro", "endereco"))
    numero = (entradas_validas("cadastro", "numero"))
    bairro = (entradas_validas("cadastro", "bairro"))
    estado = (entradas_validas("cadastro", "estado"))
    cidade = (entradas_validas("cadastro", "cidade"))
    endereco[cidade] = {
        "logradouro": logradouro,
        "numero": numero,
        "bairro": bairro,
        "estado": estado,
    }
    # Integra os dados no dicionário do sistema
    usuarios[cpf] = {
        "usuario": Pessoa_Fisica(cpf, nome, data_nascimento, endereco)
    }
    print(MSG.Usuario.Entrada.Sucesso.cadastro_realizado)
    return {"lista_usuarios": usuarios}

# Entradas para criação de conta
def cadastrar_conta(usuarios, numero_conta):
    numero_conta += 1

    if usuarios == {}:
        # Erro -1 = não há usuários cadastrados no sistema
        return  {"error": -1}

    while True:
        # Imprime na tela todos os usuários no sistema
        lista_cpf = []
        
        for i, (chave, lista_de_usuarios) in enumerate(usuarios.items()):
            print(f"{i} - {lista_de_usuarios["usuario"].nome}")
            lista_cpf.append(chave)
        
        conta_usuario = Padronizacao.Numero(input(MSG.Usuario.Entrada.Cadastro.conta))
        cpf = lista_cpf[conta_usuario]
        
        for i, (chave, lista_de_usuarios) in enumerate(usuarios.items()):
            
            if lista_de_usuarios["usuario"].cpf == cpf:
                index_usuario = i
                break
            else:
                index_usuario = None
        
        if index_usuario is not None:
            nova_conta = str(numero_conta).zfill(10)
            contacc = Conta_Corrente.Nova_Conta(usuarios[cpf]["usuario"], nova_conta)
            usuarios[cpf]["usuario"].adicionar_conta(contacc)
            break
        else:
            print(MSG.Erro.Cadastro.conta_inexistente)
    print(MSG.Usuario.Entrada.Sucesso.conta_cadastrada)
    return {"lista_usuarios": usuarios, "conta": numero_conta}

# Pega a conta do usuário
def pega_conta (usuarios):
    lista_cpf = []
    lista_contas = []

    if usuarios == {}:
        # Erro -1 = não há usuários cadastrados no sistema
        return  {"error": -1}
    
    for i, (chave, lista_usuarios) in enumerate(usuarios.items()):
        print(f"{i} - {lista_usuarios['usuario'].nome}")
        lista_cpf.append(chave)

    while True:
        usuario_selecionado = Padronizacao.Numero(input(f"\nQual o usuário deseja acessar?\n>>> "))
        
        if (0 <= usuario_selecionado < len(lista_cpf)):
            cpf = lista_cpf[usuario_selecionado]
            break

        elif (usuario_selecionado == "Error"):
            print(MSG.Erro.Entrada.entrada_numero)

        else:
            print(MSG.Erro.Movimentacao.usuario_nao_encontrado)
            

    if Pessoa_Fisica.contas == []:
        # Erro -2 = Não há contas cadastradas para o usuário
        return {"error": -2}
    
    for i, numero_contas in enumerate(usuarios[cpf]["usuario"].contas):
        print(f"{i} - Conta Número: {numero_contas.numero}")
        lista_contas.append(numero_contas)
    
    while True:
        conta_selecionada = Padronizacao.Numero(input(f"\nQual a conta que será movimentada?\n>>> "))
        
        if (0 <= conta_selecionada < len(lista_contas)):
            conta = lista_contas[conta_selecionada]
            return {"conta": conta, "dados_conta": usuarios[cpf]["usuario"].contas[conta_selecionada].numero, "usuario": cpf}

        elif (conta_selecionada == "Error"):
            print(MSG.Erro.Entrada.entrada_numero)

        else:
            print(MSG.Erro.Movimentacao.conta_nao_encontrada)
            

def movimentacao (*, usuario, conta):
    
    print(conta)

    transacao = None

    while True:
        opcao = Padronizacao.Numero(entradas_validas("movimentacao", "principal"))

        if opcao == "saque" or opcao == 1:
            valor = entradas_validas("movimentacao", "saque")
            transacao = Saque(valor)
            Cliente.realizar_transacao(usuario, conta, transacao)

        elif opcao == "deposito" or opcao == 2:
            valor = entradas_validas("movimentacao", "deposito")
            transacao = Deposito(valor)
            Cliente.realizar_transacao(usuario, conta, transacao)

        elif opcao == "extrato" or opcao == 3:
            if "sem_movimentacao" in conta.historico.extrato:
                print(conta.historico.extrato["sem_movimentacao"])
            else:
                print(MSG.Extrato.consulta)
                for i, extrato in enumerate(conta.historico.extrato["com_movimentacao"]):
                    print(extrato)

        elif opcao == "saldo" or opcao == 4:
            print(f"{MSG.Extrato.saldo_atualizado}{conta.saldo}")

        elif opcao == "voltar" or opcao == 5:
            print(MSG.Caixa.sair)
            break

        else:
            print(MSG.Erro.Caixa.opcao_indisponivel)


def main (usuarios, numero_conta): 
    while True:
        opcao = Padronizacao.Texto(input(f"\n{MSG.Menu.titulo}\n{MSG.Menu.Cadastro.menu_pricipal}\n>>> "))
        
        if(opcao == 1):
            dados_conta = cadastrar_usuario(usuarios)

            if "error" in dados_conta:
                print(MSG.Erro.Cadastro.sem_usuarios)
        
        elif (opcao == 2):
            dados = cadastrar_conta(usuarios, numero_conta)
            if "error" in dados:
                print(MSG.Erro.Cadastro.sem_usuarios)
            else:                
                numero_conta = dados["conta"]
        
        elif (opcao == 3):
            dados_conta = pega_conta(usuarios)
            if "error" in dados_conta:
                if dados_conta["error"] == -1:
                    print(MSG.Erro.Cadastro.sem_usuarios)
                else:
                    print(MSG.Erro.Cadastro.sem_conta)
            else:
                usuario = dados_conta["usuario"]
                conta = dados_conta["conta"]
                movimentacao(usuario=usuario, conta=conta)
        elif (opcao == "printar"):
            print(usuarios)        
        elif (opcao == 4):
            print(MSG.Caixa.desligar)
            break        
        else:
            print(MSG.Erro.Caixa.opcao_indisponivel)

if __name__ == "__main__":
    main(usuarios, numero_conta)