from PIL import Image
import os
image = Image.open("n.png")
width, height = image.size


count = 0

folder = "數"
for i in range(int(height / 32)):
	for j in range(int(width / 32)):
		image.crop((32 * j,32 * i,32 * (j + 1),32 * (i + 1))).convert('RGBA').save(folder + "/%s.png" % str(j))