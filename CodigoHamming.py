import random
import math
import sys

def generateRandomPacket(l):
    return [random.randint(0,1) for x in range(8 * l)]

def getNoOfParityBits(noOfBits):
	i=0
	while 2.**i <= noOfBits + i : # (power of 2 + parity bits laready  counted) that is for 4 bit of dataword requires 3 bit of parity bits
		i+=1

	return i

def getNoOfParityBitsInCode(noOfBits):
	i=0
	while 2.**i <= noOfBits:
		i+=1

	return i

def getValueParityBit(pack, initialIndex, increment):
    bitsSum = 0
    indexPack = initialIndex
    while indexPack <= len(pack) - 1:
        aux = 0
        while aux < increment:
            if indexPack + aux <= len(pack) - 1:
                bitsSum += pack[indexPack]
                aux += 1
                indexPack += 1
            aux = increment
            indexPack += increment

    if bitsSum % 2 == 0:
        return 1
    else:
        return 0

def appendParityBit(originalPacket, parityBits):
    i = 0
    j = 0
    k = 0
    message = list()
    while i < parityBits + len(originalPacket):
        if i == (2. ** j) - 1:
            message.insert(i, 0)
            j += 1
        else:
            message.insert(i, originalPacket[k])
            k += 1
        i += 1
    return message

def errorDetection(transmittedPacket, noOfParityBitsInCode):
    indexError = 0
    noOfParityBits = 0
    while noOfParityBits < noOfParityBitsInCode:
        if getValueParityBit(transmittedPacket, (2 ** noOfParityBits) - 1, 2 ** noOfParityBits) == 1:
            indexError += (2 ** noOfParityBits)
        noOfParityBits += 1
    indexError -= 1
    return indexError

def errorCorrection(packet, indexOfIncorrectParityBit):
    if packet[indexOfIncorrectParityBit] == 1:
        packet[indexOfIncorrectParityBit] = 0
    else:
        packet[indexOfIncorrectParityBit] = 1
    return packet


def codePacket(originalPacket):
    noOfParityBitsMessage = getNoOfParityBits(len(originalPacket))
    message = appendParityBit(originalPacket,noOfParityBitsMessage)
    noOfParityBits = 0
    while noOfParityBits < noOfParityBitsMessage:
        message[(2 ** noOfParityBits) - 1] = getValueParityBit(message, (2 ** noOfParityBits) - 1, 2 ** noOfParityBits)
        noOfParityBits += 1
    return message

def decodePacket(transmittedPacket):
    noOfParityBitsInCode = getNoOfParityBitsInCode(len(transmittedPacket))
    verifyError = errorDetection(transmittedPacket, noOfParityBitsInCode)
    if verifyError != -1:
        transmittedPacket = errorCorrection(transmittedPacket, verifyError)
    message = list()
    i = 0
    j = 0
    while i < len(transmittedPacket):
        if i == (2. ** j) - 1:
            j += 1
        else:
            message.insert(i, transmittedPacket[i])
        i += 1
    return message

print codePacket(generateRandomPacket(3))