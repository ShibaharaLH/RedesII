import random
import math
import sys

#########
# Implementacao simplificada de um esquema de paridade bidimensional 2x4
# (paridade par).
#
# Cada byte do pacote (2x4 = 8 bits) eh mapeado para uma matrix 2x4:
# d0 d1 d2 d3 d4 d5 d6 d7 => --           --
#                            | d0 d1 d2 d3 |
#                            | d4 d5 d6 d7 |
#                            --           --
# Cada coluna 0 <= i <= 3 da origem a uma paridade pc_i.
# Cada linha 0 <= i <= 1 da origem a uma paridade pl_i.
#
# No pacote codificado, os bits sao organizados na forma:
# d0 d1 d2 d3 d4 d5 d6 d7 pc0 pc1 pc2 pc3 pl0 pl1
#
# Isso se repete para cada byte do pacote original.
########

###
##
# Funcoes a serem alteradas!
##
###

##
# Codifica o pacote de entrada, gerando um pacote
# de saida com bits redundantes.
##

def leCoordenada():

    input = raw_input("Dimensao da Matriz: ")

    try:
        i = int(input.split(' ')[0])
        j = int(input.split(' ')[1])
    except ValueError:
        print ("Dimensao invalida! Use o formato \"i j\" (sem aspas),")
        raw_input("Pressione <enter> ...")
        return False

    return (i, j)

def codePacket(originalPacket, b, z):

    ## OriginalPacket vem em formato de bits num vetor
    parityMatrix = [[0 for x in range(z)] for y in range(b)]

    if (len(originalPacket) % (b*z) == 0):
        codedLen = (len(originalPacket) / (b*z)) * ((b*z) + b + z)
    else:
        codedLen = (((len(originalPacket) / (b*z)) + 1) * ((b*z) + b + z))

    codedPacket = [0 for x in range(codedLen)]

    print('')
    print('originalPacket', originalPacket)
    print('')

    ##
    # Itera por cada byte do pacote original.
    ##

    tamanho = (len(originalPacket) / (b*z))

    if(len(originalPacket) % (b*z) != 0):
        tamanho = tamanho + 1

    auxiliar = len(originalPacket)

    for i in range(tamanho):

        ##
        # Bits do i-esimo byte sao dispostos na matriz.
        ##

        for j in range(0, b):
            for k in range(0, z):
                if auxiliar <= (i * (b*z) + z * j + k):
                    parityMatrix[j][k] = 0
                else:
                    parityMatrix[j][k] = originalPacket[i * (b*z) + z * j + k]

        print('parityMatrix Certo', parityMatrix)

        ##
        # Replicacao dos bits de dados no pacote codificado.
        ##

        for j in range(b*z):
            if (i * (b*z) + j) >= len(originalPacket):
                codedPacket[i * ((b*z) + b + z) + j] = 0
            else:
                codedPacket[i * ((b*z) + b + z) + j] = originalPacket[i * (b*z) + j]

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das colunas.
        ##

        for n in range(z):

            parityTop = parityMatrix[0][n]

            for j in range(1, b):

                parityTop = parityTop + parityMatrix[j][n]

OAOA            if parityTop % 2 == 0:
OAOA                codedPacket[i * ((b*z) + b + z) + b*z + n] = 0
OAOA
            else:
OAOA                codedPacket[i * ((b*z) + b + z) + b*z + n] = 1

OAOA        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das linhas.
        ##
OAOA

        for m in range(b):

            paritySide = parityMatrix[m][0]

            for j in range(1,z):
                paritySide = paritySide + parityMatrix[m][j]

            if (paritySide % 2 == 0):
                codedPacket[i * ((b*z) + b + z) + (b*z) + z + m] = 0
            else:
                codedPacket[i * ((b*z) + b + z) + (b*z) + z + m] = 1

    print('')
    print('codedPacket Final', codedPacket)
    print('')

    return codedPacket

##
# Executa decodificacao do pacote transmittedPacket, gerando
# novo pacote decodedPacket.
##

def decodePacket(transmittedPacket, b, z):

    parityMatrix = [[0 for x in range(z)] for y in range(b)]
    parityColumns = [0 for x in range(z)]
    parityRows = [0 for x in range(b)]
    decodedPacket = [0 for x in range(len(transmittedPacket))]

    # quantidade de bits por matriz (b*z) bits de dados + (b + z) bits de paridade
    sizeByte = (b*z) + b + z

    n = 0 # Contador de bytes no pacote decodificado.

    ##
    # Itera por cada sequencia de 14 bits (8 de dados + 6 de paridade).
    ##
    for i in range(0, len(transmittedPacket), sizeByte):

        ##
        # Bits do i-esimo conjunto sao dispostos na matriz.
        ##
        for j in range(b):
            for k in range(z):
                parityMatrix[j][k] = transmittedPacket[i + z * j + k]

        ##
        # Bits de paridade das colunas.
        ##
        for j in range(z):
            parityColumns[j] = transmittedPacket[i + (b*z) + j]

        ##
        # Bits de paridade das linhas.
        ##
        for j in range(b):
            parityRows[j] = transmittedPacket[i + (b*z) + z + j]

        ##
        # Verificacao dos bits de paridade: colunas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##

        errorInColumn = -1

        for c in range(z):

            parityTop = parityMatrix[0][c]

            for j in range(1, b):

                parityTop = parityTop + parityMatrix[j][c]

            if parityTop % 2 != parityColumns[c]:
                errorInColumn = c
                break

        ##
        # Verificacao dos bits de paridade: linhas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##

        errorInRow = -1

        for m in range(b):

            paritySide = parityMatrix[m][0]

            for j in range(1,z):
                paritySide = paritySide + parityMatrix[m][j]

            if paritySide % 2 != parityRows[m]:
                errorInRow = m
                break

        ##
        # Se algum erro foi encontrado, corrigir.
        ##
        if errorInRow > -1 and errorInColumn > -1:

            if parityMatrix[errorInRow][errorInColumn] == 1:
                parityMatrix[errorInRow][errorInColumn] = 0
            else:
                parityMatrix[errorInRow][errorInColumn] = 1

        ##
        # Colocar bits (possivelmente corrigidos) na saida.
        ##

        for j in range(b):
            for k in range(z):
                decodedPacket[(b*z) * n + z * j + k] = parityMatrix[j][k]

        ##
        # Incrementar numero de bytes na saida.
        ##
        n = n + 1

    return decodedPacket

