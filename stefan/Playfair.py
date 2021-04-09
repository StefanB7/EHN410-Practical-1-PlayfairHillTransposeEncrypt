#EHN 410 - Practical 1 - 2021
#Playfair encryption and decryption
#Group 7
#Created: 2 April 2021

import numpy as np
import string

from PIL import Image
from numpy import asarray

playfairKey = []

#Playfair encryption algorithm
def Playfair_Encrypt(key, plaintext):
    # Test if the key is < 24 characters
    if (len(key) > 24):
        raise Exception("Key is too long, number of key characters > 24")
    key = key.lower()

    #If the plaintext is a string to be encrypted:
    if (isinstance(plaintext,str)):

        keyMatrix = generatePlayfairKeyAlpha(key)

        #Clean the plaintext
        plaintext = cleanInput(plaintext)

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
                index += 2
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
        #Copy the plaintext:
        plainTextCopy = plaintext.copy()
        
        #Get the necryption key matrix:
        keyMatrix = generatePlayfairKeyArray(key)

        #Check the plaintext's dimentions:
        numRows = plaintext.shape[0]
        numColumns = plaintext.shape[1]
        if (plaintext.ndim == 2):
            numLayers = 1
        else:
            numLayers = plaintext.shape[2]

        #Test if there is an AlphaLayer:
        bAlphaLayer = False
        if (numLayers > 3):
            bAlphaLayer = True
            numLayers = 3
            
        #TODO:Check the incoming array's dimentions

        #Ciphertext variable:
        cipherText = np.zeros((numRows, numColumns, numLayers), dtype='u1')
        
        #For the case when layers are 3:
        if numLayers == 3:
            
            #Calculate the least probable pixel value for the given layer:
            leastValuesCount = [0] * 256
            columnLeast = 0
            rowLeast = 0
            layerLeast = 0
            
            while rowLeast < numRows:
                leastValuesCount[plainTextCopy[rowLeast][columnLeast][layerLeast]] += 1
                rowLeast, columnLeast, layerLeast = incrementLayerColumnRow(rowLeast, columnLeast, layerLeast, numRows, numColumns, numLayers, 1)
                
            #255 should not be chosen as it does not have a +1:
            leastValuesCount[255] = max(leastValuesCount)
                
            #The value that occurs the least will be assigned the placeholder:
            leastValue = leastValuesCount.index(min(leastValuesCount))
            
            #Assign the red value of the first pixel to the leastValue:
            plainTextCopy[0][0][0] = leastValue
                
            #Go through the entire matrix, incrementing the least value:
            columnLeast = 0
            rowLeast = 0
            layerLeast = 1  #Skip the first element (where it is stored)
            
            while rowLeast < numRows:
                if plainTextCopy[rowLeast][columnLeast][layerLeast] == leastValue:
                    plainTextCopy[rowLeast][columnLeast][layerLeast] += 1
                rowLeast, columnLeast, layerLeast = incrementLayerColumnRow(rowLeast, columnLeast, layerLeast, numRows, numColumns, numLayers, 1)
                
            #Encryption algorithm:
            diagramIndexRowFirst = 0
            diagramIndexColumnFirst = 0
            diagramLayerFirst = 0

            diagramIndexRowSecond = 0
            diagramIndexColumnSecond = 0
            diagramLayerSecond = 1
        
            #Iterate over all the diagrams:
            while diagramIndexRowSecond < numRows:
                valueFirst = plainTextCopy[diagramIndexRowFirst][diagramIndexColumnFirst][diagramLayerFirst]
                valueSecond = plainTextCopy[diagramIndexRowSecond][diagramIndexColumnSecond][diagramLayerSecond]
                
                #If the values are the same, replace the second value with the least occurring value (placeholder, calculated above):
                if (valueFirst == valueSecond):
                    valueSecond = leastValue
                    
                # Row and column where the first letter is found in the keyMatrix
                rowF = 0
                columnF = 0
                # Row and column where the second letter is found in the keyMatrix
                rowS = 0
                columnS = 0
            
                #Search for the first and second values of the diagram in the key matrix:
                bFoundFirst = False
                bFoundSecond = False
                rowSearch = 0
                columnSearch = 0
                while (rowSearch < 16) and (not(bFoundFirst) or not(bFoundSecond)):
                    if (valueFirst == keyMatrix[rowSearch][columnSearch]):
                        rowF = rowSearch
                        columnF = columnSearch
                        bFoundFirst = True
                    if (valueSecond == keyMatrix[rowSearch][columnSearch]):
                        rowS = rowSearch
                        columnS = columnSearch
                        bFoundSecond = True

                    # Update the matrix indices
                    columnSearch += 1
                    if (columnSearch >= 16):
                        columnSearch = 0
                        rowSearch += 1
                        
                # The value's positions in the key matrix have been obtained

                # get the two ciphertext characters corresponding to the diagram:
                
                # If the two characters are in the same row of the key matrix:
                if (rowF == rowS):
                    # add to the ciphertext the characters to the right in the key matrix
                    cipherText[diagramIndexRowFirst][diagramIndexColumnFirst][diagramLayerFirst] = keyMatrix[rowF][(columnF + 1) % 16]
                    cipherText[diagramIndexRowSecond][diagramIndexColumnSecond][diagramLayerSecond] = keyMatrix[rowS][(columnS + 1) % 16]

                # If the two characters are in the same column of the key matrix:
                elif (columnF == columnS):
                    # add to the ciphertext the characters to the bottom in the key matrix
                    cipherText[diagramIndexRowFirst][diagramIndexColumnFirst][diagramLayerFirst] = keyMatrix[(rowF+1)%16][columnF]
                    cipherText[diagramIndexRowSecond][diagramIndexColumnSecond][diagramLayerSecond] = keyMatrix[(rowS+1)%16][columnS]
                else:
                    # add to the ciphertext the character in the same row, but in its partner's column:
                    cipherText[diagramIndexRowFirst][diagramIndexColumnFirst][diagramLayerFirst] = keyMatrix[rowF][columnS]
                    cipherText[diagramIndexRowSecond][diagramIndexColumnSecond][diagramLayerSecond] = keyMatrix[rowS][columnF]

                diagramIndexRowFirst, diagramIndexColumnFirst, diagramLayerFirst = incrementLayerColumnRow(diagramIndexRowFirst,diagramIndexColumnFirst,diagramLayerFirst,numRows,numColumns,numLayers,2)
                diagramIndexRowSecond, diagramIndexColumnSecond, diagramLayerSecond = incrementLayerColumnRow(diagramIndexRowSecond,diagramIndexColumnSecond,diagramLayerSecond,numRows,numColumns,numLayers,2)

        
            return cipherText
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        



        return cipherText






