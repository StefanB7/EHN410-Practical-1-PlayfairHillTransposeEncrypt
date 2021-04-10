# eerder string concatenate want ciphers doen nie goed om herhalende goed te encrypt nie? dalk so by hill maar nie hier nie?
# kan pixels concatenate of ek kan key herhaal, 
from PIL import Image
import numpy as np
import string


############################ Main functions: ############################

# Transpose_ Encrypt (key : String, stage : Int, plaintext : String)

# wat gebeur as die matriks nie heeltemal vol gemaak word met die plaintext nie
def Transpose_Encrypt(key, stage, plaintext):

    K = __cleanStringInt(key)

    # text
    if type(plaintext) is not np.ndarray:
        P = np.array(list(__cleanStringAlpha(plaintext)))

        flag_small = False

        # if the plaintext is smaller than the key
        while len(P) < len(K):
            flag_small = True
            P = np.concatenate((P,P), axis=None)

        if flag_small == True:
            P = P[:len(K)]
            print("\nWARNING: plaintext length too short, plaintext was concatenated... (skryf dalk iets beter hier?)\n")

        int_l = len(P)
        # if the plaintext length is not a multiple of key lenght, concatenated the string
        if len(P) != (len(K)*(len(P)//len(K))):
            print("\nWARNING: plaintext length too short, plaintext was concatenated... (skryf dalk iets beter hier?)\n")
            P = np.concatenate((P,P), axis=None)
            P = P[:len(K)*(int_l//len(K))+len(K)]

        P = P.reshape(-1,(len(K)))

        print(P)

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

        return "".join(C)
    # Image
    else:
        
        P = plaintext

        flag_key_short = False
        while len(K) < plaintext.shape[1]:
            flag_key_short = True
            K = np.concatenate((K,K), axis=None)
        
        if flag_key_short == True:
            print("\nWARNING: Key length too short, Key was concatenated... (skryf dalk iets beter hier?)\n")
            K = K[:plaintext.shape[1]]

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
            print("\nWARNING: Not enough pixels, image was contactednated... (skryf dalk iets beter hier?)\n")

        while len(g_channel) < len(K):
            flag_small_g = True
            g_channel = np.concatenate((g_channel,g_channel), axis=None)
        
        if flag_small_g == True:
            g_channel = g_channel[:len(K)]
            print("\nWARNING: Not enough pixels, image was contactednated... (skryf dalk iets beter hier?)\n")
        
        while len(b_channel) < len(K):
            flag_small_b = True
            b_channel = np.concatenate((b_channel,b_channel), axis=None)
        
        if flag_small_b == True:
            b_channel = b_channel[:len(K)]
            print("\nWARNING: Not enough pixels, image was contactednated... (skryf dalk iets beter hier?)\n")


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

        if stage==2:

            r_channel = r_enc
            g_channel = g_enc
            b_channel = b_enc

            K = __cleanStringInt(key)

            while len(K) < plaintext.shape[1]:
                K = np.concatenate((K,K), axis=None)
            
            # hmmm moet dit nie altyd geroep word nie
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

        
        # r_enc = r_enc[:plaintext[:,:,0].shape[0]*plaintext[:,:,0].shape[1]]
        # g_enc = g_enc[:plaintext[:,:,0].shape[0]*plaintext[:,:,0].shape[1]]
        # b_enc = b_enc[:plaintext[:,:,0].shape[0]*plaintext[:,:,0].shape[1]]

        r_enc = r_enc.reshape(plaintext[:,:,0].shape[0],plaintext[:,:,0].shape[1])
        g_enc = g_enc.reshape(plaintext[:,:,1].shape[0],plaintext[:,:,1].shape[1])
        b_enc = b_enc.reshape(plaintext[:,:,2].shape[0],plaintext[:,:,2].shape[1])

        return np.dstack((r_enc,g_enc,b_enc))
    

# Transpose_ Decrypt (key : String, stage : Int, ciphertext : String)
def Transpose_Decrypt(key, stage, ciphertext):
    
    K = __cleanStringInt(key)
    
    # text
    if type(ciphertext) is not np.ndarray:
    
        C = np.array(list(__cleanStringAlpha(ciphertext)))

        C = C.reshape((len(K),-1)).transpose()

        preP = np.empty(shape=(len(C[:,0]),len(K)),dtype=str)

        for i in range(len(K)):
            pos = np.argmin(K)
            K[pos] = 99
            preP[:,pos] = C[:,i]

        preP = preP.reshape((1,-1))[0]

        P = "".join(preP)

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
    # image
    else:
        flag_key_short = False

        while len(K) < ciphertext.shape[1]:
            flag_key_short = True
            K = np.concatenate((K,K), axis=None)
        
        if flag_key_short == True:
            print("\nWARNING: Key length too short, Key was concatenated... (skryf dalk iets beter hier?)\n")
            K = K[:ciphertext.shape[1]]

        r_channel = np.array(ciphertext[:,:,0])
        g_channel = np.array(ciphertext[:,:,1])
        b_channel = np.array(ciphertext[:,:,2])

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


# trans_enc = Transpose_Encrypt("helao",1,"Die is n baie lang sin ek wonder of hy gaan inpas")

# print(trans_enc)

# trans_dec = Transpose_Decrypt("helao",1,trans_enc)

# print(trans_dec)

p_File = Image.open('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\office.png')
p_img = np.asarray(p_File)

#print(p_img)

print("___________________________________________")

img_enc = Transpose_Encrypt("RRFVSVCCT",2,p_img)
print("half")
img_dec = Transpose_Decrypt("RRFVSVCCT",2,img_enc)

#print((Image.fromarray(img_dec.astype(np.uint8))).size)

Image.fromarray(img_enc.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\office_encrypted_T.png')
Image.fromarray(img_dec.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\office_decrypted_T.png')

#TODO: vir die gevalle waar die key en die plaintext nie oplyn nie kan ek
# - die laaste goed wat nie inpas nie net uitlos
# - die key probeer herhaal of verminder sodat die plain text inpas, maar dit sal ook nie altyd werk nie, se maar die lengte van die plaintext is n priemgetal
#TODO: exceptions
#TODO: filler symbol is x want hy kom die minste voor in die woordeboek probability is laer, en a dubbel x bestaan nie in min woorde aan die begin en einde???
