import sys

pontos = ['!', '?', '.', ',', '<', '>', '(', ')', '$', '€', '@', '«', '»', '-']
alf = 'abcdefghijklmnopqrstuvwxyz'


class Node(object):
    """docstring for Node."""
    def __init__(self, palavra):
        super(Node, self).__init__()
        self.palavra = palavra
        self.nextNode = None


class Lista(object):
    """docstring for lista."""
    def __init__(self):
        super(Lista, self).__init__()
        self.head = Node("")
        self.numero = 0

    def add(self, palavra):
        current = self.head
        if current.nextNode is None:
            current.nextNode = Node(palavra)
            self.numero += 1
            return True
        else:
            current = current.nextNode

        return False

    def get(self, palavra):
        current = self.head.nextNode
        if current is None:
            return ""
        else:
            while current is not None:
                if current.palavra == palavra: return palavra
                current = current.nextNode
            return ""

    def printLista(self, max_list, head, i):
        if head is not None and i != max_list:
            i += 1
            return head.palavra + "-->" + self.printLista(max_list, head.nextNode, i)
        else:
            return ""


class Tabela(object):
    """docstring for Tabela."""
    def __init__(self, size):
        super(Tabela, self).__init__()
        self.size = size
        self.listas = [None] * size

    def add(self, hash_value, palavra):
        try:
            self.listas[hash_value].add(palavra)
            return True
        except:
            # Nao existe valor hash
            self.listas[hash_value] = Lista()
            self.listas[hash_value].add(palavra)

    def get(self, hashValue, palavra):
        try:
            return self.listas[hashValue].get(palavra)
        except:
            return ""

        return ""

    def print_hash(self, no_empty, max_hash_t, max_list):
        for i in range(self.size):
            if self.listas[i] is None :
                print("lista["+str(i)+"]: None")
            else:
                if i == max_hash_t:
                    return
                else:
                    print("lista[" + str(i) + "]:" + self.listas[i].printLista(max_list, self.listas[i].head, 0))


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


# Função de dispersão
def hash(pal, size):
    sum_ascii = 0
    for letra in pal:
        sum_ascii += ord(letra)
    sum_ascii *= sum_ascii

    if sum_ascii < size*100:
        sum_ascii *= sum_ascii

    return sum_ascii % size


def main():
    temp_input_pals = []
    final_input_pals = []
    final_output_pals = []
    distancia_erro1 = []
    distancia_erro2 = []

    # Verifica os parametros
    try:
        fileInput = sys.argv[1]
    except IndexError:
        print("Wrong number of arguments")
        sys.exit(0)

    # Tabela de hash e tamanho (tamanhos primos)
    tam_tabela_pals = 32 # SIZE = 4813 Numero de palavras da lista é 3665,
    tabela_pals = Tabela(tam_tabela_pals)
    tam_tabela_freq = 1217 # Numero de frequencias é 1000
    tabela_freq = Tabela(tam_tabela_freq)

    # Localizaçao do ficheiro com as palavras do dicionario
    words_file_path = "words/pt_sortedWords_small.txt"

    # Adiciona as frequencias de algumas palavras numa tabela de dispersao
    print(hash("ontei", tam_tabela_pals))

    # Adiciona as palavras do dicionario na tabela de dispersao
    with open(words_file_path, "r") as f:
        lista_palavras = [pal for pal in f.read().split()]

    for pal in lista_palavras:
        tabela_pals.add(hash(pal, tam_tabela_pals), pal)

    tabela_pals.print_hash(False, 2, 0)
    # Le as palavras do input
    with open(fileInput, "r") as f:
        temp_input_pals = [pal for pal in f.read().split()]

    # Remove pontuacao das palavras (se existir)
    for pal in temp_input_pals:
        final_input_pals.append(del_pont(pal))

    # Verifica agora se ha erros ortograficos
    for pal in final_input_pals:
        print(tabela_pals.get(hash(pal, tam_tabela_pals), pal))
        if tabela_pals.get(hash(pal, tam_tabela_pals), pal) != "":
            final_output_pals.append(pal)
        else:
            # Primeiro os erros de distancia 1
            distancia_erro1 = edit_word(pal)
            print(distancia_erro1)
            # E os erros de distancia 2
            """for pal in distancia_erro1:
                distancia_erro2 += edit_word(pal)
            print(distancia_erro2, len(distancia_erro2))"""

    print(final_output_pals)
    
    
if __name__ == "__main__":
    main()
