import sys
import time

pontos = ['!', '?', '.', ',', '<', '>', '(', ')', '$', '€', '@', '«', '»']
alf = 'abcdefghijklmnopqrstuvwxyz'
todos_pontos = []  # Pontuação removida


class Node(object):
    """docstring for Node."""
    def __init__(self, palavra):
        super(Node, self).__init__()
        self.palavra: str = palavra
        self.frequencia: int = 0  # Quanto maior, mais frequente é a palavra
        self.nextNode = None


class NodeHist(Node):
    def __init__(self, palavra, correcao):
        super(NodeHist, self).__init__(palavra)
        self.correcao = correcao


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

    def add_correcao(self, palavra, correcao):
        current = self.head
        while current is not None:
            if current.nextNode is None:
                current.nextNode = NodeHist(palavra, correcao)
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

    def add_correcao(self, hash_value, palavra, correcao):
        try:
            self.listas[hash_value].add_correcao(palavra, correcao)
            self.entries += 1
            return True
        except:
            # Nao existe valor hash
            self.listas[hash_value] = Lista()
            self.listas[hash_value].add_correcao(palavra, correcao)
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
def del_pont(palavra, word_number):
    has_changed = True
    index = 0
    while has_changed:
        has_changed = False
        for char in palavra:
            if char in pontos:
                todos_pontos.append(char + "|" + str(index) + "|" + str(word_number))
                has_changed = True
                palavra = palavra.replace(char, "")
                break
            index += 1

    return palavra


# Função de dispersão (SDBM)
def hash_function(pal, size):
    hash_value = 0

    for letra in pal:
        hash_value = ord(letra) + (hash_value << 6) + (hash_value << 16) - hash_value

    return hash_value % size


def main():
    final_input_pals = []
    final_output_pals = []
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
    tam_tabela_hist = 4813
    tabela_hist = Tabela(tam_tabela_hist)

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

    # Le as palavras do input
    with open(file_input, "r") as f:
        temp_input_pals = [pal for pal in f.read().split()]

    # Remove pontuacao das palavras (se existir)
    i = 0
    for pal in temp_input_pals:
        final_input_pals.append(del_pont(pal, i))
        i += 1

    # Verifica agora se ha erros ortograficos
    for pal in final_input_pals:
        distancia_erro2 = []

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
                # Primeiro verifica se a correçao existe no historico
                returned_node = tabela_hist.get(hash_function(pal, tam_tabela_hist), pal)
                if returned_node is not None:
                    print("Do historico,", returned_node.correcao, "? (Y-yes N-no)")
                    choice = input()
                    if choice == "Y" or choice == "y":
                        final_output_pals.append(returned_node.correcao)
                        continue

                # Não existe, primeiro os erros de distancia 1
                distancia_erro1 = edit_word(pal)

                # E os erros de distancia 2
                for pal_2 in distancia_erro1:
                    distancia_erro2 += edit_word(pal_2)

                # Guarda num array as 5 palavras que existem mais frequentes
                most_frequent = []
                least_frequent_index = 0

                for edited_word in distancia_erro2:
                    returned_node = tabela_pals.get(hash_function(edited_word, tam_tabela_pals), edited_word)

                    if returned_node is not None and returned_node not in most_frequent:
                        if len(most_frequent) < 5:
                            # Se há um espaço livre na lista, guarda lá o node recebido
                            most_frequent.append(returned_node)
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
                        # Coloca no historico a correçao
                        tabela_hist.add_correcao(hash_function(pal, tam_tabela_hist), pal, node.palavra)
                        correction_rejected = False
                        break

                if correction_rejected:
                    final_output_pals.append("CORREÇÃO-NÃO-ENCONTRADA")

    # Volta a colocar pontuação
    frase_final = ""
    i = 0
    for pal in final_output_pals:
        word_not_added = True
        for pont in todos_pontos:
            splits = pont.split("|")
            if int(splits[2]) == i:  # Se esta palavra tinha algum ponto
                if int(splits[1]) > len(pal) / 2:  # O ponto estava provavelmente no fim
                    pal += splits[0]
                    frase_final += (pal + " ")
                else:  # O ponto estava provavelmente no inicio
                    splits[0] += pal
                    frase_final += (splits[0] + " ")
                word_not_added = False
        i += 1
        if word_not_added:
            frase_final += (pal + " ")

    print(frase_final)


if __name__ == "__main__":
    main()
