from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
from random import randint
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter

iar = np.empty([100, 100], dtype=float)
iar_two = np.empty([100, 100], dtype = float)
x2 = np.empty([100, 1], dtype = float)
y2 = np.empty([100, 1], dtype = float)

#create empty 100x100 array

a = 0
for b in range(100):
    iar [a,b] = 10
for a in range (1,99):
    iar[a,0] = 10
    for b in range (1,99):
        iar[a,b] = 10
    iar[a,99] = 10
a = 99
for b in range(100):
    iar [a,b] = 10
#populate np array with initial mountain

for c in range(1000):
    a = randint(1,99)
    b = randint(1,99)
    c= randint(-30,30)/10
    iar[a,b] += c

for a in range (100):
    for b in range(100):
        iar[a,b] += (a/10)

erodecount = 0
depocount = 0

for k in range (4*10**4):
    rainx = randint(1,98)
    rainy = randint(1,98)
    starth = iar[rainx,rainy]
    #height of start
    lowesth = starth
    #initial value of lowest height
    lowestc=[]  
    #direction of lowest height
    lowestcs = []
    #collects directions of lowest heights
    downhill=[]
    #heights of surrounding area
    v = 1
    #initial velocity, could be 0 but how would erode peak?
    soilcarry = 0
    stepcount = 0
    endrun = 0
    #initial conditions for rain
    while rainx>1 and rainx<98 and rainy>1 and rainy<98 and endrun == 0:
        downhill =[]
        starth = iar[rainx,rainy]
        for l in range(-1,2):
            for m in range(-1,2):
                downhill.append(iar[rainx+l,rainy+m])
        for l in range(-1,2):
            for m in range(-1,2):
                if iar[rainx+l,rainy+m]==min(downhill):
                    lowestcs.append([l,m])
                else:
                    pass
        lowesth = min(downhill)
        #set lowest to minimum
        if len(lowestcs)>1:
            dirchoose = randint(0,len(lowestcs)-1)
            lowestc = lowestcs[dirchoose]
        else:
            lowestc = lowestcs[0]
        ##print(k,rainx,rainy,iar[rainx,rainy],lowestc,lowesth)
        #find lowest point
        rainslope = (starth - lowesth)
        v = rainslope
        soilcarrycap = v * 10
        ##print(v, soilcarrycap,soilcarry)
        if rainslope == 0:
            iar[rainx,rainy] += soilcarry
            soilcarry = 0
            endrun = 1
        else:
            pass
        if soilcarrycap>=soilcarry:
            erode = (soilcarrycap - soilcarry)
            if erode > rainslope:
                erode = rainslope
            else:
                pass
            soilcarry += erode
            iar[rainx,rainy] -= erode
            erodecount += erode
            ##print('erode', erode)
        else:
        #(soilcarrycap<soilcarry, = deposition)
            depo = (soilcarry - soilcarrycap)            
            if depo>=rainslope:
                depo =rainslope
            else:
                pass
            #does this work if we are at the low?
            soilcarry -= depo
            iar[rainx,rainy] += depo
            depocount += depo
            ##print('depo',depo)
        #erosion/deposition
        rainx = rainx + lowestc[0]
        rainy = rainy + lowestc[1]
        #move water


for j in range(100):
    y2[j,0] = iar[50,j]
    x2[j,0] = j
#take slice for profile

'''x3 = np.empty([100, 100])
y3 = np.empty([100, 100])
z3 = iar
for j in range(100):
    for k in range(100):
    x3[j,k] = [j,k]
    #how do the nps that feed a 3d plot work???'''
x3 = np.arange(0, 100, 1)
y3 = np.arange(0, 100, 1)
x3, y3 = np.meshgrid(x3, y3)
z3 = iar

'''
def updatefig(*args):
    global iar
    for x in range(1,99):
        for y in range(1,99):
            cellcount = 0
            for xx in range(x-1,x+2):
                for yy in range(y-1,y+2):
                    if iar[xx,yy]==1:
                        cellcount +=1
                    else:
                        pass
            cellcount -= iar[x,y]
#            print(x,y,iar[x,y],cellcount)
            if cellcount >1 and cellcount <4 and iar[x,y] == 1:
                iar_two[x,y] = 1
            elif cellcount == 3 and iar[x,y] == 0:
                iar_two[x,y] = 1
            elif cellcount >3:
                iar_two[x,y] = 0
            elif cellcount <2:
                iar_two[x,y] = 0
            else:
                iar_two[x,y] = 0
    iar = iar_two
    im.set_array(iar)
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=500)
'''

print(erodecount,depocount)

plt.subplot(2, 1, 1)
#plt.figure()
plt.imshow(iar, 'CMRmap_r', interpolation='none')

plt.subplot(2, 1, 2)
plt.plot(x2, y2, 'r.-')
plt.xlabel('cross-section (m)')
plt.ylabel('altitude (m)')

#plt.subplot(3, 1, 3)
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(x3,y3,z3,cmap='CMRmap_r', linewidth=0)
ax.set_zlim(0,50)

plt.show()