###
##
# Outras funcoes.
##
###

##
# Gera conteudo aleatorio no pacote passado como
# parametro. Pacote eh representado por um vetor
# em que cada posicao representa um bit.
# Comprimento do pacote (em bytes) deve ser
# especificado.
##
def generateRandomPacket(l):

    return [random.randint(0,1) for x in range(8 * l)]

def geomRand(p):

    uRand = 0
    while(uRand == 0):
        uRand = random.uniform(0, 1)

    return int(math.log(uRand) / math.log(1 - p))

def insertErrors(codedPacket, errorProb):

    i = -1
    n = 0 # Numero de erros inseridos no pacote.

    ##
    # Copia o conteudo do pacote codificado para o novo pacote.
    ##
    transmittedPacket = list(codedPacket)

    while 1:

        ##
        # Sorteia a proxima posicao em que um erro sera inserido.
        ##
        r = geomRand(errorProb)
        i = i + 1 + r

        if i >= len(transmittedPacket):
            break

        ##
        # Altera o valor do bit.
        ##
        if transmittedPacket[i] == 1:
            transmittedPacket[i] = 0
        else:
            transmittedPacket[i] = 1

        n = n + 1

    return n, transmittedPacket

def countErrors(originalPacket, decodedPacket):

    errors = 0

    for i in range(len(originalPacket)):
        if originalPacket[i] != decodedPacket[i]:
            errors = errors + 1

    return errors

def help(selfName):

    sys.stderr.write("Simulador de metodos de FEC/codificacao.\n\n")
    sys.stderr.write("Modo de uso:\n\n")
    sys.stderr.write("\t" + selfName + " <tam_pacote> <reps> <prob. erro>\n\n")
    sys.stderr.write("Onde:\n")
    sys.stderr.write("\t- <tam_pacote>: tamanho do pacote usado nas simulacoes (em bytes).\n")
    sys.stderr.write("\t- <reps>: numero de repeticoes da simulacao.\n")
    sys.stderr.write("\t- <prob. erro>: probabilidade de erro de bits (i.e., probabilidade\n")
    sys.stderr.write("de que um dado bit tenha seu valor alterado pelo canal.)\n\n")

    sys.exit(1)

##
# Programa principal:
#  - le parametros de entrada;
#  - gera pacote aleatorio;
#  - gera bits de redundancia do pacote
#  - executa o numero pedido de simulacoes:
#      + Introduz erro
#  - imprime estatisticas.
##

##
# Inicializacao de contadores.
##
totalBitErrorCount = 0
totalPacketErrorCount = 0
totalInsertedErrorCount = 0

##
# Leitura dos argumentos de linha de comando.
##
if len(sys.argv) != 4:
    help(sys.argv[0])

packetLength = int(sys.argv[1])
reps = int(sys.argv[2])
errorProb = float(sys.argv[3])

if packetLength <= 0 or reps <= 0 or errorProb < 0 or errorProb > 1:
    help(argv[0])

##
# Inicializacao da semente do gerador de numeros
# pseudo-aleatorios.
##
random.seed()

##
# Geracao do pacote original aleatorio.
##

coordenadas = leCoordenada()

b, z = coordenadas

originalPacket = generateRandomPacket(packetLength)
codedPacket = codePacket(originalPacket, b, z)

for i in range(reps):

    ##
    # Gerar nova versao do pacote com erros aleatorios.
    ##
    insertedErrorCount, transmittedPacket = insertErrors(codedPacket, errorProb)
    totalInsertedErrorCount = totalInsertedErrorCount + insertedErrorCount

    ##
    # Gerar versao decodificada do pacote.
    ##
    decodedPacket = decodePacket(transmittedPacket, b, z)

    ##
    # Contar erros.
    ##
    bitErrorCount = countErrors(originalPacket, decodedPacket)

    if bitErrorCount > 0:

        totalBitErrorCount = totalBitErrorCount + bitErrorCount
        totalPacketErrorCount = totalPacketErrorCount + 1

print 'Numero de transmissoes simuladas: {0:d}\n'.format(reps)
print 'Numero de bits transmitidos: {0:d}'.format(reps * packetLength * 8)
print 'Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount)
print 'Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0)
print 'Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount)
print 'Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(float(totalBitErrorCount) / float(reps * packetLength * 8) * 100.0)
print 'Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount)
print 'Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0)
