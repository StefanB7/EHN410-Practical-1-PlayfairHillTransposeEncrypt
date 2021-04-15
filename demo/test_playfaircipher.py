from PIL import Image
import numpy as np
import importlib
EHN_Group7 = importlib.import_module("EHN_Group7")

txtENC = ""
txtDEC = ""

imgENC = None
imgDEC = None

##### TEXT DECRYPTION AND ENCRYPTION TESTING #####

# Test plaintext that is too small 
print("\n____________________________________________________")
print("\nTest (1/7): Plaintext that is too small")
print("\nInput:")
print("Plaintext: a")
print("Key: StefanJacobus")
print("\nOutput:")
txtENC = EHN_Group7.Playfair_Encrypt("StefanJacobus","a")
print("Encrypted text: ",txtENC)
txtDEC = EHN_Group7.Playfair_Decrypt("StefanJacobus",txtENC)
print("Decrypted text: ",txtDEC)
print("Key matrix:\n",EHN_Group7.Get_Playfair_Encryption_Matrix())

# Test plaintext that is not the correct length
print("\n____________________________________________________")
print("\nTest (2/7): Plaintext that is not the correct length")
print("\nInput:")
print("Plaintext: We have been captured, cease all communication")
print("Key: ElongMusk")
print("\nOutput:")
txtENC = EHN_Group7.Playfair_Encrypt("ElongMusk","We have been captured, cease all communication")
print("Encrypted text: ",txtENC)
txtDEC = EHN_Group7.Playfair_Decrypt("ElongMusk",txtENC)
print("Decrypted text: ",txtDEC)
print("Key matrix:\n",EHN_Group7.Get_Playfair_Encryption_Matrix())

# Test unsupported plaintext
print("\n____________________________________________________")
print("\nTest (3/7): Unsupported plaintext")
print("\nInput:")
print("Plaintext: The following symbols should not be encrypted: @,#,$,%,^,*,&,*,1,2,3,4.")
print("Key: UgandaKenyaNigeria")
print("\nOutput:")
txtENC = EHN_Group7.Playfair_Encrypt("UgandaKenyaNigeria","The following symbols should not be encrypted: @,#,$,%,^,*,&,*,1,2,3,4.")
print("Encrypted text: ",txtENC)
txtDEC = EHN_Group7.Playfair_Decrypt("UgandaKenyaNigeria",txtENC)
print("Decrypted text: ",txtDEC)
print("Key matrix:\n",EHN_Group7.Get_Playfair_Encryption_Matrix())

#Test a long key:
print("\n____________________________________________________")
print("\nTest (4/7): long key")
print("\nInput:")
print("Plaintext: that's a fat cat")
print("Key: theenemyiswithinandwemig")
print("\nOutput:")
txtENC = EHN_Group7.Playfair_Encrypt("theenemyiswithinandwemig","that's a fat cat")
print("Encrypted text: ",txtENC)
txtDEC = EHN_Group7.Playfair_Decrypt("theenemyiswithinandwemig",txtENC)
print("Decrypted text: ",txtDEC)
print("Key matrix:\n",EHN_Group7.Get_Playfair_Encryption_Matrix())

# Test a long plaintext
print("\n____________________________________________________")
print("\nTest (5/7): long plaintext")
print("\nInput:")
print("Plaintext: Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma – which is living with the results of other people's thinking. - Steve Jobs")
print("Key: rickastley")
print("\nOutput:")
txtENC = EHN_Group7.Playfair_Encrypt("rickastley","Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma – which is living with the results of other people's thinking. - Steve Jobs")
print("Encrypted text: ",txtENC)
txtDEC = EHN_Group7.Playfair_Decrypt("rickastley",txtENC)
print("Decrypted text: ",txtDEC)
print("Key matrix:\n",EHN_Group7.Get_Playfair_Encryption_Matrix())

##### IMAGE DECRYPTION AND ENCRYPTION TESTING #####

#Test image encryption and decryption
print("\n____________________________________________________")
print("\nTest (6/7): Normal image encryption and decryption")
print("Key: JacobusStefanEHNPrakties")
p_File = Image.open('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\\berge.png')
p_img = np.asarray(p_File)
imgENC = EHN_Group7.Playfair_Encrypt("JacobusStefanEHNPrakties",p_img)
Image.fromarray(imgENC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\mountains_encrypted_playfair.png')
imgDEC = EHN_Group7.Playfair_Decrypt("JacobusStefanEHNPrakties",imgENC)
Image.fromarray(imgDEC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\mountains_decrypted_playfair.png')
print("Key matrix:\n",EHN_Group7.Get_Playfair_Encryption_Matrix())

#Test another image encryption and decryption
print("\n____________________________________________________")
print("\nTest (7/7): Normal image encryption and decryption")
print("Key: Therearenobearsinsouthaf")
p_File = Image.open('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\\beer.png')
p_img = np.asarray(p_File)
imgENC = EHN_Group7.Playfair_Encrypt("Therearenobearsinsouthaf",p_img)
Image.fromarray(imgENC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\\bear_encrypted_playfair.png')
imgDEC = EHN_Group7.Playfair_Decrypt("Therearenobearsinsouthaf",imgENC)
Image.fromarray(imgDEC.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\demo\\bear_decrypted_playfair.png')
print("Key matrix:\n",EHN_Group7.Get_Playfair_Encryption_Matrix())