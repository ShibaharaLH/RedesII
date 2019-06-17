import random
import math
import sys

#verifica quantos bits de paridade serao necessarios para a codificacao
def getNoOfParityBits(noOfBits):
	i=0
	while 2.**i <= noOfBits + i :
		i+=1

	return i

#verifica quantos bits de paridade estao sendo utilizado no pacote
def getNoOfParityBitsInCode(noOfBits):
	i=0
	while 2.**i <= noOfBits:
		i+=1

	return i

#verifica o valor do bit de varidade
def getValueParityBit(pack, initialIndex, increment):
    bitsSum = 0
    indexPack = initialIndex
    #usado para percorrer todos os indices do pacote
    while indexPack <= len(pack) - 1:
        aux = 0
        #usado para somar os valores dos bits da sublista (soma n pula n)
        while aux < increment:
            if indexPack + aux <= len(pack) - 1:
                bitsSum += pack[indexPack]
                aux += 1
                indexPack += 1
            else:
                aux = increment
            indexPack += increment
    # paridade impar
    if bitsSum % 2 == 0:
        return 1
    else:
        return 0

#retorna uma lista com bit de valor 0 nas posicoes de paridade e os bits de mensagem
def appendParityBit(originalPacket, parityBits):
    # contador de indice da mensagem a ser transmitida
    i = 0
    # contador de bits de paridade
    j = 0
    # contador do indice da mensagem original
    k = 0
    message = list()
    while i < parityBits + len(originalPacket):
        # insere o bit de valor 0 na posicao de paridade
        if i == (2. ** j) - 1:
            message.insert(i, 0)
            j += 1
        # insere o bit de valor da mensagem original na mensagem a ser transmitida
        else:
            message.insert(i, originalPacket[k])
            k += 1
        i += 1
    return message

#realiza a deteccao de erro
def errorDetection(transmittedPacket, noOfParityBitsInCode):
    indexError = 0
    noOfParityBits = 0
    contError = 0;
    #usado para verificar todos os bits de paridade
    while noOfParityBits < noOfParityBitsInCode:
        #como usamos a paridade impar, se a soma dos bits de mensagem e de paridade for 1, ha um erro
        if getValueParityBit(transmittedPacket, (2 ** noOfParityBits) - 1, 2 ** noOfParityBits) == 1:
            indexError += (2 ** noOfParityBits)
            contError += 1
        noOfParityBits += 1
    if contError > 0:
        if contError == 1:
            indexError += contError
        else:
            indexError += contError - 1
        #verifica se houve mais de um erro
        if indexError >= len(transmittedPacket):
            return -2
        return indexError
    else:
        return -1

#realiza a correcao do erro. Flopamos o bit
def errorCorrection(packet, indexOfIncorrectParityBit):
    if packet[indexOfIncorrectParityBit] == 1:
        packet[indexOfIncorrectParityBit] = 0
    else:
        packet[indexOfIncorrectParityBit] = 1
    return packet


def codePacket(originalPacket):
    #verifica o numero de bits de paridade que sera necessario
    noOfParityBitsMessage = getNoOfParityBits(len(originalPacket))
    #insere o bit de valor 0 na posicao de paridade
    message = appendParityBit(originalPacket,noOfParityBitsMessage)
    noOfParityBits = 0
    while noOfParityBits < noOfParityBitsMessage:
        #insere o devido valor do bit de paridade
        message[(2 ** noOfParityBits) - 1] = getValueParityBit(message, (2 ** noOfParityBits) - 1, 2 ** noOfParityBits)
        noOfParityBits += 1
    return message

def decodePacket(transmittedPacket):
    #verifica quantos bits de paridade estao sendo utilizados no pacote transmitido
    noOfParityBitsInCode = getNoOfParityBitsInCode(len(transmittedPacket))
    #verifica se houve um erro
    verifyError = errorDetection(transmittedPacket, noOfParityBitsInCode)
    if verifyError > -1:
        #realiza a correcao do erro
        transmittedPacket = errorCorrection(transmittedPacket, verifyError)

    message = list()
    i = 0
    j = 0
    #decodifica o pacote
    while i < len(transmittedPacket):
        if i == (2. ** j) - 1:
            j += 1
        else:
            message.insert(i, transmittedPacket[i])
        i += 1
    return message

##
# Gera conteudo aleatorio no pacote passado como
# parametro. Pacote eh representado por um vetor
# em que cada posicao representa um bit.
# Comprimento do pacote (em bytes) deve ser
# especificado.
##
def generateRandomPacket(l):

    return [random.randint(0,1) for x in range(8 * l)]

##
# Gera um numero pseudo-aleatorio com distribuicao geometrica.
##
def geomRand(p):

    uRand = 0
    while(uRand == 0):
        uRand = random.uniform(0, 1)

    return int(math.log(uRand) / math.log(1 - p))

##
# Insere erros aleatorios no pacote, gerando uma nova versao.
# Cada bit tem seu erro alterado com probabilidade errorProb,
# e de forma independente dos demais bits.
# Retorna o numero de erros inseridos no pacote e o pacote com erros.
##
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

##
# Conta o numero de bits errados no pacote
# decodificado usando como referencia
# o pacote original. O parametro packetLength especifica o
# tamanho dos dois pacotes em bytes.
##
def countErrors(originalPacket, decodedPacket):
    errors = 0

    for i in range(len(originalPacket)):

        if originalPacket[i] != decodedPacket[i]:
            errors = errors + 1

    return errors

##
# Exibe modo de uso e aborta execucao.
##
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
    help(sys.argv[0])

##
# Inicializacao da semente do gerador de numeros
# pseudo-aleatorios.
##
random.seed()

##
# Geracao do pacote original aleatorio.
##

originalPacket = generateRandomPacket(packetLength)
codedPacket = codePacket(originalPacket)

##
# Loop de repeticoes da simulacao.
##
for i in range(reps):

    ##
    # Gerar nova versao do pacote com erros aleatorios.
    ##
    insertedErrorCount, transmittedPacket = insertErrors(codedPacket, errorProb)
    totalInsertedErrorCount = totalInsertedErrorCount + insertedErrorCount

    ##
    # Gerar versao decodificada do pacote.
    ##
    decodedPacket = decodePacket(transmittedPacket)

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