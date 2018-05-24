import sys

pontos = ['!', '?', '.', ',', '<', '>', '(', ')', '$', '€', '@', '«', '»', '-']
alf = 'abcdefghijklmnopqrstuvwxyz'


class Node(object):
    """docstring for Node."""
    def __init__(self, palavra):
        super(Node, self).__init__()
        self.palavra = palavra
        self.frequencia: int = 0  # Quanto maior, mais frequente é a palavra
        self.nextNode = None


class Lista(object):
    """docstring for lista."""
    def __init__(self):
        super(Lista, self).__init__()
        self.head = Node("")
        self.numero = 0

    def add(self, palavra):
        current = self.head
        while current is not None:
            if current.nextNode is None:
                current.nextNode = Node(palavra)
                self.numero += 1
                return True
            elif current.palavra == palavra:
                return False
            else:
                current = current.nextNode

        return False

    def get(self, palavra):
        current = self.head.nextNode
        if current is None:
            return None
        else:
            while current is not None:
                if current.palavra == palavra:
                    return current
                current = current.nextNode
            return None

    def set_freq(self, pal, freq: int):
        current = self.head.nextNode
        while current is not None:
            if current.palavra == pal or current.palavra.lower() == pal.lower():
                current.frequencia = freq
                return True
            current = current.nextNode
        return False

    def print_lista(self, max_list, head, i):
        if head is not None and i != max_list:
            i += 1
            return head.palavra + "-->" + self.print_lista(max_list, head.nextNode, i)
        else:
            return ""


class Tabela(object):
    """docstring for Tabela."""
    def __init__(self, size):
        super(Tabela, self).__init__()
        self.size = size
        self.listas = [None] * size
        self.entries = 0

    def add(self, hash_value, palavra):
        try:
            self.listas[hash_value].add(palavra)
            self.entries += 1
            return True
        except:
            # Nao existe valor hash
            self.listas[hash_value] = Lista()
            self.listas[hash_value].add(palavra)
            self.entries += 1

    def get(self, hash_value, palavra):
        try:
            return self.listas[hash_value].get(palavra)
        except:
            return None

    def set_freq(self, hash_value, pal, freq: int):
        try:
            if self.listas[hash_value].set_freq(pal, freq):
                return True
        except:
            pass
        return False

    def print_hash(self, no_empty, max_hash_t, max_list):
        for i in range(self.size):
            if self.listas[i] is None :
                print("lista["+str(i)+"]: None")
            else:
                if i == max_hash_t:
                    return
                else:
                    print("lista[" + str(i) + "]:" + self.listas[i].print_lista(max_list, self.listas[i].head, 0))

    # Calcula o racio de colisao de entradas da tabela
    def collision_rate(self):
        total_collisions = 0
        for i in range(self.size):
            if self.listas[i] is not None and self.listas[i].head.nextNode is not None:
                current = self.listas[i].head.nextNode.nextNode
                while current is not None:
                    total_collisions += 1
                    current = current.nextNode
        print(round(total_collisions / self.entries * 100, 2), "% de colisao")


# A partir de palavra, encontra todas as palavras a uma correçao de distancia
def edit_word(palavra):
    # Adicionar uma letra
    add_one_letter_res = [palavra[:i] + letra + palavra[i:] for i in range(len(palavra)+1) for letra in alf ]
    del_one_letter_res = [palavra[:i] + palavra[i+1:] for i in range(len(palavra))]
    rep_one_letter_res = [palavra[:i]+letra+palavra[i+1:] for i in range(len(palavra)) for letra in alf]
    swt_one_letter_res = [palavra[:i]+palavra[i+1]+palavra[i]+palavra[i+2:] for i in range(len(palavra))
                          if(i < len(palavra)-1)]

    return add_one_letter_res + del_one_letter_res + rep_one_letter_res + swt_one_letter_res


# Apaga a pontuaçao da palavra
def del_pont(palavra):
    has_changed = True
    while has_changed:
        has_changed = False
        for char in palavra:
            if char in pontos:
                has_changed = True
                palavra = palavra.replace(char, "")
                break

    return palavra


# Função de dispersão (SDBM)
def hash_function(pal, size):
    hash_value = 0

    for letra in pal:
        hash_value = ord(letra) + (hash_value << 6) + (hash_value << 16) - hash_value

    return hash_value % size


