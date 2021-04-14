# Stefan Buys (u18043098), Jacobus Oettle (u18000135) - University of Pretoria
# EHN 410 - 2021

from PIL import Image
import numpy as np
import string
from numpy import asarray


############################################################
#                   PLAYFAIR CIPHER                        #
############################################################

############################ Main Functions: ##########################

# Playfair encryption algorithm
def Playfair_Encrypt(key, plaintext):
    # Test if the key is < 24 characters
    if (len(key) > 24):
        raise Exception("Key is too long, number of key characters > 24")
    key = key.lower()

    #### Plaintext Encoding ####

    # If the plaintext is a string to be encrypted:
    if (isinstance(plaintext, str)):

        keyMatrix = generatePlayfairKeyAlpha(key)

        # Clean the plaintext
        plaintext = cleanInput(plaintext)

        # Replace the j's with i's:
        plaintext = plaintext.replace('j', 'i')

        # Go through the plaintext, adding x's where two characters are in the same diagram
        plaintextCorrected = ""

        index = 1
        # Variable stores the index of up to where the plaintext has been added to plaintextCorrected:
        indexConverted = 0
        while (index < len(plaintext)):
            if (plaintext[index] == plaintext[index - 1]):
                plaintextCorrected += (plaintext[index - 1])
                plaintextCorrected += ('x')
                indexConverted = index
                index += 1
            else:
                plaintextCorrected += (plaintext[index - 1])
                plaintextCorrected += (plaintext[index])
                indexConverted = index
                index += 2

        # Edge-case, if the length of the plaintext is 1, add the plaintext character to plaintextCorrected
        if len(plaintext) == 1:
            plaintextCorrected = plaintext[0];

        # Add the possible last character that wasn't added because it is not part of diagram
        indexConverted += 1
        while (indexConverted < len(plaintext)):
            plaintextCorrected += plaintext[indexConverted]
            indexConverted += 1

        # If the number of symbols in the plaintext is not even add a trailing x:
        if not (len(plaintextCorrected) % 2 == 0):
            plaintextCorrected += ('x')

        # Replace all j's with i's:
        plaintextCorrected.replace('j', 'i')

        # ================================================
        # Begin encoding algorithm

        cipherText = ""

        diagramIndex = 0
        # Row and column where the first letter is found in the keyMatrix
        rowF = 0
        columnF = 0
        # Row and column where the second letter is found in the keyMatrix
        rowS = 0
        columnS = 0

        while (diagramIndex < len(plaintextCorrected)):
            firstLetter = plaintextCorrected[diagramIndex]
            secondLetter = plaintextCorrected[diagramIndex + 1]

            rowSearch = 0
            columnSearch = 0
            bFoundFirst = False
            bFoundSecond = False
            # Find the row and column of the two letters in the diagram in the key matrix:
            while ((rowSearch < 5) and (not (bFoundFirst) or not (bFoundSecond))):
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

            # get the two ciphertext characters corresponding to the diagram:

            # If the two characters are in the same row of the key matrix:
            if (rowF == rowS):
                # add to the ciphertext the characters to the right in the key matrix
                cipherText += (keyMatrix[rowF][(columnF + 1) % 5])
                cipherText += (keyMatrix[rowS][(columnS + 1) % 5])

            # If the two characters are in the same column of the key matrix:
            elif (columnF == columnS):
                # add to the ciphertext the characters to the bottom in the key matrix
                cipherText += (keyMatrix[(rowF + 1) % 5][columnF])
                cipherText += (keyMatrix[(rowS + 1) % 5][columnS])
            else:
                # add to the ciphertext the character in the same row, but in its partner's column:
                cipherText += (keyMatrix[rowF][columnS])
                cipherText += (keyMatrix[rowS][columnF])

            # Go to the next diagram
            diagramIndex += 2

        return cipherText

    #### Image Encoding ####

    # If the plaintext is an image (ndarray) that needs to be encrypted:
    if (isinstance(plaintext, np.ndarray)):
        # Copy the plaintext:
        plainTextCopy = plaintext.copy()

        # Get the necryption key matrix:
        keyMatrix = generatePlayfairKeyArray(key)

        # Check the plaintext's dimentions:
        numRows = plaintext.shape[0]
        numColumns = plaintext.shape[1]
        numLayers = plaintext.shape[2]

        # Test if there is an AlphaLayer:
        bAlphaLayer = False
        if (numLayers > 3):
            bAlphaLayer = True
            numLayers = 3
            alpha_layer = np.array(plaintext[:, :, 3])

        # Ciphertext variable:
        cipherText = np.zeros((numRows, numColumns, numLayers), dtype='u1')

        for layer in range(numLayers):
            # Calculate the least probable pixel value for the given layer:
            leastValuesCount = [0] * 256
            columnLeast = 0
            rowLeast = 0

            while rowLeast < numRows:
                leastValuesCount[plainTextCopy[rowLeast][columnLeast][layer]] += 1
                rowLeast, columnLeast = incrementRowColumn(rowLeast, columnLeast, numRows, numColumns, 1)

            # 255 should not be chosen as it does not have a +1:
            leastValuesCount[255] = max(leastValuesCount)

            # The value that occurs the least will be assigned the placeholder:
            leastValue = leastValuesCount.index(min(leastValuesCount))

            # Go through the entire matrix, incrementing the least value:
            columnLeast = 1
            rowLeast = 0

            while rowLeast < numRows:
                if plainTextCopy[rowLeast][columnLeast][layer] == leastValue:
                    plainTextCopy[rowLeast][columnLeast][layer] += 1
                rowLeast, columnLeast = incrementRowColumn(rowLeast, columnLeast, numRows, numColumns, 1)

            # Assign the red value of the first pixel to the leastValue:
            plainTextCopy[0][0][layer] = leastValue

            # Encryption algorithm:
            diagramIndexRowFirst = 0
            diagramIndexColumnFirst = 0

            diagramIndexRowSecond = 0
            diagramIndexColumnSecond = 1

            # Iterate over all the diagrams:
            while diagramIndexRowSecond < numRows:
                valueFirst = plainTextCopy[diagramIndexRowFirst][diagramIndexColumnFirst][layer]
                valueSecond = plainTextCopy[diagramIndexRowSecond][diagramIndexColumnSecond][layer]

                # If the values are the same, replace the second value with the least occurring value (placeholder, calculated above):
                if (valueFirst == valueSecond):
                    valueSecond = leastValue

                # Row and column where the first letter is found in the keyMatrix
                rowF = 0
                columnF = 0
                # Row and column where the second letter is found in the keyMatrix
                rowS = 0
                columnS = 0

                # Search for the first and second values of the diagram in the key matrix:
                bFoundFirst = False
                bFoundSecond = False
                rowSearch = 0
                columnSearch = 0
                while (rowSearch < 16) and (not (bFoundFirst) or not (bFoundSecond)):
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
                    cipherText[diagramIndexRowFirst][diagramIndexColumnFirst][layer] = keyMatrix[rowF][
                        (columnF + 1) % 16]
                    cipherText[diagramIndexRowSecond][diagramIndexColumnSecond][layer] = \
                        keyMatrix[rowS][(columnS + 1) % 16]

                # If the two characters are in the same column of the key matrix:
                elif (columnF == columnS):
                    # add to the ciphertext the characters to the bottom in the key matrix
                    cipherText[diagramIndexRowFirst][diagramIndexColumnFirst][layer] = \
                        keyMatrix[(rowF + 1) % 16][columnF]
                    cipherText[diagramIndexRowSecond][diagramIndexColumnSecond][layer] = \
                        keyMatrix[(rowS + 1) % 16][columnS]
                else:
                    # add to the ciphertext the character in the same row, but in its partner's column:
                    cipherText[diagramIndexRowFirst][diagramIndexColumnFirst][layer] = keyMatrix[rowF][
                        columnS]
                    cipherText[diagramIndexRowSecond][diagramIndexColumnSecond][layer] = \
                        keyMatrix[rowS][columnF]

                diagramIndexRowFirst, diagramIndexColumnFirst = incrementRowColumn(diagramIndexRowFirst,
                                                                                   diagramIndexColumnFirst, numRows,
                                                                                   numColumns, 2)
                diagramIndexRowSecond, diagramIndexColumnSecond = incrementRowColumn(diagramIndexRowSecond,
                                                                                     diagramIndexColumnSecond, numRows,
                                                                                     numColumns, 2)

        if bAlphaLayer:
            cipherText = np.dstack((cipherText, alpha_layer))

        return cipherText.astype(int)