def incrementRowColumn(currentRow, currentColumn, totalRows, totalColumns, numIncrement):
    returnColumn = currentColumn + numIncrement
    if returnColumn >= totalColumns:
        returnRow = currentRow + 1
        returnColumn = returnColumn - totalColumns
    else:
        returnRow = currentRow

    return returnRow, returnColumn

def incrementLayerColumnRow(currentRow,currentColumn,currentLayer,totalRows,totalColumns,totalLayers,numIncrement):
    returnRow = currentRow
    returnColumn = currentColumn    
    returnLayer = currentLayer + numIncrement
    if returnLayer >= totalLayers:
        returnLayer = returnLayer - totalLayers
        returnColumn = currentColumn + 1
        if returnColumn >= totalColumns:
            returnColumn = returnColumn - totalColumns
            returnRow = currentRow + 1
            
    return returnRow, returnColumn, returnLayer






























#Playfair decryption algorithm
def Playfair_Decrypt(key, ciphertext):
    # Test if the key is < 24 characters
    if (len(key) > 24):
        raise Exception("Key is too long, number of key characters > 24")
    key = key.lower()


    if (isinstance(ciphertext, str)):

        keyMatrix = generatePlayfairKeyAlpha(key)

        #Clean the ciphertext:
        ciphertext = cleanInput(ciphertext)

        #================================================
        # Begin decoding algorithm

        plainText = ""

        diagramIndex = 0

        #Row and column where the first letter is found in the keyMatrix
        rowF = 0
        columnF = 0
        #Row and column where the second letter is found in the keyMatrix
        rowS = 0
        columnS = 0

        while (diagramIndex < len(ciphertext)):
            firstLetter = ciphertext[diagramIndex]
            secondLetter = ciphertext[diagramIndex+1]

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

            # The letter's positions in the key matrix has been obtained

            #Get the plaintext characters corresponding to the ciphertext diagram:
            # If the two characters are in the same row of the key matrix:
            if (rowF == rowS):
                # add to the plainText the characters to the left in the key matrix
                plainText += (keyMatrix[rowF][(columnF - 1) % 5])
                plainText += (keyMatrix[rowS][(columnS - 1) % 5])

            # If the two characters are in the same column of the key matrix:
            elif (columnF == columnS):
                # add to the plainText the characters to the bottom in the key matrix
                plainText += (keyMatrix[(rowF - 1) % 5][columnF])
                plainText += (keyMatrix[(rowS - 1) % 5][columnS])
            else:
                # add to the plainText the character in the same row, but in its partner's column:
                plainText += (keyMatrix[rowF][columnS])
                plainText += (keyMatrix[rowS][columnF])

            # Go to the next diagram
            diagramIndex += 2

        #TODO: Find out if this is necessary
        #Remove the x's that were placed at repeating letters:

        plainTextCopy = plainText
        plainText = ""
        index = 0

        while (index < len(plainTextCopy)):
            #If there are enough space left on the end to include index's double letter and x: (index+2)
            if (index + 2 < len(plainTextCopy)):
                #If double and x between them, skip the x
                if ((plainTextCopy[index+1] == 'x') and (plainTextCopy[index] == plainTextCopy[index+2])):
                    plainText += plainTextCopy[index]
                    index += 2
                else:
                    #If not double just add the letter
                    plainText += plainTextCopy[index]
                    index += 1
            else:
                #Last few characters are added, those with (index + 2 < len(plainTextCopy))
                plainText += plainTextCopy[index]
                index += 1

        return plainText







    #If the ciphertext is an image (ndarray) that needs to be encrypted:
    if (isinstance(ciphertext,np.ndarray)):
        print("Playfair Decrypt met ndarray ciphertext")












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
    return ord(letter) - 97

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

