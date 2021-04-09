# TODO: moet ek error goed maak indien inputs verkeerd is?
# TODO: sit error code goed in exception
# TODO: kyk na array se formating orals (int, float, double ens)
# TODO: Eerder herhaal as net uitlos hkm? want die laaste letters van n woord of die laste ry pixels van n foto kan die foto weg gee (fail-safe method)
# ma kan die nie regitg met fotos doen nie want die moet seker dimensions he... en by fotos sal dit max 2 pixels wees

# hill cipher kan nie regtig een kleurig goed doen nie?

from PIL import Image
import numpy as np
import string

K = None
 
############################ Main functions: ############################

# TODO: key of encryption matrix return?
# TODO: kan my code hanteer as jy 2 keer encryption na mekaar doen?
# TODO: edge cases: as plain text kleiner is as 2 of 3 = gooi error en repeat plaintext sodat hy groot genoeg is
# Hill_Encrypt (key : String, plaintext : String or Int ndarray)
def Hill_Encrypt(key, plaintext):
    if len(key) == 4:
        m = 2
    elif len(key) == 9:
        m = 3

    C = []
    K = __makeMatrix(key)
    
    flag_small = False

    # text
    if type(plaintext) is not np.ndarray:
        P = __cleanString(plaintext)

        # plaintext not long enough to be encrypted
        while len(P) < m:
            flag_small = True
            P = np.concatenate((P,P), axis=None)
        
        if flag_small == True:
            P = P[:m]
            print("\nWARNING: plaintext length too short, plaintext was concatenated... (skryf dalk iets beter hier?)\n")

        
        int_l = len(P)
        # if the plaintext length is not a multiple of m, concatenated the string
        if len(P) != (m*(len(P)//m)):
            print("\nWARNING: plaintext length too short, plaintext was concatenated... (skryf dalk iets beter hier?)\n")
            P = np.concatenate((P,P), axis=None)
            P = P[:m*(int_l//m)+m]
        
        for i in range(len(P) // m):
            C = np.concatenate((C, np.mod(np.dot(P[m*i:m*i+m], K), 26)), axis=None)

        return __arrayToString(C)
    # images
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
            print("\nWARNING: Not enough pixels, image was contactednated... (skryf dalk iets beter hier?)\n")
        
        while len(g_channel) < m:
            flag_small_g = True
            g_channel = np.concatenate((g_channel,g_channel), axis=None)
        
        if flag_small_g == True:
            g_channel = g_channel[:m]
            print("\nWARNING: Not enough pixels, image was contactednated... (skryf dalk iets beter hier?)\n")
        
        while len(b_channel) < m:
            flag_small_b = True
            b_channel = np.concatenate((b_channel,b_channel), axis=None)
        
        if flag_small_b == True:
            b_channel = b_channel[:m]
            print("\nWARNING: Not enough pixels, image was contactednated... (skryf dalk iets beter hier?)\n")
    

        for i in range(len(r_channel) // m):
            r_enc = np.concatenate((r_enc,np.dot(r_channel[m*i:m*i+m], K)), axis=None)
        for j in range(len(g_channel) // m):
            g_enc = np.concatenate((g_enc,np.dot(g_channel[m*j:m*j+m], K)), axis=None)
        for k in range(len(b_channel) // m):
            b_enc = np.concatenate((b_enc,np.dot(b_channel[m*k:m*k+m], K)), axis=None)




        # letters wat nie ge-encrypt is nie word maar nou unencrypted agter aan gesit,
        if len(r_channel) != len(r_enc):
            r_enc = np.concatenate((r_enc,r_channel[len(r_enc)::]),axis=None)
        if len(g_channel) != len(g_enc):
            g_enc = np.concatenate((g_enc,g_channel[len(g_enc)::]),axis=None)
        if len(b_channel) != len(b_enc):
            b_enc = np.concatenate((b_enc,b_channel[len(b_enc)::]),axis=None)

        r_enc = r_enc.reshape(plaintext[:,:,0].shape[0],plaintext[:,:,0].shape[1])
        g_enc = g_enc.reshape(plaintext[:,:,1].shape[0],plaintext[:,:,1].shape[1])
        b_enc = b_enc.reshape(plaintext[:,:,2].shape[0],plaintext[:,:,2].shape[1])

        return np.dstack((r_enc,g_enc,b_enc))

# Hill_Decrypt (key : String, ciphertext : String or Int ndarray)
def Hill_Decrypt(key, ciphertext):

    # TODO: png check
    if len(key) == 4:
        m = 2
    elif len(key) == 9:
        m = 3
    
    P = []
    K = __makeMatrix(key)
    
    if type(ciphertext) is not np.ndarray:
        C = __cleanString(ciphertext)
        K_inv = __inverse(m,K,False)

        for i in range(len(C) // m):
            P = np.concatenate((P, np.mod(np.dot(C[m*i:m*i+m], K_inv), 26)), axis=None)
        
        return __arrayToString(P)

    else:
        C = ciphertext

        r_channel = np.array(ciphertext[:,:,0]).reshape(1,ciphertext[:,:,0].shape[0]*ciphertext[:,:,0].shape[1])[0]
        g_channel = np.array(ciphertext[:,:,1]).reshape(1,ciphertext[:,:,1].shape[0]*ciphertext[:,:,1].shape[1])[0]
        b_channel = np.array(ciphertext[:,:,2]).reshape(1,ciphertext[:,:,2].shape[0]*ciphertext[:,:,2].shape[1])[0]

        r_dec = []
        g_dec = []
        b_dec = []

        K_inv = __inverse(m,K,True)

        for i in range(len(r_channel) // m):
            r_dec = np.concatenate((r_dec,np.dot(r_channel[m*i:m*i+m], K_inv)), axis=None)
        for j in range(len(g_channel) // m):
            g_dec = np.concatenate((g_dec,np.dot(g_channel[m*j:m*j+m], K_inv)), axis=None)
        for k in range(len(b_channel) // m):
            b_dec = np.concatenate((b_dec,np.dot(b_channel[m*k:m*k+m], K_inv)), axis=None)

        if len(r_channel) != len(r_dec):
            r_dec = np.concatenate((r_dec,r_channel[len(r_dec)::]),axis=None)
        if len(g_channel) != len(g_dec):
            g_dec = np.concatenate((g_dec,g_channel[len(g_dec)::]),axis=None)
        if len(b_channel) != len(b_dec):
            b_dec = np.concatenate((b_dec,b_channel[len(b_dec)::]),axis=None)

        r_dec = r_dec.reshape(ciphertext[:,:,0].shape[0],ciphertext[:,:,0].shape[1])
        g_dec = g_dec.reshape(ciphertext[:,:,1].shape[0],ciphertext[:,:,1].shape[1])
        b_dec = b_dec.reshape(ciphertext[:,:,2].shape[0],ciphertext[:,:,2].shape[1])

        return np.dstack((r_dec,g_dec,b_dec))

# Get_Hill_Encryption_Matrix ()
def Get_Hill_Encryption_Matrix():
    # TODO: float return ?
    return K


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

    if m == 2:
        d = arrM[0][0]*arrM[1][1]-arrM[1][0]*arrM[0][1]
    else:
        d = arrM[0][0]*arrM[1][1]*arrM[2][2] + arrM[1][0]*arrM[2][1]*arrM[0][2] + arrM[2][0]*arrM[0][1]*arrM[1][2] \
            - arrM[2][0]*arrM[1][1]*arrM[0][2] - arrM[1][0] * \
            arrM[0][1]*arrM[2][2] - arrM[0][0]*arrM[2][1]*arrM[1][2]

    return int(d)

def __inverseModulo(a):
    for i in range(1,26):
        if (a*i)%26 == 1:
            return i
    
    print("sit nog n error hier in iets soos : Key matrix determinant does not have modular multiplicative inverse")
    return -1

def __inverse(m, arrM, png):
    inv = np.zeros(shape=(m, m))

    # image
    if png == True:
        det = __determinant(m, arrM)
        det = 1/det
    # text
    else:
        det = __determinant(m, arrM)%26
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

    if png == True:
        return inv
    else:
        return np.mod(inv,26)

def __arrayToString(arrString):
    return ''.join(chr(int(i)+97) for i in arrString)


# TODO: hanteer nog case waar input nie die regte lengte is nie, maak exception, by fotos los net daai pixels uit maar gee nogsteeds die warning



# print(Hill_Encrypt("RRFVSVCCT","jannieensannie"))
# print(Hill_Decrypt("RRFVSVCCT","xxghjxnalnaaesj"))

p_File = Image.open('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\o_blue.png')
p_img = np.asarray(p_File)

#print(p_img)

print("___________________________________________")

img_enc = Hill_Encrypt("RRFVSVCCT",p_img)
print("half")
img_dec = Hill_Decrypt("RRFVSVCCT",img_enc)

#print((Image.fromarray(img_dec.astype(np.uint8))).size)

Image.fromarray(img_enc.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\o_blue_encrypted.png')
Image.fromarray(img_dec.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\o_blue_decrypted.png')

#print(p_img)

# extract 2D R,G,B arrays
#print("R: ",p_img[:,:,0])
# print("G: ",p_img[:,:,1])
# print("B: ",p_img[:,:,2])

# From 2D array to 1D array
# r_channel = np.array(p_img[:,:,0]).reshape(1,p_img[:,:,0].shape[0]*p_img[:,:,0].shape[1])[0]
# g_channel = np.array(p_img[:,:,1]).reshape(1,p_img[:,:,1].shape[0]*p_img[:,:,1].shape[1])[0]
# b_channel = np.array(p_img[:,:,2]).reshape(1,p_img[:,:,2].shape[0]*p_img[:,:,2].shape[1])[0]

# r_channel = r_channel.reshape(p_img[:,:,0].shape[0],p_img[:,:,0].shape[1])
# g_channel = g_channel.reshape(p_img[:,:,1].shape[0],p_img[:,:,1].shape[1])
# b_channel = b_channel.reshape(p_img[:,:,2].shape[0],p_img[:,:,2].shape[1])

# print(type(p_File))

# # summarize image details
# print(p_File.mode)
# print(p_File.size)


# print("_______________________________")


# print(np.dstack((r_channel,g_channel,b_channel)))

# Img2 = Image.fromarray(np.dstack((r_channel,g_channel,b_channel)))
# print(type(Img2))

# # summarize image details
# print(Img2.mode)
# print(Img2.size)

# Img2.save('office_out.png')


#print(r_channel)
# print(g_channel)
# print(b_channel)

# a = np.array([[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8]])

# b = np.array([[11,12,13,14,15,16,17,18],[11,12,13,14,15,16,17,18],[11,12,13,14,15,16,17,18]])

# c = np.array([[21,22,23,24,25,26,27,28],[21,22,23,24,25,26,27,28],[21,22,23,24,25,26,27,28]])

# print(np.dstack((a,b,c)))



# print(Hill_Encrypt("RRFVSVCCT",a))
# print(Hill_Decrypt("RRFVSVCCT",np.array([65,59,104,10175,9413,11416,6145,5812,3821, 9])))



# a = [[2, 3, 3], [4, 5, 6], [7, 8, 9]]
# b = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# c = [[2, 3], [1, 9]]

# A = [[5,8],[17,3]]
# K = [[17,17,5],[21,18,21],[2,2,19]]

# w = [[6,24,1],[13,16,10],[20,17,15]]

# wk = [[3,3],[2,5]]

# print(__inverse(2,wk))

#print(__determinant(3,K))

# print(Hill_Encrypt("RRFVSVCCT","paymoremoneyaa"))
# print(Hill_Decrypt("RRFVSVCCT","rrlmwbkaspdhaa"))

# print(Hill_Encrypt("DDCF","HELP"))
# print(Hill_Decrypt("DDCF","dple"))

# print(Hill_Encrypt("DDCF","THISWATERISVNICE"))
# print(Hill_Encrypt("LUdd","toikoonzpnsddboa"))
# print(Hill_Decrypt("LUdd","rgoiokkxwbzfklyu"))
# print(Hill_Decrypt("DDCF","toikoonzpnsddboa"))

# print(Hill_Encrypt("alphabeta","wearesafe"))
# print(Hill_Decrypt("alphabeta","ciwwjzzyf"))

# DDCA???

#print(Hill_Encrypt("RRFVSVCCT","paymoremoney"))

# print(Hill_Encrypt("DCIF","hillcipher"))
# print(Hill_Decrypt("DCIF","hcrzssxnsp"))

# print(Hill_Encrypt("DCIZ","hillcipher"))
# print(Hill_Decrypt("DCIZ","hgrlswxxsr"))

# print(Hill_Encrypt("DDCF","hillcipher"))
# print(Hill_Decrypt("DDCF","ljdkwuhcut"))


# https://crypto.interactive-maths.com/hill-cipher.html
# let wel hulle gebruik C = KP mod 26 en ons (volgens handboek) C = PK mod 26, so ook vir decryption