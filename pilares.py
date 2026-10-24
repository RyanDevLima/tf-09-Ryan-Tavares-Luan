from abc import ABC, abstractmethod

class Medivel(ABC):
    """
    Interface abstrata pura que define o contrato de medição.
    Qualquer classe que assinar este contrato deve saber calcular seu tamanho.
    """
    @abstractmethod
    def tamanho(self):
        pass


class Item(Medivel):
    """
    Classe abstrata que representa um elemento genérico do sistema de arquivos.
    Estabelece a herança de comportamento comum para todos os itens.
    """
    __slots__ = ["__nome", "__pai"]

    def __init__(self, nome, pai=None):
        self.__nome = nome
        self.__pai = None
        if pai is not None:
            pai.adicionar(self)

    @property
    def nome(self):
        return self.__nome

    @property
    def pai(self):
        return self.__pai

    @pai.setter
    def pai(self, novo_pai):
        self.__pai = novo_pai

    def mover_para(self, nova_pasta):
        """Move o item atual para uma nova pasta de destino."""
        if self.__pai is not None:
            self.__pai.remover(self)
        if nova_pasta is not None:
            nova_pasta.adicionar(self)

    def caminho(self):
        """Monta recursivamente o caminho absoluto do item na árvore."""
        if self.__pai is None:
            return self.__nome
        return f"{self.__pai.caminho()}/{self.__nome}"

    @abstractmethod
    def mostrar(self, recuo=0):
        pass


class Arquivo(Item):
    """
    Representa um arquivo físico final que armazena dados.
    """
    __slots__ = ["__tamanho_bytes"]

    def __init__(self, nome, tamanho_bytes, pai=None):
        self.__tamanho_bytes = tamanho_bytes
        super().__init__(nome, pai)

    def tamanho(self):
        """Devolve o tamanho físico real do arquivo."""
        return self.__tamanho_bytes

    def mostrar(self, recuo=0):
        """Imprime o arquivo formatado com seu respectivo recuo visual."""
        espacos = " " * recuo
        print(f"{espacos}- {self.nome} ({self.tamanho()} bytes)")


class Pasta(Item):
    """
    Representa um diretório que pode conter outros itens (pastas, arquivos, atalhos).
    """
    __slots__ = ["__itens"]

    def __init__(self, nome, pai=None):
        self.__itens = []
        super().__init__(nome, pai)

    @property
    def itens(self):
        return self.__itens

    def adicionar(self, item):
        """Adiciona um item à pasta e o vincula como filho."""
        self.__itens.append(item)
        item.pai = self

    def remover(self, item):
        """Remove um item da lista interna e remove seu vínculo paterno."""
        self.__itens.remove(item)
        item.pai = None

    def tamanho(self):
        """Calcula de forma polimórfica o tamanho somado de seus itens internos."""
        total = 0
        for item in self.__itens:
            total = total + item.tamanho()
        return total

    def mostrar(self, recuo=0):
        """Exibe o nome da pasta e solicita a seus filhos que se mostrem."""
        espacos = " " * recuo
        print(f"{espacos}+ {self.nome}/")
        for item in self.__itens:
            item.mostrar(recuo + 2)


class Lixeira:
    """
    Componente independente que armazena itens descartados.
    Implementa a interface Medivel de forma direta.
    """
    __slots__ = ["__descartados"]

    def __init__(self):
        self.__descartados = []

    def descartar(self, item):
        """Insere um item na lista de descarte retirando-o de sua árvore original."""
        item.mover_para(None)
        self.__descartados.append(item)

    def tamanho(self):
        """Mede o tamanho total acumulado de todos os objetos na lixeira."""
        total = 0
        for item in self.__descartados:
            total = total + item.tamanho()
        return total