def generatePlayfairKeyArray(characterKey):
    #Generate the key

    characterKey = characterKey.lower()

    keyMatrix = np.empty((16, 16), dtype='u1')
    alreadyIn = []
    #Iterators:
    row = 0
    column = 0
    for character in characterKey:
        characterNum = toNumber(character)

        if not(characterNum in alreadyIn):
            keyMatrix[row][column] = characterNum
            alreadyIn.append(characterNum)

            #Update the matrix indices
            column += 1
            if (column >= 16):
                column = 0
                row += 1

    #Fill in the rest of the key matrix with the remaining values up to 255:
    index = 0
    while (row < 16):
        if not(index in alreadyIn):
            keyMatrix[row][column] = index
            alreadyIn.append(index)

            #Update the matrix indices
            column += 1
            if (column >= 16):
                column = 0
                row += 1

        #Test next value
        index += 1

    return keyMatrix










Playfair_Encrypt("Hello","Mamma")
print(cleanInput("Hi!, //@@ Hoe gaan dit vandag met jou?"))

print(toNumber('a'))

print(generatePlayfairKeyAlpha("monarchy"))

print(Playfair_Encrypt("monarchy","Helloi"))

print(Playfair_Decrypt("monarchy","cfsupmsa"))

print(generatePlayfairKeyArray("Stefan"))

row, column = incrementRowColumn(0,0,2,2,3)
print(row)
print(column)


#Images:
image = Image.open('office.png')

data = asarray(image)

dataBack = Playfair_Encrypt("Stefan",data)

image2 = Image.fromarray(dataBack).save("encypted.jpeg")