# Playfair decryption algorithm
def Playfair_Decrypt(key, ciphertext):
    # Test if the key is < 24 characters
    if (len(key) > 24):
        raise Exception("Key is too long, number of key characters > 24")
    key = key.lower()

    #### Plaintext Decoding ####

    if (isinstance(ciphertext, str)):

        keyMatrix = generatePlayfairKeyAlpha(key)

        # Clean the ciphertext:
        ciphertext = cleanInput(ciphertext)

        # ================================================
        # Begin decoding algorithm

        plainText = ""

        diagramIndex = 0

        # Row and column where the first letter is found in the keyMatrix
        rowF = 0
        columnF = 0
        # Row and column where the second letter is found in the keyMatrix
        rowS = 0
        columnS = 0

        while (diagramIndex < len(ciphertext)):
            firstLetter = ciphertext[diagramIndex]
            secondLetter = ciphertext[diagramIndex + 1]

            rowSearch = 0
            columnSearch = 0
            bFoundFirst = False
            bFoundSecond = False
            # Find the row and column of the two letters in the diagram in the key matrix:
            while ((rowSearch < 5) and (not (bFoundFirst) or not (bFoundSecond))):
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

            # Get the plaintext characters corresponding to the ciphertext diagram:
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

        # TODO: Find out if this is necessary
        # Remove the x's that were placed at repeating letters:

        plainTextCopy = plainText
        plainText = ""
        index = 0

        while (index < len(plainTextCopy)):
            # If there are enough space left on the end to include index's double letter and x: (index+2)
            if (index + 2 < len(plainTextCopy)):
                # If double and x between them, skip the x
                if ((plainTextCopy[index + 1] == 'x') and (plainTextCopy[index] == plainTextCopy[index + 2])):
                    plainText += plainTextCopy[index]
                    index += 2
                else:
                    # If not double just add the letter
                    plainText += plainTextCopy[index]
                    index += 1
            else:
                # Last few characters are added, those with (index + 2 < len(plainTextCopy))
                plainText += plainTextCopy[index]
                index += 1

        return plainText

    #### Image Decoding ####

    # If the ciphertext is an image (ndarray) that needs to be decrypted:
    if (isinstance(ciphertext, np.ndarray)):
        # Copy the plaintext:
        cipherTextCopy = ciphertext.copy()

        # Get the encryption key matrix:
        keyMatrix = generatePlayfairKeyArray(key)

        # Check the plaintext's dimentions:
        numRows = ciphertext.shape[0]
        numColumns = ciphertext.shape[1]
        numLayers = ciphertext.shape[2]

        # Test if there is an AlphaLayer:
        # Test if there is an AlphaLayer:
        bAlphaLayer = False
        if (numLayers > 3):
            bAlphaLayer = True
            numLayers = 3
            alpha_layer = np.array(ciphertext[:, :, 3])

        # Ciphertext variable:
        plainText = np.zeros((numRows, numColumns, numLayers), dtype='u1')

        for layer in range(numLayers):

            # Get the layer's least occuring value (used as the filler symbol):
            leastValue = -1

            # Decryption algorithm:
            diagramIndexRowFirst = 0
            diagramIndexColumnFirst = 0

            diagramIndexRowSecond = 0
            diagramIndexColumnSecond = 1

            # Iterate over all the diagrams:
            while diagramIndexRowSecond < numRows:
                valueFirst = cipherTextCopy[diagramIndexRowFirst][diagramIndexColumnFirst][layer]
                valueSecond = cipherTextCopy[diagramIndexRowSecond][diagramIndexColumnSecond][layer]

                # Row and column where the first letter is found in the keyMatrix
                rowF = 0
                columnF = 0
                # Row and column where the second letter is found in the keyMatrix
                rowS = 0
                columnS = 0

                # Search for the first and second values of the diagram in the key matrix:
                bFoundFirst = False
                bFoundSecond = False
                rowSearch = 0
                columnSearch = 0
                while (rowSearch < 16) and (not (bFoundFirst) or not (bFoundSecond)):
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

                # get the two plaintext characters corresponding to the diagram:

                # If the two characters are in the same row of the key matrix:
                if (rowF == rowS):
                    # add to the ciphertext the characters to the right in the key matrix
                    plainText[diagramIndexRowFirst][diagramIndexColumnFirst][layer] = keyMatrix[rowF][
                        (columnF - 1) % 16]
                    plainText[diagramIndexRowSecond][diagramIndexColumnSecond][layer] = keyMatrix[rowS][
                        (columnS - 1) % 16]

                # If the two characters are in the same column of the key matrix:
                elif (columnF == columnS):
                    # add to the ciphertext the characters to the bottom in the key matrix
                    plainText[diagramIndexRowFirst][diagramIndexColumnFirst][layer] = keyMatrix[(rowF - 1) % 16][
                        columnF]
                    plainText[diagramIndexRowSecond][diagramIndexColumnSecond][layer] = keyMatrix[(rowS - 1) % 16][
                        columnS]
                else:
                    # add to the ciphertext the character in the same row, but in its partner's column:
                    plainText[diagramIndexRowFirst][diagramIndexColumnFirst][layer] = keyMatrix[rowF][columnS]
                    plainText[diagramIndexRowSecond][diagramIndexColumnSecond][layer] = keyMatrix[rowS][columnF]

                # If the first element was just decrypted, save it as the least occurring (filler) symbol:
                if (diagramIndexRowFirst == 0) and (diagramIndexColumnFirst == 0):
                    leastValue = plainText[0][0][layer]

                # If the second value in the diagram is equal to the filler symbol, copy the first element in the diagram to the second element in the diagram:
                if plainText[diagramIndexRowSecond][diagramIndexColumnSecond][layer] == leastValue:
                    plainText[diagramIndexRowSecond][diagramIndexColumnSecond][layer] = \
                    plainText[diagramIndexRowFirst][diagramIndexColumnFirst][layer]

                # Increment the diagram indexes (go to the next diagram)
                diagramIndexRowFirst, diagramIndexColumnFirst = incrementRowColumn(diagramIndexRowFirst,
                                                                                   diagramIndexColumnFirst, numRows,
                                                                                   numColumns, 2)
                diagramIndexRowSecond, diagramIndexColumnSecond = incrementRowColumn(diagramIndexRowSecond,
                                                                                     diagramIndexColumnSecond, numRows,
                                                                                     numColumns, 2)

        if bAlphaLayer:
            plainText = np.dstack((plainText, alpha_layer))

        return plainText.astype(int)