def main():
    temp_input_pals = []
    final_input_pals = []
    final_output_pals = []
    distancia_erro1 = []
    distancia_erro2 = []

    # Verifica os parametros
    try:
        file_input = sys.argv[1]
    except IndexError:
        print("Wrong number of arguments")
        sys.exit(0)

    # Tabela de hash e tamanho (tamanhos primos)
    tam_tabela_pals = 1322963  # Num de palavras da lista é 994707, numero primo mais proximo de 1.33*994707 -> 1322963
    tabela_pals = Tabela(tam_tabela_pals)

    # Localizaçao do ficheiro com as palavras do dicionario
    words_file_path = "words/pt_sortedWords_big.txt"
    words_freq_path = "words/pt_wordFrequency_big.txt"

    # Adiciona as palavras do dicionario na tabela de dispersao
    with open(words_file_path, mode="r", encoding="utf-8") as f:
        lista_palavras = [pal for pal in f.read().split()]

    for pal in lista_palavras:
        tabela_pals.add(hash_function(pal, tam_tabela_pals), pal)

    # Adiciona as frequencias de algumas palavras na tabela de dispersao
    with open(words_freq_path, mode="r", encoding="utf-8") as f:
        content = [line.strip() for line in f.readlines()]

    for linha in content:
        splits = linha.split()
        tabela_pals.set_freq(hash_function(splits[1], tam_tabela_pals), splits[1], int(splits[0]))

    tabela_pals.collision_rate()

    # Le as palavras do input
    with open(file_input, "r") as f:
        temp_input_pals = [pal for pal in f.read().split()]

    # Remove pontuacao das palavras (se existir)
    for pal in temp_input_pals:
        final_input_pals.append(del_pont(pal))

    # Verifica agora se ha erros ortograficos
    for pal in final_input_pals:
        returned_node = tabela_pals.get(hash_function(pal, tam_tabela_pals), pal)
        if returned_node is not None:
            final_output_pals.append(pal)
        else:
            # Pergunta se a palavra deve ser guardada no dicionario
            print("Pretende guardar --", pal, "-- no dicionario? (Y-sim N-nao)")
            choice = input()

            if choice == "y" or choice == "Y":
                tabela_pals.add(hash_function(pal, tam_tabela_pals), pal)
                final_output_pals.append(pal)
            else:
                # Primeiro os erros de distancia 1
                distancia_erro1 = edit_word(pal)

                # E os erros de distancia 2
                for pal_2 in distancia_erro1:
                    distancia_erro2 += edit_word(pal_2)

                # Guarda num array as 5 palavras que existem mais frequentes
                most_frequent = [None] * 5
                least_frequent_index = 0

                for edited_word in distancia_erro2:
                    returned_node = tabela_pals.get(hash_function(edited_word, tam_tabela_pals), edited_word)

                    if returned_node is not None and returned_node not in most_frequent:
                        if None in most_frequent:
                            # Se há um espaço livre na lista, procura-o e guarda lá o node recebido
                            for i in range(5):
                                if most_frequent[i] is None:
                                    most_frequent[i] = returned_node
                        else:
                            # O array esta cheio, procura o node com a palavra menos frequente aí contida
                            for i in range(5):
                                if most_frequent[i].frequencia < most_frequent[least_frequent_index].frequencia:
                                    least_frequent_index = i

                            # Substitui então a dita palavra pela nova se esta for mais frequente
                            if most_frequent[least_frequent_index].frequencia < returned_node.frequencia:
                                most_frequent[least_frequent_index] = returned_node
                                least_frequent_index = 0

                correction_rejected = True
                print("For word ", pal, " did you mean: (Y-yes N-no)")
                # Ordena por frequência
                for node in sorted(most_frequent, key=lambda x: x.frequencia, reverse=True):
                    print(node.palavra, "?")
                    choice = input()
                    if choice == "y" or choice == "Y":
                        final_output_pals.append(node.palavra)
                        correction_rejected = False
                        break

                if correction_rejected:
                    final_output_pals.append("CORREÇÃO-NÃO-ENCONTRADA")

    print(final_output_pals)
    
    
if __name__ == "__main__":
    main()
