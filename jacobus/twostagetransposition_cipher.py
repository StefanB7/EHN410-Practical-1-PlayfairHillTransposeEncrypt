from PIL import Image
import numpy as np
import string


############################ Main functions: ############################

# Transpose_ Encrypt (key : String, stage : Int, plaintext : String)

# wat gebeur as die matriks nie heeltemal vol gemaak word met die plaintext nie
def Transpose_Encrypt(key, stage, plaintext):
    print("Transpose encrypt")

    P = np.array(list(__cleanStringAlpha(plaintext)))
    K = __cleanStringInt(key)

    P = P.reshape(-1,(len(K)))

    C = []

    for i in range(len(K)):
        pos = np.argmin(K)
        K[pos] = 99
        C = np.concatenate((C,P[:,pos]),axis=None)

    if stage==2:
        P = C
        K = __cleanStringInt(key)
        P = P.reshape(-1,(len(K)))
        C = []

        for i in range(len(K)):
            pos = np.argmin(K)
            K[pos] = 99
            C = np.concatenate((C,P[:,pos]),axis=None)

    # can be used to do n-amount of stages:
    return "".join(C)

# Transpose_ Decrypt (key : String, stage : Int, ciphertext : String)
def Transpose_Decrypt(key, stage, ciphertext):
    
    
    
    
    
    
    
    
    print("Transpose decrypt")


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


Transpose_Encrypt("helao",1,"Die is n baie lang sin ek ek wonder of hy gaan inaps")
