from PIL import Image
import random
import sys
import time

start_time = time.time()

img_height = 2000
img_width = 2000

sector_height = 5
sector_width = 5

if img_height%sector_height!=0 or img_width%sector_width!=0:
    print("Improper total/sector size. Try reevaluating so that image%sector == 0.")
    sys.exit()
vertical_div = int(img_height / sector_height)
horizontal_div = int(img_width / sector_width)

sector_total = int(vertical_div * horizontal_div)

sector_map = []
x_bounds = {}
y_bounds = {}

img = Image.new('RGBA', (img_width, img_height))
pixels = img.load()
global redcount
redcount = 0
for i in range(horizontal_div+1):
    key_string = 'x'+ str(i)
    x_bounds[key_string] = i*sector_width
for i in range(vertical_div+1):
    key_string = 'y'+ str(i)
    y_bounds[key_string] = i*sector_height


test_location = [8, 17]
##for i in range(x_bounds['x1']):
##    for j in range(y_bounds['y1']):
##        pixels[i, j] = (0, 255, 150, 255)

print(x_bounds)
x_bound_size = len(x_bounds)
y_bound_size = len(y_bounds)

def colorCode(x, y):
    global redcount
    pixels[x, y] = (redcount, redcount, 255, 255)
    redcount += 1
    if redcount==255:
        redcount=0
##    print(redcount)
    
for i in range(x_bound_size):
##    print(i)
    key_string = 'x'+str(i)
    if i==0:
        for x in range(x_bounds[key_string]):
            pass
    elif i>0:
        old_key = 'x'+str(i-1)
        for x in range(x_bounds[old_key], x_bounds[key_string]):
##            img.save('Blork.png')
##            time.sleep(2)
            for j in range(y_bound_size):
                koy_strong = 'y'+str(j)
                if j>0:
                    old_koy = 'y'+str(j-1)
                    for y in range(y_bounds[old_koy], y_bounds[koy_strong]):
                        colorCode(x, y)
##                        pixels[x, y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)

print('Image processed in {} seconds'.format(time.time() - start_time))
start_save = time.time()
img.save('BlorkTest.png')
print('Image saved in {} seconds'.format(time.time() - start_save))
