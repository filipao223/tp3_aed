import sys
from pympler import asizeof

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

    def add(self,palavra):
        current = self.head.nextNode

        if current is None:
            current = Node(palavra)
            return True
        else:
            current = current.nextNode

        return False


class Tabela(object):
    """docstring for Tabela."""
    def __init__(self, size):
        super(Tabela, self).__init__()
        self.size = size
        self.listas = [None] * size

    def add(self, hashValue, palavra):
        try:
            self.listas[hashValue].add(palavra)
            return True
        except:
            #Nao existe valor hash
            self.listas[hashValue] = Lista()
            self.listas[hashValue].add(palavra)

        return False

def hash(pal, size):
    sum = 0
    for char in pal:
        sum += ord(char)

    return sum % size

def main():
    try:
        fileInput = sys.argv[1]
    except IndexError:
        print("Wrong number of arguments")
        sys.exit(0)

    #Tabela de hash
    tableSize = 65536
    tabela = Tabela(tableSize)

    print(asizeof.asizeof(tabela))

    wordsFilePath = "words/wordlist-preao-latest.txt"

    with open(wordsFilePath, "r") as f:
        #Convert to list of words
        listaPalavras = [pal for pal in f.read().split()]

    for pal in listaPalavras:
        #Add to hash table each word
        tabela.add(hash(pal, tableSize), pal)

    print(asizeof.asizeof(tabela))


if __name__ == "__main__":
    main()