class Atalho(Item):
    """
    Representa um link simbólico que aponta para outro elemento do sistema.
    Demonstra polimorfismo, herança refinada e encapsulamento estrito.
    """
    __slots__ = ["__destino"]

    def __init__(self, nome, destino, pai=None):
        self.__destino = None
        # Executa a validação antes mesmo de vincular o item ao pai
        self.redirecionar(destino)
        super().__init__(nome, pai)

    @property
    def destino(self):
        """Expõe o destino de forma pública apenas para leitura."""
        return self.__destino

    def redirecionar(self, novo_destino):
        """
        Modifica o alvo do atalho. Impede referências circulares ou
        apontamentos para pastas ancestrais que gerariam loops na árvore.
        """
        if novo_destino is self:
            raise ValueError("Um atalho nao pode apontar para ele mesmo.")

        # Valida se o novo destino é um ancestral direto do atalho atual
        atual = self.pai
        while atual is not None:
            if novo_destino is ...:  # Tratado polimorficamente por ID de objeto
                pass
            if novo_destino is atual:
                raise ValueError("Um atalho nao pode apontar para um de seus ancestrais.")
            atual = atual.pai

        self.__destino = novo_destino

    def tamanho(self):
        """Retorna o tamanho fixo de 1 byte, respeitando o polimorfismo."""
        return 1

    def mostrar(self, recuo=0):
        """Exibe a assinatura visual do atalho indicando o caminho final."""
        espacos = " " * recuo
        print(f"{espacos}@ {self.nome} -> {self.__destino.caminho()}")


def espaco_total(mediveis):
    """Calcula a soma agregada de qualquer estrutura compatível com Medivel."""
    total = 0
    for elemento in mediveis:
        total = total + elemento.tamanho()
    return total


def tentar(funcao):
    """Encapsula execuções propensas a falhas para exibir erros amigavelmente."""
    try:
        funcao()
    except Exception as erro:
        print(f"[ERRO ESPERADO]: {erro}")


# ==============================================================================
# Bloco de Testes Executáveis (Personalizado Ryan)
# ==============================================================================

# Criação da árvore base de diretórios
raiz = Pasta("C:")
pasta_users = Pasta("Users", raiz)
pasta_usuario = Pasta("Ryan", pasta_users)
pasta_desktop = Pasta("Desktop", pasta_usuario)

# Criação de arquivos físicos reais
arquivo_notas = Arquivo("notas.txt", 500, pasta_desktop)
arquivo_foto = Arquivo("foto.png", 2500, pasta_desktop)

# Criação dos atalhos polimórficos
atalho_para_arquivo = Atalho("atalho_notas", arquivo_notas, pasta_desktop)
atalho_para_pasta = Atalho("atalho_usuario", pasta_usuario, pasta_desktop)

print("--- EXIBIÇÃO DA ÁRVORE COMPLETA ---")
raiz.mostrar()
print()

print("--- MEDIÇÃO DE ESPAÇO AGREGADO (INTERFACE) ---")
lixeira_teste = Lixeira()
arquivo_velho = Arquivo("antigo.log", 150, None)
lixeira_teste.descartar(arquivo_velho)

# Lista misturando Arquivo, Pasta (com atalho interno) e Lixeira
elementos_para_medir = [arquivo_notas, pasta_desktop, lixeira_teste]
print(f"Espaço total calculado: {espaco_total(elementos_para_medir)} bytes")
print()

print("--- TESTES DE VALIDAÇÃO E ENCAPSULAMENTO (FALHAS CONTROLADAS) ---")

# Falha 1: Tentar alterar a propriedade diretamente (Não possui setter)
def teste_erro_setter():
    atalho_para_arquivo.destino = arquivo_foto
print("1. Tentando alterar propriedade .destino diretamente:")
tentar(teste_erro_setter)

# Falha 2: Tentar apontar para o próprio objeto atalho
print("\n2. Tentando apontar o atalho para ele mesmo:")
tentar(lambda: atalho_para_arquivo.redirecionar(atalho_para_arquivo))

# Falha 3: Tentar apontar para uma pasta ancestral (no caso, a pasta Desktop onde ele vive)
print("\n3. Tentando apontar o atalho para sua própria pasta pai (Desktop):")
tentar(lambda: atalho_para_arquivo.redirecionar(pasta_desktop))
