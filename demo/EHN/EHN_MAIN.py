import numpy as np
import string
import PIL.Image as pilimage
import random as rnd
import time as t
from ehn2021_demo1 import Playfair_Encrypt
from ehn2021_demo1 import Get_Playfair_Encryption_Matrix
from ehn2021_demo1 import Playfair_Decrypt
from ehn2021_demo1 import Hill_Encrypt
from ehn2021_demo1 import Get_Hill_Encryption_Matrix
from ehn2021_demo1 import Hill_Decrypt
from ehn2021_demo1 import Transpose_Encrypt
from ehn2021_demo1 import Transpose_Decrypt

sleep_sec = 5
hill_key_override = False
low_res_override = False



# For marking purposes -------------
#Generate a random key of numbers or lettersm, depending on the mode
def Generate_Random_Key(mode = 'text', length = 9):
    key = None
    letters = string.ascii_letters
    numbers = string.digits
    if(mode == 'text'):
        key = ""
        for i in range(length):
            key += rnd.choice(letters)

    elif (mode == 'img'):
        key = (np.random.choice(numbers) for i in range(length))

    return key

# Get the message from a file, either a text file or a png
def Get_Message(mode= 'text'):
    message = None
    if(mode == 'text'):
        file_object = open(r"message.txt","r")
        message = file_object.readlines()
        for m in range(0, len(message)):
            if(message[m][-1] == "\n"):
                message[m] = message[m][0:-1]


    elif(mode == 'img'):
        message = list()
        if (low_res_override == True):
            message.append(pilimage.open("img1_Low.png"))
            message.append(pilimage.open("img2_Low.png"))
            message.append(pilimage.open("img3_Low.png"))
        else:
            message.append(pilimage.open("img1.png"))
            message.append(pilimage.open("img2.png"))
            message.append(pilimage.open("img3.png"))
        # print(im.format, im.size, im.mode)
    return message

# End marking functions ------------

def Test_Playfair_Text():

    text_plaintext = Get_Message(mode='text')
    k = 0
    for plain in text_plaintext:
        print("Testing Playfair for Text message : " + plain)
        key = Generate_Random_Key(mode='text', length=5 + k)
        k += 3
        print("Key: " + str(key))

        ciphertext = None
        try:
            ciphertext = Playfair_Encrypt(key=key, plaintext=plain)
        except:
            print('EXCEPTION ENCOUNTERED AT "Playfair_Encrypt"...')
        try:
            print("Encrypted message: " + ciphertext)
        except:
            print('PLAYFAIR TEXT CIPHERTEXT PROBABLY NOT A STRING...')

        playfair_matrix = None
        try:
            playfair_matrix = Get_Playfair_Encryption_Matrix()
            if(isinstance(playfair_matrix, list) or isinstance(playfair_matrix, tuple)):
                playfair_matrix = np.asarray(playfair_matrix)
        except:
            print('EXCEPTION ENCOUNTERED AT "Get_Playfair_Encryption_Matrix"...')
        try:
            print("Playfair Matrix shape: " + str(playfair_matrix.shape))
        except:
            print('PLAYFAIR MATRIX NOT ndarray')
        try:
            print("Playfair Matrix: \n" + str(playfair_matrix))
        except:
            print('CANNOT PRINT PLAYFAIR MATRIX...')

        plaintext = None
        try:
            plaintext = Playfair_Decrypt(key=key, ciphertext=ciphertext)
        except:
            print('EXCEPTION ENCOUNTERED AT "Playfair_Decrypt"...')
        try:
            print("Decrypted Plaintext: " + plaintext)
        except:
            print('PLAYFAIR TEXT PLAINTEXT PROBABLY NOT A STRING...')

    print("Exiting Test_Playfair_Text...")


