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