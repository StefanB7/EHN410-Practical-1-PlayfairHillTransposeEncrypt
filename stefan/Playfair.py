#EHN 410 - Practical 1 - 2021
#Playfair encryption and decryption
#Group 7
#Created: 2 April 2021

import numpy as np
import string

playfairKey = []

def Playfair_Encrypt(key, plaintext):
    #If the plaintext is a string to be encrypted:
    if (isinstance(plaintext,str)):
        #Test if the key is < 24 characters
        if (len(key) > 24):
            raise Exception("Key is too long, number of key characters > 24")
        key = key.lower()

        keyMatrix = generatePlayfairKeyAlpha(key)

        #Go through the plaintext, adding x's where two characters are in the same diagram
        plaintextCorrected = ""

        index = 1
        #Variable stores the index of up to where the plaintext has been added to plaintextCorrected:
        indexConverted = 0
        while (index < len(plaintext)):
            if (plaintext[index] == plaintext[index-1]):
                plaintextCorrected += (plaintext[index-1])
                plaintextCorrected += ('x')
                plaintextCorrected += (plaintext[index])
                indexConverted = index
                index += 1
            else:
                plaintextCorrected += (plaintext[index - 1])
                plaintextCorrected += (plaintext[index])
                indexConverted = index
                index += 2

        #Add the possible last character that wasn't added because it is not part of diagram
        indexConverted += 1
        while (indexConverted < len(plaintext)):
            plaintextCorrected += plaintext[indexConverted]
            indexConverted += 1

        #If the number of symbols in the plaintext is not even add a trailing x:
        if not(len(plaintextCorrected) % 2 == 0):
            plaintextCorrected += ('x')

        #Replace all j's with i's:
        plaintextCorrected.replace('j','i')

        #================================================
        # Begin encoding algorithm

        cipherText = ""

        diagramIndex = 0
        #Row and column where the first letter is found in the keyMatrix
        rowF = 0
        columnF = 0
        #Row and column where the second letter is found in the keyMatrix
        rowS = 0
        columnS = 0

        while (diagramIndex < len(plaintextCorrected)):
            firstLetter = plaintextCorrected[diagramIndex]
            secondLetter = plaintextCorrected[diagramIndex+1]

            rowSearch = 0
            columnSearch = 0
            bFoundFirst = False
            bFoundSecond = False
            #Find the row and column of the two letters in the diagram in the key matrix:
            while ((rowSearch < 5) and (not(bFoundFirst) or not(bFoundSecond))):
                if (keyMatrix[rowSearch][columnSearch] == firstLetter):
                    rowF = rowSearch
                    columnF = columnSearch
                    bFoundFirst = True
                elif (keyMatrix[rowSearch][columnSearch] == secondLetter):
                    rowS = rowSearch
                    columnS = columnSearch
                    bFoundSecond = True

                # Update the matrix indices
                columnSearch += 1
                if (columnSearch >= 5):
                    columnSearch = 0
                    rowSearch += 1

            #The letter's positions in the key matrix has been obtained

            #get the two ciphertext characters corresponding to the diagram:

            #If the two characters are in the same row of the key matrix:
            if (rowF == rowS):
                #add to the ciphertext the characters to the right in the key matrix
                cipherText += (keyMatrix[rowF][(columnF+1) % 5])
                cipherText += (keyMatrix[rowS][(columnS+1) % 5])

            #If the two characters are in the same column of the key matrix:
            elif (columnF == columnS):
                #add to the ciphertext the characters to the bottom in the key matrix
                cipherText += (keyMatrix[(rowF+1) % 5][columnF])
                cipherText += (keyMatrix[(rowS+1) % 5][columnS])
            else:
                #add to the ciphertext the character in the same row, but in its partner's column:
                cipherText += (keyMatrix[rowF][columnS])
                cipherText += (keyMatrix[rowS][columnF])

            #Go to the next diagram
            diagramIndex += 2

        return cipherText










    #If the plaintext is an image (ndarray) that needs to be encrypted:
    if (isinstance(plaintext,np.ndarray)):
        print("Hello2")

#Function cleans the input, removes any special characters (including spaces) and makes all letters lower case
def cleanInput(input):

    input = input.lower();

    alphabet= ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'];
    cleanedInput = ""
    for character in input:
        bAlphaLetter = False
        index = 0
        while (not(bAlphaLetter) and (index < len(alphabet))):
            if (character == alphabet[index]):
                bAlphaLetter = True
            index += 1
        if (bAlphaLetter):
            cleanedInput = cleanedInput + character

    return cleanedInput

def toNumber(letter):
    return ord(letter) - 96

def generatePlayfairKeyAlpha(characterKey):
    # Generate the key:
    alphabet = ['a','b','c','d','e','f','g','h','i','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    characterKey = characterKey.lower()

    #Change all j's to i's in the key:
    characterKey.replace('j','i')

    charKeyMatrix = np.empty((5, 5), dtype='U1')
    alreadyIn = []
    #Iterators:
    row = 0
    column = 0
    for character in characterKey:
        if not(character in alreadyIn):
            charKeyMatrix[row][column] = character
            alreadyIn += (character)
            #I and J together in same bin:
            if ((character == 'i') or (character == 'j')):
                #Add both as it does not matter if they are repeated
                alreadyIn += 'i'
                alreadyIn += 'j'

            #Update the matrix indices
            column += 1
            if (column >= 5):
                column = 0
                row += 1

    #Fill in the rest of the key matrix with the leftover alphabetic letters
    alphabetIndex = 0
    while (row < 5):
        if not(alphabet[alphabetIndex] in alreadyIn):
            charKeyMatrix[row][column] = alphabet[alphabetIndex]

            #Update the matrix indices
            column += 1
            if (column >= 5):
                column = 0
                row += 1

        #Go to next alphabet letter
        alphabetIndex += 1

    return charKeyMatrix







Playfair_Encrypt("Hello","Mamma")
print(cleanInput("Hi!, //@@ Hoe gaan dit vandag met jou?"))

print(toNumber('a'))

print(generatePlayfairKeyAlpha("Hj"))

print(Playfair_Encrypt("monarchy","instruments"))