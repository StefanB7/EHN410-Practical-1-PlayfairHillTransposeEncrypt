from PIL import Image
import numpy as np
import importlib
EHN_Group7 = importlib.import_module("EHN_Group7")

txtENC = ""
txtDEC = ""

imgENC = None
imgDEC = None

# Test plaintext that is too small 
print("\n____________________________________________________")
print("\nTest (1/9): Plaintext that is too small")
print("\nInput:")
print("Plaintext: a")
print("Key: RRFVSVCCT")
print("\nOutput:")
txtENC = EHN_Group7.Hill_Encrypt("RRFVSVCCT","a")
print("Encrypted text: ",txtENC)
txtDEC = EHN_Group7.Hill_Decrypt("RRFVSVCCT",txtENC)
print("Decrypted text: ",txtDEC)
print("Key matrix:\n",EHN_Group7.Get_Hill_Encryption_Matrix())


# Test plaintext that is not the correct length
print("\n____________________________________________________")
print("\nTest (2/9): Plaintext that is not the correct length")
print("\nInput:")
print("Plaintext: jeep")
print("Key: RRFVSVCCT")
print("\nOutput:")
txtENC = EHN_Group7.Hill_Encrypt("RRFVSVCCT","jeep")
print("Encrypted text: ",txtENC)
txtDEC = EHN_Group7.Hill_Decrypt("RRFVSVCCT",txtENC)
print("Decrypted text: ",txtDEC)
print("Key matrix:\n",EHN_Group7.Get_Hill_Encryption_Matrix())

# Test unsupported plaintext
print("\n____________________________________________________")
print("\nTest (3/9): Unsupported plaintext")
print("\nInput:")
print("Plaintext: The following symbols should not be encrypted: @,#,$,%,^,*,&,*,1,2,3,4.")
print("Key: RRFVSVCCT")
print("\nOutput:")
txtENC = EHN_Group7.Hill_Encrypt("RRFVSVCCT","The following symbols should not be encrypted: @,#,$,%,^,*,&,*,1,2,3,4.")
print("Encrypted text: ",txtENC)
txtDEC = EHN_Group7.Hill_Decrypt("RRFVSVCCT",txtENC)
print("Decrypted text: ",txtDEC)
print("Key matrix:\n",EHN_Group7.Get_Hill_Encryption_Matrix())

# Test a 2x2 key matrix
print("\n____________________________________________________")
print("\nTest (4/9): 2x2 key matrix")
print("\nInput:")
print("Plaintext: that's a fat cat")
print("Key: DDCF")
print("\nOutput:")
txtENC = EHN_Group7.Hill_Encrypt("DDCF","that's a fat cat")
print("Encrypted text: ",txtENC)
txtDEC = EHN_Group7.Hill_Decrypt("DDCF",txtENC)
print("Decrypted text: ",txtDEC)
print("Key matrix:\n",EHN_Group7.Get_Hill_Encryption_Matrix())

print("\n____________________________________________________")
print("\nTest (5/9): Return of the key matrix")
print(EHN_Group7.Get_Hill_Encryption_Matrix())

# Test a 3x3 key matrix
print("\n____________________________________________________")
print("\nTest (6/9): 3x3 key matrix")
print("\nInput:")
print("Plaintext: that's a fat cat")
print("Key: RRFVSVCCT")
print("\nOutput:")
txtENC = EHN_Group7.Hill_Encrypt("RRFVSVCCT","that's a fat cat")
print("Encrypted text: ",txtENC)
txtDEC = EHN_Group7.Hill_Decrypt("RRFVSVCCT",txtENC)
print("Decrypted text: ",txtDEC)
print("Key matrix:\n",EHN_Group7.Get_Hill_Encryption_Matrix())

# Test image that is not the correct length
# print("\n____________________________________________________")
# print("\nTest (6/9): Image 1")
# p_File = Image.open('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\\berge.png')
# p_img = np.asarray(p_File)
# imgENC = EHN_Group7.Hill_Encrypt("RRFVSVCCT",p_img)
# Image.fromarray(imgENC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\mountains_encrypted_hill.png')
# imgDEC = EHN_Group7.Hill_Decrypt("RRFVSVCCT",imgENC)
# Image.fromarray(imgDEC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\mountains_decrypted_hill.png')
# print("Key matrix:\n",EHN_Group7.Get_Hill_Encryption_Matrix())

# Correct sized image
# print("\n____________________________________________________")
# print("\nTest (7/9): Image 2")
# p_File = Image.open('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\\beer.png')
# p_img = np.asarray(p_File)
# imgENC = EHN_Group7.Hill_Encrypt("RRFVSVCCT",p_img)
# Image.fromarray(imgENC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\\bear_encrypted_hill.png')
# imgDEC = EHN_Group7.Hill_Decrypt("RRFVSVCCT",imgENC)
# Image.fromarray(imgDEC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\\bear_decrypted_hill.png')
# print("Key matrix:\n",EHN_Group7.Get_Hill_Encryption_Matrix())

print("\n____________________________________________________")
print("\nTest (8/9): Image that is not the correct size")
p_File = Image.open('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\img1_Low.png')
p_img = np.asarray(p_File)
imgENC = EHN_Group7.Hill_Encrypt("RRFVSVCCT",p_img)
Image.fromarray(imgENC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\img1_Low_enc.png')
imgDEC = EHN_Group7.Hill_Decrypt("RRFVSVCCT",imgENC)
Image.fromarray(imgDEC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\img1_Low_dec.png')
print("Key matrix:\n",EHN_Group7.Get_Hill_Encryption_Matrix())

# # Test a when key matrix does not have a modular multiplicative inverse
# print("\n____________________________________________________")
# print("\nTest (9/9): When key matrix does not have a modular multiplicative inverse")
# print("\nInput:")
# print("Plaintext: that's a fat cat")
# print("Key: Aristocat")
# print("\nOutput:")
# txtENC = EHN_Group7.Hill_Encrypt("catamaran","that's a fat cat")
# print("Encrypted text: ",txtENC)
# txtDEC = EHN_Group7.Hill_Decrypt("catamaran",txtENC)
# print("Decrypted text: ",txtDEC)
# print("Key matrix:\n",EHN_Group7.Get_Hill_Encryption_Matrix())