def Test_Playfair_Image():
    image_plaintext = Get_Message(mode='img')
    k = 0
    i = 1
    for im in image_plaintext:
        plain = np.asarray(im)
        # plain = plain[:,:,0:3]
        print("Testing Playfair for Image message : " + str(i))
        key = Generate_Random_Key(mode='text', length= 3 + k)
        k += 2
        print("Key: " + str(key))

        ciphertext = None
        try:
            ciphertext = Playfair_Encrypt(key=key, plaintext=plain)
        except:
            print('EXCEPTION ENCOUNTERED AT "Playfair_Encrypt"...')
        try:
            print("Encrypted message: " + str(ciphertext[0:3]))
        except:
            print('PLAYFAIR IMAGE CIPHERTEXT CANNOT PRINT...')

        playfair_matrix = None
        try:
            playfair_matrix = Get_Playfair_Encryption_Matrix()
            if (isinstance(playfair_matrix, list) or isinstance(playfair_matrix, tuple)):
                playfair_matrix = np.asarray(playfair_matrix)
        except:
            print('EXCEPTION ENCOUNTERED AT "Get_Playfair_Encryption_Matrix"...')
        try:
            print("Playfair Matrix shape: " + str(playfair_matrix.shape))
        except:
            print('PLAYFAIR MATRIX NOT ndarray...')
        try:
            print("Playfair Matrix: \n" + str(playfair_matrix[0:3]))
        except:
            print('CANNOT PRINT PLAYFAIR MATRIX...')

        plaintext = None
        try:
            plaintext = Playfair_Decrypt(key=key, ciphertext=ciphertext)
        except:
            print('EXCEPTION ENCOUNTERED AT "Playfair_Decrypt"...')
        try:
            print(plaintext.shape)
            image = pilimage.fromarray(plaintext)
            image.show()
            t.sleep(sleep_sec)
        except:
            print('PLAYFAIR IMAGE PLAINTEXT TO IMAGE FAILED...')
        i += 1
    print("Exiting Test_Playfair_Image...")


def Test_Hill_Text():
    text_plaintext = Get_Message(mode='text')
    k = 0
    for plain in text_plaintext:
        print("Testing Hill for Text message : " + plain)
        key = None
        if(hill_key_override == True):
            key = 'dkuujrjer'
        else:
            key = Generate_Random_Key(mode='text', length=9)
        print("Key: " + str(key))

        ciphertext = None
        try:
            ciphertext = Hill_Encrypt(key=key, plaintext=plain)
        except:
            print('EXCEPTION ENCOUNTERED AT "Hill_Encrypt"...')
        try:
            print("Encrypted message: " + ciphertext)
        except:
            print('HILL TEXT CIPHERTEXT PROBABLY NOT A STRING...')

        hill_matrix = None
        try:
            hill_matrix = Get_Hill_Encryption_Matrix()
            if (isinstance(hill_matrix, list) or isinstance(hill_matrix, tuple)):
                hill_matrix = np.asarray(hill_matrix)
        except:
            print('EXCEPTION ENCOUNTERED AT "Get_Hill_Encryption_Matrix"...')
        try:
            print("Hill Matrix shape: " + str(hill_matrix.shape))
        except:
            print('Hill MATRIX NOT ndarray')
        try:
            print("Hill Matrix: \n" + str(hill_matrix))
        except:
            print('CANNOT PRINT HILL MATRIX...')

        plaintext = None
        try:
            plaintext = Hill_Decrypt(key=key, ciphertext=ciphertext)
        except:
            print('EXCEPTION ENCOUNTERED AT "Hill_Decrypt"...')
        try:
            print("Decrypted Plaintext: " + plaintext)
        except:
            print('HILL TEXT PLAINTEXT PROBABLY NOT A STRING...')

    print("Exiting Test_Hill_Text...")


