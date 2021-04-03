# TODO: moet ek error goed maak indien inputs verkeerd is?

from PIL import Image
import numpy as np
import string

K = None

######### Main functions:

# Hill_Encrypt (key : String, plaintext : String or Int ndarray)
# TODO: kan my code hanteer as jy 2 keer encryption na mekaar doen?
def Hill_Encrypt(key, plaintext):
    if len(key) == 4:
        m = 2    
    elif len(key) == 9:
        m = 3

    # TODO: skep nog geval waar hy n png kan handle
    if type(plaintext) is not np.ndarray:
        P = __cleanString(plaintext)
    
    C = []
    K = __makeMatrix(key)

    for i in range(len(P) // m):
        C = np.concatenate((C,np.mod(np.dot(P[m*i:m*i+m],K),26)),axis=None)

    # TODO: Sit die nog om na string as input string?
    return C

# Hill_Decrypt (key : String, ciphertext : String or Int ndarray)
def Hill_Decrypt (key, ciphertext):
    print("Hill decrypt")

# Get_Hill_Encryption_Matrix ()
def Get_Hill_Encryption_Matrix():
    # TODO: float return ?
    return K

######### Helper functions:

def __cleanString(strText):
    s = strText.lower()
    s = ''.join(str(ord(i)-97)+',' for i in s if i.isalpha())
    return np.fromstring(s, dtype=int, sep=',')

def __makeMatrix(strKey):
    if len(strKey) == 4:
        return np.array(list(__cleanString(strKey))).reshape(2,2)
    else:
        return np.array(list(__cleanString(strKey))).reshape(3,3)

def __inverse(arrM):
    print("inverse")


def _arrayToString(arrString):
    return ''.join(chr(int(i)+97) for i in arrString)

a = Hill_Encrypt("DCIF","hillcipher")

print(_arrayToString(a))

#print(Hill_Encrypt("RRFVSVCCT","paymoremoney"))
#print(Hill_Encrypt("DCIF","hillcipher"))