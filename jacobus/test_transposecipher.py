#### !!!!! verander hill_cipher nog na die final combination script !!!!!

from PIL import Image
import numpy as np
import importlib
verander_die = importlib.import_module("twostagetransposition_cipher")

txtENC = ""
txtDEC = ""

imgENC = None
imgDEC = None

# Test plaintext that is too small 
print("\n____________________________________________________")
print("\nTest (1/5): Plaintext that is too small")
print("\nInput:")
print("Plaintext: jeep")
print("Key: bigapple")
print("\nOutput:")
txtENC = verander_die.Transpose_Encrypt("bigapple",1,"jeep")
print("Encrypted text: ",txtENC)
txtDEC = verander_die.Transpose_Decrypt("bigapple",1,txtENC)
print("Decrypted text: ",txtDEC)

# Test plaintext that is not the correct length
print("\n____________________________________________________")
print("\nTest (2/5): Plaintext that is not the correct length")
print("\nInput:")
print("Plaintext: this sentence is not long enough")
print("Key: bigapple")
print("\nOutput:")
txtENC = verander_die.Transpose_Encrypt("bigapple",1,"this sentence is not long enough")
print("Encrypted text: ",txtENC)
txtDEC = verander_die.Transpose_Decrypt("bigapple",1,txtENC)
print("Decrypted text: ",txtDEC)

# Test unsupported plaintext
print("\n____________________________________________________")
print("\nTest (3/5): Unsupported plaintext")
print("\nInput:")
print("Plaintext: The following symbols should not be encrypted: @,#,$,%,^,*,&,*,1,2,3,4.")
print("Key: bigapple")
print("\nOutput:")
txtENC = verander_die.Transpose_Encrypt("bigapple",1,"The following symbols should not be encrypted: @,#,$,%,^,*,&,*,1,2,3,4.")
print("Encrypted text: ",txtENC)
txtDEC = verander_die.Transpose_Decrypt("bigapple",1,txtENC)
print("Decrypted text: ",txtDEC)

# Single stage encryption and decryption
print("\n____________________________________________________")
print("\nTest (4/5): Single stage encryption and decryption")
print("\nInput:")
print("Plaintext: that's a fat cat")
print("Key: bigapple")
print("\nOutput:")
txtENC = verander_die.Transpose_Encrypt("bigapple",1,"that's a fat cat")
print("Encrypted text: ",txtENC)
txtDEC = verander_die.Transpose_Decrypt("bigapple",1,txtENC)
print("Decrypted text: ",txtDEC)

# Double stage encryption and decryption
print("\n____________________________________________________")
print("\nTest (5/5): Double stage encryption and decryption")
print("\nInput:")
print("Plaintext: that's a fat cat")
print("Key: bigapple")
print("\nOutput:")
txtENC = verander_die.Transpose_Encrypt("bigapple",2,"that's a fat cat")
print("Encrypted text: ",txtENC)
txtDEC = verander_die.Transpose_Decrypt("bigapple",2,txtENC)
print("Decrypted text: ",txtDEC)
