
# # print(Hill_Encrypt("RRFVSVCCT","jannieensannie"))
# # print(Hill_Decrypt("RRFVSVCCT","xxghjxnalnaaesj"))

# p_File = Image.open('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\o_blue.png')
# p_img = np.asarray(p_File)

# #print(p_img)

# print("___________________________________________")

# img_enc = Hill_Encrypt("RRFVSVCCT",p_img)
# print("half")
# img_dec = Hill_Decrypt("RRFVSVCCT",img_enc)

# #print((Image.fromarray(img_dec.astype(np.uint8))).size)

# Image.fromarray(img_enc.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\o_blue_encrypted.png')
# Image.fromarray(img_dec.astype(np.uint8)).save('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\o_blue_decrypted.png')

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


class dieiscool(Exception):
    pass

raise dieiscool("die is n custom error")