def Test_Hill_Image():
    image_plaintext = Get_Message(mode='img')
    k = 0
    i = 1
    for im in image_plaintext:
        plain = np.asarray(im)
        # plain = plain[:,:,0:3]
        print("Testing Hill for Image message : " + str(i))
        key = None
        if (hill_key_override == True):
            key = 'dkuujrjer'
        else:
            key = Generate_Random_Key(mode='text', length=9)
        print("Key: " + str(key))

        ciphertext = None
        try:
            ciphertext = Hill_Encrypt(key=key, plaintext=plain)
        except:
            print('EXCEPTION ENCOUNTERED AT "Hill_Encrypt"...')
        try:
            print("Encrypted message: " + str(ciphertext[0:3]))
        except:
            print('HILL IMAGE CIPHERTEXT CANNOT PRINT...')

        Hill_matrix = None
        try:
            Hill_matrix = Get_Hill_Encryption_Matrix()
            if (isinstance(Hill_matrix, list) or isinstance(Hill_matrix, tuple)):
                Hill_matrix = np.asarray(Hill_matrix)
        except:
            print('EXCEPTION ENCOUNTERED AT "Get_Hill_Encryption_Matrix"...')
        try:
            print("Hill Matrix shape: " + str(Hill_matrix.shape))
        except:
            print('HILL MATRIX NOT ndarray...')
        try:
            print("Hill Matrix: \n" + str(Hill_matrix[0:3]))
        except:
            print('CANNOT PRINT Hill MATRIX...')

        plaintext = None
        try:
            plaintext = Hill_Decrypt(key=key, ciphertext=ciphertext)
        except:
            print('EXCEPTION ENCOUNTERED AT "Hill_Decrypt"...')
        try:
            print(plaintext.shape)
            image = pilimage.fromarray(plaintext)
            image.show()
            t.sleep(sleep_sec)
        except:
            print('Hill IMAGE PLAINTEXT TO IMAGE FAILED...')
        i += 1
    print("Exiting Test_Hill_Image...")


def Test_Transposition_Text():
    text_plaintext = Get_Message(mode='text')
    k = 0
    for plain in text_plaintext:
        print("Testing Transposition for Text message : " + plain)
        key = Generate_Random_Key(mode='text', length=15)
        print("Key: " + str(key))

        ciphertext1 = None
        ciphertext2 = None
        try:
            ciphertext1 = Transpose_Encrypt(key=key, stage= 1, plaintext=plain)
        except:
            print('EXCEPTION ENCOUNTERED AT "Single stage Transpose_Encrypt"...')
        try:
            ciphertext2 = Transpose_Encrypt(key=key, stage= 2, plaintext=plain)
        except:
            print('EXCEPTION ENCOUNTERED AT "Double stage Transpose_Encrypt"...')
        try:
            print("Single stage encrypted message: " + ciphertext1)
            print("Double stage encrypted message: " + ciphertext2)
        except:
            print('TRANSPOSITION TEXT CIPHERTEXT PROBABLY NOT A STRING...')


        plaintext1 = None
        plaintext2 = None
        try:
            plaintext1 = Transpose_Decrypt(key=key, stage= 1, ciphertext=ciphertext1)
        except:
            print('EXCEPTION ENCOUNTERED AT "Single stage Transpose_Decrypt"...')
        try:
            plaintext2 = Transpose_Decrypt(key=key, stage= 2, ciphertext=ciphertext2)
        except:
            print('EXCEPTION ENCOUNTERED AT "Double stage Transpose_Decrypt"...')
        try:
            print("Single stage Decrypted Plaintext: " + plaintext1)
            print("Double stage Decrypted Plaintext: " + plaintext2)
        except:
            print('TRANSPOSITION TEXT PLAINTEXT PROBABLY NOT A STRING...')

    print("Exiting Test_Transposition_Text...")


# Main function for Practical 1
if __name__ == '__main__':
    # Image_Test()
    print("PLAYFAIR TESTING: \n")
    Test_Playfair_Text()
    Test_Playfair_Image()
    print("\n PLAYFAIR TESTING DONE. \n")

    print("HILL TESTING: \n")
    Test_Hill_Text()
    Test_Hill_Image()
    print("\n HILL TESTING DONE. \n")

    print("TRANSPOSITION TESTING: \n")
    Test_Transposition_Text()
    print("\n TRANSPOSITION TESTING DONE. \n")

    print("Done...")




