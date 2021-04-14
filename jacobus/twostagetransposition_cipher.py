# TODO: ek dink ek moet die image goed uithaal...

from PIL import Image
import numpy as np
import string

############################ Main functions: ############################

# Transpose_ Encrypt (key : String, stage : Int, plaintext : String)
def Transpose_Encrypt(key, stage, plaintext):

    K = __cleanStringInt(key)

    # plaintext encryption
    if type(plaintext) is not np.ndarray:
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
    
    # image encryption
    else:
        
        P = plaintext
        
        # key too short for the image encryption implementation
        flag_key_short = False
        while len(K) < plaintext.shape[1]:
            flag_key_short = True
            K = np.concatenate((K,K), axis=None)
        
        if flag_key_short == True:
            print("\nWARNING: Key length too short, Key was repeated...\n")
            K = K[:plaintext.shape[1]]

        # extract RGB channels
        r_channel = np.array(plaintext[:,:,0]).reshape(1,plaintext[:,:,0].shape[0]*plaintext[:,:,0].shape[1])[0]
        g_channel = np.array(plaintext[:,:,1]).reshape(1,plaintext[:,:,1].shape[0]*plaintext[:,:,1].shape[1])[0]
        b_channel = np.array(plaintext[:,:,2]).reshape(1,plaintext[:,:,2].shape[0]*plaintext[:,:,2].shape[1])[0]

        flag_small_r = False
        flag_small_g = False
        flag_small_b = False

        # if not enough pixels to be encrypted
        while len(r_channel) < len(K):
            flag_small_r = True
            r_channel = np.concatenate((r_channel,r_channel), axis=None)
        
        if flag_small_r == True:
            r_channel = r_channel[:len(K)]
            print("\nWARNING: Not enough pixels, image pixels were repeated...\n")

        while len(g_channel) < len(K):
            flag_small_g = True
            g_channel = np.concatenate((g_channel,g_channel), axis=None)
        
        if flag_small_g == True:
            g_channel = g_channel[:len(K)]
        
        while len(b_channel) < len(K):
            flag_small_b = True
            b_channel = np.concatenate((b_channel,b_channel), axis=None)
        
        if flag_small_b == True:
            b_channel = b_channel[:len(K)]


        r_channel = r_channel.reshape(-1,(len(K)))
        g_channel = g_channel.reshape(-1,(len(K)))
        b_channel = b_channel.reshape(-1,(len(K)))

        r_enc = []
        g_enc = []
        b_enc = []

        # 1 stage encryption
        for i in range(len(K)):
            pos = np.argmin(K)
            K[pos] = 999

            r_enc = np.concatenate((r_enc,r_channel[:,pos]),axis=None)
            g_enc = np.concatenate((g_enc,g_channel[:,pos]),axis=None)
            b_enc = np.concatenate((b_enc,b_channel[:,pos]),axis=None)

        # 2 stage encryption 
        if stage==2:

            r_channel = r_enc
            g_channel = g_enc
            b_channel = b_enc

            K = __cleanStringInt(key)

            while len(K) < plaintext.shape[1]:
                K = np.concatenate((K,K), axis=None)
            
            K = K[:plaintext.shape[1]]

            r_channel = r_channel.reshape(-1,(len(K)))
            g_channel = g_channel.reshape(-1,(len(K)))
            b_channel = b_channel.reshape(-1,(len(K)))
            
            r_enc = []
            g_enc = []
            b_enc = []

            for i in range(len(K)):
                pos = np.argmin(K)
                K[pos] = 999

                r_enc = np.concatenate((r_enc,r_channel[:,pos]),axis=None)
                g_enc = np.concatenate((g_enc,g_channel[:,pos]),axis=None)
                b_enc = np.concatenate((b_enc,b_channel[:,pos]),axis=None)

        # reshape RGB channels to matrices
        r_enc = r_enc.reshape(plaintext[:,:,0].shape[0],plaintext[:,:,0].shape[1])
        g_enc = g_enc.reshape(plaintext[:,:,1].shape[0],plaintext[:,:,1].shape[1])
        b_enc = b_enc.reshape(plaintext[:,:,2].shape[0],plaintext[:,:,2].shape[1])

        # combine RGB matrices into one array
        return np.dstack((r_enc,g_enc,b_enc))
    
# Transpose_ Decrypt (key : String, stage : Int, ciphertext : String)
def Transpose_Decrypt(key, stage, ciphertext):
    
    K = __cleanStringInt(key)
    
    # plaintext decryption
    if type(ciphertext) is not np.ndarray:
    
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

    # image decryption
    else:
        flag_key_short = False

        while len(K) < ciphertext.shape[1]:
            flag_key_short = True
            K = np.concatenate((K,K), axis=None)
        
        if flag_key_short == True:
            K = K[:ciphertext.shape[1]]
        
        # extract RGB channels
        r_channel = np.array(ciphertext[:,:,0])
        g_channel = np.array(ciphertext[:,:,1])
        b_channel = np.array(ciphertext[:,:,2])

        r_channel = r_channel.reshape((len(K),-1))
        g_channel = g_channel.reshape((len(K),-1))
        b_channel = b_channel.reshape((len(K),-1))

        pre_R = np.empty(shape=(r_channel.shape[1],len(K)),dtype=int)
        pre_G = np.empty(shape=(g_channel.shape[1],len(K)),dtype=int)
        pre_B = np.empty(shape=(b_channel.shape[1],len(K)),dtype=int)

        # 1 stage decryption
        for i in range(len(K)):
            pos = np.argmin(K)
            K[pos] = 999
        
            pre_R[:,pos] = r_channel[i,:]
            pre_G[:,pos] = g_channel[i,:]
            pre_B[:,pos] = b_channel[i,:]

        # 2 stage decryption
        if stage==2:
            K = __cleanStringInt(key)

            r_channel = pre_R
            g_channel = pre_G
            b_channel = pre_B

            while len(K) < ciphertext.shape[1]:
                flag_key_short = True
                K = np.concatenate((K,K), axis=None)
            K = K[:ciphertext.shape[1]]
            
            r_channel = r_channel.reshape((len(K),-1))
            g_channel = g_channel.reshape((len(K),-1))
            b_channel = b_channel.reshape((len(K),-1))

            pre_R = np.empty(shape=(r_channel.shape[1],len(K)),dtype=int)
            pre_G = np.empty(shape=(g_channel.shape[1],len(K)),dtype=int)
            pre_B = np.empty(shape=(b_channel.shape[1],len(K)),dtype=int)

            for i in range(len(K)):
                pos = np.argmin(K)
                K[pos] = 999       
                pre_R[:,pos] = r_channel[i,:]
                pre_G[:,pos] = g_channel[i,:]
                pre_B[:,pos] = b_channel[i,:]

        return np.dstack((pre_R,pre_G,pre_B))

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