def Get_Playfair_Encryption_Matrix():
    return playfairKey


############################ Helper Functions: ##########################

# Function cleans the input, removes any special characters (including spaces) and makes all letters lower case
def cleanInput(input):
    input = input.lower();

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'];
    cleanedInput = ""
    for character in input:
        bAlphaLetter = False
        index = 0
        while (not (bAlphaLetter) and (index < len(alphabet))):
            if (character == alphabet[index]):
                bAlphaLetter = True
            index += 1
        if (bAlphaLetter):
            cleanedInput = cleanedInput + character

    return cleanedInput


def toNumber(letter):
    return ord(letter) - 97


def incrementRowColumn(currentRow, currentColumn, totalRows, totalColumns, numIncrement):
    returnColumn = currentColumn + numIncrement
    if returnColumn >= totalColumns:
        returnRow = currentRow + 1
        returnColumn = returnColumn - totalColumns
    else:
        returnRow = currentRow

    return returnRow, returnColumn


def generatePlayfairKeyAlpha(characterKey):
    global playfairKey

    # Generate the key:
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                'w', 'x', 'y', 'z']
    characterKey = characterKey.lower()

    # Change all j's to i's in the key:
    characterKey = characterKey.replace('j', 'i')

    charKeyMatrix = np.empty((5, 5), dtype='U1')
    alreadyIn = []
    # Iterators:
    row = 0
    column = 0
    for character in characterKey:
        if not (character in alreadyIn):
            charKeyMatrix[row][column] = character
            alreadyIn += (character)
            # I and J together in same bin:
            if ((character == 'i') or (character == 'j')):
                # Add both as it does not matter if they are repeated
                alreadyIn += 'i'
                alreadyIn += 'j'

            # Update the matrix indices
            column += 1
            if (column >= 5):
                column = 0
                row += 1

    # Fill in the rest of the key matrix with the leftover alphabetic letters
    alphabetIndex = 0
    while (row < 5):
        if not (alphabet[alphabetIndex] in alreadyIn):
            charKeyMatrix[row][column] = alphabet[alphabetIndex]

            # Update the matrix indices
            column += 1
            if (column >= 5):
                column = 0
                row += 1

        # Go to next alphabet letter
        alphabetIndex += 1

    # Store the result in the global playfair key
    playfairKey = charKeyMatrix.copy()

    return charKeyMatrix


