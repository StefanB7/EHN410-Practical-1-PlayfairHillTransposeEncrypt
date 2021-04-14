from PIL import Image
import numpy as np

p_File = Image.open('EHN410_Prak1_PlayfairHillTransposeEncrypt\jacobus\images\o_alph.png')
p_img = np.asarray(p_File)


print(p_img.shape[2])
