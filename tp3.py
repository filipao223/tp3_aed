import sys

pontos = ['!', '?', '.', ',', '<', '>', '(', ')', '$', '€', '@', '«', '»', '-']
alf = 'abcdefghijklmnopqrstuvwxyz'

class Node(object):
    """docstring for Node."""
    def __init__(self, palavra, freq):
        super(Node, self).__init__()
        self.palavra = palavra
        self.frequencia = freq
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

    def get(self, palavra):
        current = self.head.nextNode

        if current is None:
            return ""
        else:
            while(current != None):
                if(current.palavra == palavra): return palavra
                current = current.nextNode
            return ""


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

    def get(self, hashValue, palavra):
        try:
            return self.listas[hashValue].get(palavra)
        except:
            return ""

        return ""

#A partir de palavra, encontra todas as palavras a uma correçao de distancia
def editWord(palavra):
    #Adicionar uma letra
    addOneLetterRes = [palavra[:i]+letra+palavra[i:] for i in range(len(palavra)+1) for letra in alf]
    delOneLetterRes = [palavra[:i]+palavra[i+1:] for i in range(len(palavra))]
    repOneLetterRes = [palavra[:i]+letra+palavra[i+1:] for i in range(len(palavra)) for letra in alf]
    swtOneLetterRes = [palavra[:i]+palavra[i+1]+palavra[i]+palavra[i+2:] for i in range(len(palavra)) if(i < len(palavra)-1)]
    return addOneLetterRes + delOneLetterRes + repOneLetterRes + swtOneLetterRes

#Apaga a pontuaçao da palavra
def delPont(palavra):
    hasChanged = True
    while(hasChanged):
        hasChanged = False
        for char in palavra:
            if(char in pontos):
                hasChanged = True
                palavra = palavra.replace(char, "")
                break

    return palavra

#Função de dispersão
def hash(pal, size):
    sum = 0
    for char in pal:
        sum += ord(char)

    return sum % size

def main():
    tempInputPals = []
    finalInputPals = []
    finalOutputPals = []
    distanciaErro1 = []

    #Verifica os parametros
    try:
        fileInput = sys.argv[1]
    except IndexError:
        print("Wrong number of arguments")
        sys.exit(0)

    #Tabela de hash
    tableSize = 4049 #Numero de palavras da lista é 3665
    tabela = Tabela(tableSize)

    #Localizaçao do ficheiro com as palavras do dicionario
    wordsFilePath = "words/sortedWords_small.txt"

    #Adiciona as palavras do dicionario na tabela de dispersao
    with open(wordsFilePath, "r") as f:
        listaPalavras = [pal for pal in f.read().split()]

    for pal in listaPalavras:
        tabela.add(hash(pal, tableSize), pal)

    #Le as palavras do input
    with open(fileInput, "r") as f:
        tempInputPals = [pal for pal in f.read().split()]

    #Remove pontuacao das palavras (se existir)
    for pal in listaPalavras:
        finalInputPals.append(delPont(pal))

    #Verifica agora se ha erros ortograficos
    for pal in finalInputPals:
        if(tabela.get(hash(pal, tableSize), pal) != ""): finalOutputPals.append(pal)
        else:
            #Primeiro os erros de distancia 1
            distanciaErro1 = editWord(pal)


if __name__ == "__main__":
    main()
