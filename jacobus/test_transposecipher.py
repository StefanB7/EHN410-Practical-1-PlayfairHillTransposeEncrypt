# trans_enc = Transpose_Encrypt("helao",1,"Die is n baie lang sin ek wonder of hy gaan inpas")

# print(trans_enc)

# trans_dec = Transpose_Decrypt("helao",1,trans_enc)

# print(trans_dec)

# p_File = Image.open('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\office.png')
# p_img = np.asarray(p_File)

#print(p_img)

# img_enc = Transpose_Encrypt("RRFVSVCCT",2,p_img)
# img_dec = Transpose_Decrypt("RRFVSVCCT",2,img_enc)

#print((Image.fromarray(img_dec.astype(np.uint8))).size)

# Image.fromarray(img_enc.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\office_encrypted_T.png')
# Image.fromarray(img_dec.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\office_decrypted_T.png')

#### !!!!! verander hill_cipher nog na die final combination script !!!!!

from PIL import Image
import numpy as np
import importlib
verander_die = importlib.import_module("hill_cipher")

txtENC = ""
txtDEC = ""

imgENC = None
imgDEC = None

# Test plaintext that is too small 
print("\n____________________________________________________")
print("\nTest (1/7): Plaintext that is too small")
print("\nInput:")
print("Plaintext: a")
print("Key: RRFVSVCCT")
print("\nOutput:")
txtENC = verander_die.Hill_Encrypt("RRFVSVCCT","a")
print("Encrypted text: ",txtENC)
txtDEC = verander_die.Hill_Decrypt("RRFVSVCCT",txtENC)
print("Decrypted text: ",txtDEC)

# Test plaintext that is not the correct length
print("\n____________________________________________________")
print("\nTest (2/7): Plaintext that is not the correct length")
print("\nInput:")
print("Plaintext: jeep")
print("Key: RRFVSVCCT")
print("\nOutput:")
txtENC = verander_die.Hill_Encrypt("RRFVSVCCT","jeep")
print("Encrypted text: ",txtENC)
txtDEC = verander_die.Hill_Decrypt("RRFVSVCCT",txtENC)
print("Decrypted text: ",txtDEC)

# Test unsupported plaintext
print("\n____________________________________________________")
print("\nTest (3/7): Unsupported plaintext")
print("\nInput:")
print("Plaintext: The following symbols should not be encrypted: @,#,$,%,^,*,&,*,1,2,3,4.")
print("Key: RRFVSVCCT")
print("\nOutput:")
txtENC = verander_die.Hill_Encrypt("RRFVSVCCT","The following symbols should not be encrypted: @,#,$,%,^,*,&,*,1,2,3,4.")
print("Encrypted text: ",txtENC)
txtDEC = verander_die.Hill_Decrypt("RRFVSVCCT",txtENC)
print("Decrypted text: ",txtDEC)

# Test a 2x2 key matrix
print("\n____________________________________________________")
print("\nTest (4/7): 2x2 key matrix")
print("\nInput:")
print("Plaintext: that's a fat cat")
print("Key: DDCF")
print("\nOutput:")
txtENC = verander_die.Hill_Encrypt("DDCF","that's a fat cat")
print("Encrypted text: ",txtENC)
txtDEC = verander_die.Hill_Decrypt("DDCF",txtENC)
print("Decrypted text: ",txtDEC)

# Test a 3x3 key matrix
print("\n____________________________________________________")
print("\nTest (5/7): 3x3 key matrix")
print("\nInput:")
print("Plaintext: that's a fat cat")
print("Key: RRFVSVCCT")
print("\nOutput:")
txtENC = verander_die.Hill_Encrypt("RRFVSVCCT","that's a fat cat")
print("Encrypted text: ",txtENC)
txtDEC = verander_die.Hill_Decrypt("RRFVSVCCT",txtENC)
print("Decrypted text: ",txtDEC)

# Test image that is not the correct length
print("\n____________________________________________________")
print("\nTest (6/7): Image that is not the correct size")
p_File = Image.open('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\images\office.png')
p_img = np.asarray(p_File)
imgENC = verander_die.Hill_Encrypt("RRFVSVCCT",p_img)
Image.fromarray(imgENC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\images_test\office_enc_hill.png')
imgDEC = verander_die.Hill_Decrypt("RRFVSVCCT",imgENC)
Image.fromarray(imgDEC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\images_test\office_dec_hill.png')

# # Test a when key matrix does not have a modular multiplicative inverse
# print("\n____________________________________________________")
# print("\nTest (7/7): When key matrix does not have a modular multiplicative inverse")
# print("\nInput:")
# print("Plaintext: that's a fat cat")
# print("Key: Aristocat")
# print("\nOutput:")
# txtENC = verander_die.Hill_Encrypt("catamaran","that's a fat cat")
# print("Encrypted text: ",txtENC)
# txtDEC = verander_die.Hill_Decrypt("catamaran",txtENC)
# print("Decrypted text: ",txtDEC)