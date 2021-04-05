# TODO: moet ek error goed maak indien inputs verkeerd is?

from PIL import Image
import numpy as np
import string

K = None

# Main functions:

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

        C = np.concatenate((C, np.mod(np.dot(P[m*i:m*i+m], K), 26)), axis=None)

    # TODO: Sit die nog om na string as input string?
    return __arrayToString(C)

# Hill_Decrypt (key : String, ciphertext : String or Int ndarray)
def Hill_Decrypt(key, ciphertext):

    # TODO: png check

    if len(key) == 4:
        m = 2
    elif len(key) == 9:
        m = 3
    
    P = []
    
    if type(ciphertext) is not np.ndarray:
        C = __cleanString(ciphertext)

    K = __makeMatrix(key)

    K_inv = __inverse(m,K)

    for i in range(len(C) // m):
        P = np.concatenate((P, np.mod(np.dot(C[m*i:m*i+m], K_inv), 26)), axis=None)

    # TODO: Sit die nog om na string as input string?
    return __arrayToString(P)



# Get_Hill_Encryption_Matrix ()
def Get_Hill_Encryption_Matrix():
    # TODO: float return ?
    return K



# Helper functions:

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

    if m == 2:
        d = arrM[0][0]*arrM[1][1]-arrM[1][0]*arrM[0][1]
    else:
        d = arrM[0][0]*arrM[1][1]*arrM[2][2] + arrM[1][0]*arrM[2][1]*arrM[0][2] + arrM[2][0]*arrM[0][1]*arrM[1][2] \
            - arrM[2][0]*arrM[1][1]*arrM[0][2] - arrM[1][0] * \
            arrM[0][1]*arrM[2][2] - arrM[0][0]*arrM[2][1]*arrM[1][2]

    return int(d)%26

def __inverseModulo(a):
    for i in range(1,26):
        if (a*i)%26 == 1:
            return i
    return -1

def __inverse(m, arrM):
    inv = np.zeros(shape=(m, m))
    det = __determinant(m, arrM)

    det = __inverseModulo(det)

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

    return np.mod(inv,26)

def __arrayToString(arrString):
    return ''.join(chr(int(i)+97) for i in arrString)


a = [[2, 3, 3], [4, 5, 6], [7, 8, 9]]
b = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
c = [[2, 3], [1, 9]]

A = [[5,8],[17,3]]
K = [[17,17,5],[21,18,21],[2,2,19]]


w = [[6,24,1],[13,16,10],[20,17,15]]

wk = [[3,3],[2,5]]

# print(__inverse(2,wk))


#print(__determinant(3,K))

#print(Hill_Encrypt("RRFVSVCCT","paymoremoney"))
print(Hill_Decrypt("RRFVSVCCT","rrlmwbkaspdh"))


#print(Hill_Encrypt("RRFVSVCCT","paymoremoney"))
# print(Hill_Encrypt("DCIF","hillcipher"))
