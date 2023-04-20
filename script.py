
from ppadb.client import Client as AdbClient
import numpy 
from PIL import Image

adb=AdbClient(host="127.0.0.1",port=5037)
devices=adb.devices()

if len(devices)==0:
    print("No device attached")
    quit()
    
device=devices[0]
image=device.screencap()
with open("screen.png","wb") as f:
    f.write(image)
    
image=Image.open("screen.png")
image=numpy.array(image)
pixels=[]
spaces=[]
space=[]

for i in image[1200] :
        row=list(i[:3])
        # if(row!=[66, 93, 165] and row!=[74, 97, 165] and row!=[74, 93, 165] and row!=[57, 81, 173] and row!=[49, 73, 132] and row!=[41, 60, 107]):
            # if(pixels.count(row)==0):
        pixels.append(row)
                # spaces.append('rgb('+str(row[0])+","+str(row[1])+","+str(row[2])+")")

for i in range(834,835):
    for j in image[i]:
        row=list(j[:3])
        if space.count(row)==0:
            space.append(row)
            spaces.append('rgb('+str(row[0])+","+str(row[1])+","+str(row[2])+")")    
    
        
with open("pixels.jsx","wb") as f:
     f.write(str(pixels).encode("utf-8"))

box=False
ignore=True
transitions=[]
for i,pixel in enumerate(pixels):
    # print (pixel)
    if ignore and pixel not in space:
        continue
    ignore = False
    if box and pixel not in space:
        box=not box
        transitions.append(i)
        continue
    if not box and pixel in space:
        box=not box
        transitions.append(i)
        continue

print(transitions)
    
    