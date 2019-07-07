from PIL import Image
import os
image = Image.open("神2.png")
width, height = image.size


count = 0

folder = "NPC"
for i in range(int(height / 32)):
	for j in range(int(width / 32)):
		image.crop((32 * j,32 * i,32 * (j + 1),32 * (i + 1))).convert('RGBA').save(folder + "/神1 %s.png" % str(j))