def generatePlayfairKeyArray(characterKey):
    global playfairKey

    # Generate the key
    keyMatrix = np.zeros((16, 16), 'u1')

    # Get value indexes of the characterKey:
    keyList = []
    for character in characterKey:
        keyList.append(toNumber(character))

    permutations = [-1] * 256

    indexInKey = 0

    for indexPermutation in range(256):
        positionPermutation = (indexPermutation + (keyList[indexInKey] * 9)) % 256
        indexInKey = (indexInKey + 1) % len(characterKey)

        # If the position is available:
        if permutations[positionPermutation] == -1:
            # Add the value to the position:
            permutations[positionPermutation] = indexPermutation
        else:
            # The position is not available search for an available position after this position:
            indexSearch = (positionPermutation + 1) % 256
            bPositionFound = False
            while not (bPositionFound):
                if permutations[indexSearch] == -1:
                    bPositionFound = True
                    permutations[indexSearch] = indexPermutation
                indexSearch = (indexSearch + 1) % 256

    # Populate the keyMatrix with the permutations, containing all values from 0 - 255:
    diagonal = 15
    row = 15
    column = 0

    for value in permutations:
        keyMatrix[row][column] = value

        if diagonal > 0:
            column += 1
            row += 1
            if (row >= 16):
                column = 0
                diagonal -= 1
                row = diagonal
        else:
            column += 1
            row += 1
            if (column >= 16):
                row = 0
                diagonal -= 1
                column = abs(diagonal)

    # Store the result in the global playfair key
    playfairKey = keyMatrix.copy().astype(float)

    return keyMatrix



