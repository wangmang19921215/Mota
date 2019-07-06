from PIL import Image
import os
image = Image.open("勇者.png")
width, height = image.size


count = 0

folder = "resources/勇者"
c = ["Down","Left","Right","Up"]
for i in range(int(height / 32)):
	for j in range(int(width / 32)):
		image.crop((32 * j,32 * i,32 * (j + 1),32 * (i + 1))).convert('RGBA').save(folder + "/%s.png" % (c[i] + " " + str(j)))