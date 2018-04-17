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
        self.head = node("")

    def add(self,palavra):
        current = head.nextNode

        if current is None:
            current = Node(palavra)
            return True
        else:
            current = current.nextNode

        return False


class Tabela(object):
    """docstring for tabela."""
    def __init__(self, size):
        super(tabela, self).__init__()
        self.size = size
        self.listas = [None] * size

    def add(self, hashValue, palavra):
        try:
            listas[hashValue].add(palavra)
            return True
        except IndexError:
            #Nao existe valor hash
            listas.append(hashValue)
            listas[hashValue].add(palavra)

        return False

def hash(key, size):
    return key * key % size

def main():

if __name__ == "__main__":
    main()