############################################################
#                      HILL CIPHER                         #
############################################################
 
############################ Main functions: ############################

# Hill_Encrypt (key : String, plaintext : String or Int ndarray)
def Hill_Encrypt(key, plaintext):
    if len(key) == 4:
        m = 2
    elif len(key) == 9:
        m = 3

    C = []

    global K
    K = __makeMatrix(key)
    
    flag_small = False

    # plaintext encryption
    if type(plaintext) is not np.ndarray:
        P = __cleanString(plaintext)

        # plaintext not long enough to be encrypted
        while len(P) < m:
            flag_small = True
            P = np.concatenate((P,[23]), axis=None)
        
        if flag_small == True:
            P = P[:m]
            print("\nWARNING: plaintext length too short, plaintext filled with 'x'...\n")

        
        int_l = len(P)
        # if the plaintext length is not a multiple of m, concatenated the string with X's
        if len(P) != (m*(len(P)//m)):
            print("\nWARNING: plaintext length too short, plaintext filled with 'x'...\n")
            arrX = np.array([23]*len(P))
            P = np.concatenate((P,arrX), axis=None)
            P = P[:m*(int_l//m)+m]
        
        # encrypt plaintext
        for i in range(len(P) // m):
            C = np.concatenate((C, np.mod(np.dot(P[m*i:m*i+m], K), 26)), axis=None)

        return __arrayToString(C)

    # image encryption
    else:
        # exctract RGB
        P = plaintext
        
        r_channel = np.array(plaintext[:,:,0]).reshape(1,plaintext[:,:,0].shape[0]*plaintext[:,:,0].shape[1])[0]
        g_channel = np.array(plaintext[:,:,1]).reshape(1,plaintext[:,:,1].shape[0]*plaintext[:,:,1].shape[1])[0]
        b_channel = np.array(plaintext[:,:,2]).reshape(1,plaintext[:,:,2].shape[0]*plaintext[:,:,2].shape[1])[0]

        r_enc = []
        g_enc = []
        b_enc = []

        flag_small_r = False
        flag_small_g = False
        flag_small_b = False

        # if not enough pixels to be encrypted
        while len(r_channel) < m:
            flag_small_r = True
            r_channel = np.concatenate((r_channel,r_channel), axis=None)
        
        if flag_small_r == True:
            r_channel = r_channel[:m]
            print("\nWARNING: Not enough pixels, image pixels were repeated...\n")
        
        while len(g_channel) < m:
            flag_small_g = True
            g_channel = np.concatenate((g_channel,g_channel), axis=None)
        
        if flag_small_g == True:
            g_channel = g_channel[:m]
        
        while len(b_channel) < m:
            flag_small_b = True
            b_channel = np.concatenate((b_channel,b_channel), axis=None)
        
        if flag_small_b == True:
            b_channel = b_channel[:m]

        # Encrypt RGB channels
        for i in range(len(r_channel) // m):
            r_enc = np.concatenate((r_enc,np.mod(np.dot(r_channel[m*i:m*i+m], K),256)), axis=None)

        for j in range(len(g_channel) // m):
            g_enc = np.concatenate((g_enc,np.mod(np.dot(g_channel[m*j:m*j+m], K),256)), axis=None)
        for k in range(len(b_channel) // m):
            b_enc = np.concatenate((b_enc,np.mod(np.dot(b_channel[m*k:m*k+m], K),256)), axis=None)
        # Pixels that were not encrypted are attached without encryption
        if len(r_channel) != len(r_enc):
            print("\nWARNING: Not enough pixels, some (less than 3) image pixels were not encrypted...\n")
            r_enc = np.concatenate((r_enc,r_channel[len(r_enc)::]),axis=None)
        if len(g_channel) != len(g_enc):
            g_enc = np.concatenate((g_enc,g_channel[len(g_enc)::]),axis=None)
        if len(b_channel) != len(b_enc):
            b_enc = np.concatenate((b_enc,b_channel[len(b_enc)::]),axis=None)

        # reshape RGB channels into matrix form
        if flag_small_r == True:
            r_enc = r_enc.reshape(m,1)
            g_enc = g_enc.reshape(m,1)
            b_enc = b_enc.reshape(m,1)
        else:
            r_enc = r_enc.reshape(plaintext[:,:,0].shape[0],plaintext[:,:,0].shape[1])
            g_enc = g_enc.reshape(plaintext[:,:,1].shape[0],plaintext[:,:,1].shape[1])
            b_enc = b_enc.reshape(plaintext[:,:,2].shape[0],plaintext[:,:,2].shape[1])

        # Combine RGB matrices into one array

        if plaintext.shape[2] == 4:
            alpha_layer = np.array(plaintext[:,:,3])
            return np.dstack((r_enc.astype(int),g_enc.astype(int),b_enc.astype(int),alpha_layer.astype(int)))
        else:
            return np.dstack((r_enc.astype(int),g_enc.astype(int),b_enc.astype(int)))

# Hill_Decrypt (key : String, ciphertext : String or Int ndarray)
def Hill_Decrypt(key, ciphertext):

    if len(key) == 4:
        m = 2
    elif len(key) == 9:
        m = 3
    
    P = []
    K = __makeMatrix(key)
    
    # plaintext decryption
    if type(ciphertext) is not np.ndarray:
        C = __cleanString(ciphertext)
        K_inv = __inverse(m,K,False)

        # decryption
        for i in range(len(C) // m):
            P = np.concatenate((P, np.mod(np.dot(C[m*i:m*i+m], K_inv), 26)), axis=None)
        
        return __arrayToString(P)

     # image decryption
    else:
        C = ciphertext

        # extract RGB channels
        r_channel = np.array(ciphertext[:,:,0]).reshape(1,ciphertext[:,:,0].shape[0]*ciphertext[:,:,0].shape[1])[0]
        g_channel = np.array(ciphertext[:,:,1]).reshape(1,ciphertext[:,:,1].shape[0]*ciphertext[:,:,1].shape[1])[0]
        b_channel = np.array(ciphertext[:,:,2]).reshape(1,ciphertext[:,:,2].shape[0]*ciphertext[:,:,2].shape[1])[0]

        r_dec = []
        g_dec = []
        b_dec = []

        K_inv = __inverse(m,K,True)
        
        # decryption
        for i in range(len(r_channel) // m):       
            r_dec = np.concatenate((r_dec,np.mod(np.dot(r_channel[m*i:m*i+m], K_inv),256)), axis=None)
        for j in range(len(g_channel) // m):         
            g_dec = np.concatenate((g_dec,np.mod(np.dot(g_channel[m*j:m*j+m], K_inv),256)), axis=None)
        for k in range(len(b_channel) // m):
            b_dec = np.concatenate((b_dec,np.mod(np.dot(b_channel[m*k:m*k+m], K_inv),256)), axis=None)

        # Pixels that were not encrypted are attached without decryption 
        if len(r_channel) != len(r_dec):
            r_dec = np.concatenate((r_dec,r_channel[len(r_dec)::]),axis=None)
        if len(g_channel) != len(g_dec):
            g_dec = np.concatenate((g_dec,g_channel[len(g_dec)::]),axis=None)
        if len(b_channel) != len(b_dec):
            b_dec = np.concatenate((b_dec,b_channel[len(b_dec)::]),axis=None)

        # reshape RGB channels into matrix form
        r_dec = r_dec.reshape(ciphertext[:,:,0].shape[0],ciphertext[:,:,0].shape[1])
        g_dec = g_dec.reshape(ciphertext[:,:,1].shape[0],ciphertext[:,:,1].shape[1])
        b_dec = b_dec.reshape(ciphertext[:,:,2].shape[0],ciphertext[:,:,2].shape[1])

        # Combine RGB matrices into one array
        
        if ciphertext.shape[2] == 4:
            alpha_layer = np.array(ciphertext[:,:,3])
            return np.dstack((r_dec.astype(int),g_dec.astype(int),b_dec.astype(int),alpha_layer.astype(int)))
        else:
            return np.dstack((r_dec.astype(int),g_dec.astype(int),b_dec.astype(int)))

# Get_Hill_Encryption_Matrix ()
def Get_Hill_Encryption_Matrix():
    return K.astype(float)

############################ Helper functions: ##########################

def __cleanString(strText):
    s = strText.lower()
    s = ''.join(str(ord(i)-97)+',' for i in s if i.isalpha())
    return np.fromstring(s, dtype=int, sep=',')

def __makeMatrix(strKey):
    if len(strKey) == 4:
        return np.array(list(__cleanString(strKey))).reshape(2, 2)
    else:
        return np.array(list(__cleanString(strKey))).reshape(3, 3)

def __determinant(m, arrM):
    # determine the determinant of a matrix (2x2 or 3x3)
    if m == 2:
        d = arrM[0][0]*arrM[1][1]-arrM[1][0]*arrM[0][1]
    else:
        d = arrM[0][0]*arrM[1][1]*arrM[2][2] + arrM[1][0]*arrM[2][1]*arrM[0][2] + arrM[2][0]*arrM[0][1]*arrM[1][2] \
            - arrM[2][0]*arrM[1][1]*arrM[0][2] - arrM[1][0] * \
            arrM[0][1]*arrM[2][2] - arrM[0][0]*arrM[2][1]*arrM[1][2]

    return int(d)

def __inverseModulo(a,png):
    if png == True:
        for i in range(1,256):
            if (a*i)%256 == 1:
                return i
    else:
        for i in range(1,26):
            if (a*i)%26 == 1:
                return i
        
    # If the matrix determinant does not have a modular multiplicative inverse
    raise errorHillCipher("Key matrix determinant does not have modular multiplicative inverse")
    
def __inverse(m, arrM, png):
    inv = np.zeros(shape=(m, m))

    # image
    if png == True:
        det = __determinant(m, arrM)%256
        det = __inverseModulo(det,True)
    # text
    else:
        det = __determinant(m, arrM)%26
        det = __inverseModulo(det,False)

    for i in range(m):
        for j in range(m):
            Dij = arrM
            Dij = np.delete(Dij, i, axis=1)
            Dij = np.delete(Dij, j, axis=0)
            if m == 2:
                det_Dij = Dij
            else:
                det_Dij = __determinant(m-1, Dij)

            inv[i][j] = np.dot(((-1)**(i+j))*(det), det_Dij)

    if png == True:
        return np.mod(inv,256)
    else:
        return np.mod(inv,26)

def __arrayToString(arrString):
    return ''.join(chr(int(i)+97) for i in arrString)

############################ ERROR handler: #############################

class errorHillCipher(Exception):
    pass


############################################################
#                  TRANSPOSITION CIPHER                    #
############################################################

############################ Main functions: ############################

# Transpose_ Encrypt (key : String, stage : Int, plaintext : String)
def Transpose_Encrypt(key, stage, plaintext):

    K = __cleanStringInt(key)

    P = np.array(list(__cleanStringAlpha(plaintext)))

    flag_small = False

    # plaintext not long enough to be encrypted
    while len(P) < len(K):
        flag_small = True
        P = np.concatenate((P,['x']), axis=None)

    if flag_small == True:
        P = P[:len(K)]
        print("\nWARNING: plaintext length too short, plaintext filled with 'x'...\n")

    int_l = len(P)
    # if the plaintext length is not a multiple of m, concatenated the string with X's
    if len(P) != (len(K)*(len(P)//len(K))):
        print("\nWARNING: plaintext length too short, plaintext filled with 'x'...\n")
        arrX = np.array(['x']*len(P))
        P = np.concatenate((P,arrX), axis=None)
        P = P[:len(K)*(int_l//len(K))+len(K)]

    P = P.reshape(-1,(len(K)))

    C = []

    # 1 stage encryption
    for i in range(len(K)):
        pos = np.argmin(K)
        K[pos] = 99
        C = np.concatenate((C,P[:,pos]),axis=None)

    # 2 stage encryption
    if stage==2:
        P = C
        K = __cleanStringInt(key)
        P = P.reshape(-1,(len(K)))
        C = []

        for i in range(len(K)):
            pos = np.argmin(K)
            K[pos] = 99
            C = np.concatenate((C,P[:,pos]),axis=None)

    return "".join(C)
    
# Transpose_ Decrypt (key : String, stage : Int, ciphertext : String)
def Transpose_Decrypt(key, stage, ciphertext):
    
    K = __cleanStringInt(key)
    
    C = np.array(list(__cleanStringAlpha(ciphertext)))
    C = C.reshape((len(K),-1)).transpose()

    preP = np.empty(shape=(len(C[:,0]),len(K)),dtype=str)

    # 1 stage decryption
    for i in range(len(K)):
        pos = np.argmin(K)
        K[pos] = 99
        preP[:,pos] = C[:,i]

    preP = preP.reshape((1,-1))[0]

    P = "".join(preP)
    
    # 2 stage decryption
    if stage==2:
        C = np.array(list(__cleanStringAlpha(P)))
        K = __cleanStringInt(key)
        C = C.reshape((len(K),-1)).transpose()

        preP = np.empty(shape=(len(C[:,0]),len(K)),dtype=str)

        for i in range(len(K)):
            pos = np.argmin(K)
            K[pos] = 99
            preP[:,pos] = C[:,i]

        preP = preP.reshape((1,-1))[0]

        P = "".join(preP)

    return P

############################ Helper functions: ##########################
def __cleanStringInt(strText):
    s = strText.lower()
    s = ''.join(str(ord(i)-97)+',' for i in s if i.isalpha())
    return np.fromstring(s, dtype=int, sep=',')

def __cleanStringAlpha(strText):
    s = strText.lower()
    s = ''.join(i for i in s if i.isalpha())
    return s

def __arrayToString(arrString):
    return ''.join(chr(int(i)+97) for i in arrString)
