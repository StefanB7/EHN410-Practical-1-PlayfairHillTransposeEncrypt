# TODO: kyk na array se formating orals (int, float, double ens)
# TODO: key of encryption matrix return?

from PIL import Image
import numpy as np
import string


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

