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




    #If the plaintext is an image (ndarray) that needs to be encrypted:
    if (isinstance(plaintext,np.ndarray)):
        print("Hello2")

#Function cleans the input, removes any special characters (including spaces) and makes all letters lower case
def cleanInput(input):

    input = input.lower();

    alphabet= ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'];
    cleanedInput = "";
    for character in input:
        bAlphaLetter = False;
        index = 0;
        while (not(bAlphaLetter) and (index < len(alphabet))):
            if (character == alphabet[index]):
                bAlphaLetter = True;
            index += 1
        if (bAlphaLetter):
            cleanedInput = cleanedInput + character;

    return cleanedInput

def toNumber(letter):
    return ord(letter) - 96

def generatePlayfairKey(characterKey):
    # Generate the key:
    alphabet = ['a','b','c','d','e','f','g','h','i','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    characterKey = characterKey.lower()

    charKeyMatrix = np.empty((5, 5), dtype='U1')
    alreadyIn = []
    #Iterators:
    row = 0
    column = 0
    for character in characterKey:
        if not(character in alreadyIn):
            charKeyMatrix[row][column] = character
            alreadyIn.append(character)
            #I and J together in same bin:
            if ((character == 'i') or (character == 'j')):
                #Add both as it does not matter if they are repeated
                alreadyIn.append('i')
                alreadyIn.append('j')

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

print(generatePlayfairKey("Hj"))