# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
import random
import math

fields=(('Please input the length of the test piece(mm):','100'),#0
        ('Please input the width of the test piece(mm):','100'),#1
        ('Please input the aggregate volume ratio (between 0-1):','0.4'),#2
        ('PPlease enter the maximum aggregate size:','20'),#3
        ('Please enter the second aggregate size:','15'),#4
        ('Please enter the third aggregate size:','10'),#5
        ('Please input the minimum size of aggregate:','5'),#6
        ('Please enter the volume ratio of the maximum aggregate(between 0-1);','0.25'), #7
        ('Please enter the volume ratio of the minimum aggregate (between 0-1):','0.5'),#8
        ('Please enter the maximum number of cycles (integer):','300000'))#9
modelparam=getInputs(fields=fields,label='Generation of three graded random aggregate:')

length=float(modelparam[0])
width=float(modelparam[1])

S_gl=length*width*float(modelparam[2])
S_max=S_gl*float(modelparam[7])
S_min=S_gl*float(modelparam[8])
S_mid=S_gl-S_max-S_min

gl_max=float(modelparam[3])
gl_sec=float(modelparam[4])
gl_thr=float(modelparam[5])
gl_min=float(modelparam[6])

count_num=float(modelparam[9])

def intercheck(point,center):
    for p in center:
        if sqrt((p[0]-point[0])**2+(p[1]-point[1])**2)<=point[2]+p[2]+1:
            sign=False
            break
        else:
            sign=True
    return sign

all_yuan=[]

#大圆骨料
dgl_param=[]
S_already=0
S_zuixiaogl=round(0.25*gl_sec*gl_sec*math.pi,2)

while S_max - S_already >= S_zuixiaogl:
    r_gl=round(random.uniform(0.5*gl_sec,0.5*gl_max), 2)
    x_gl=round(random.uniform(-0.48*length+r_gl,0.48*length-r_gl),2)
    y_gl=round(random.uniform(-0.48*width+r_gl,0.48*width-r_gl),2)

    point=[x_gl,y_gl,r_gl]
    if len(all_yuan)==0:
        all_yuan.append(point)
        dgl_param.append(point)
        S_already = S_already + round(math.pi * r_gl * r_gl, 2)
    if intercheck(point,all_yuan):
        all_yuan.append(point)
        dgl_param.append(point)
        S_already=S_already+round(math.pi*r_gl*r_gl,2)
        print(S_already)

print('1_completed')
print('S_max:'+str(S_max))
print('dgl_num:',len(dgl_param))

#中圆骨料
count=0
zgl_param=[]
S_already=0
S_zuixiaogl=round(0.25*gl_thr*gl_thr*math.pi,2)

while S_mid - S_already >= S_zuixiaogl:
    r_gl=round(random.uniform(0.5*gl_thr,0.5*gl_sec), 2)
    x_gl=round(random.uniform(-0.48*length+r_gl,0.48*length-r_gl),2)
    y_gl=round(random.uniform(-0.48*width+r_gl,0.48*width-r_gl),2)

    point=[x_gl,y_gl,r_gl]
    if intercheck(point,all_yuan):
        all_yuan.append(point)
        zgl_param.append(point)
        S_already=S_already+round(math.pi*r_gl*r_gl,2)
        print(S_already)

    count+=1
    if count>count_num:
        break

print('2_completed')
print('S_mid:'+str(S_mid))
print('zgl_num:',len(zgl_param))

#小圆骨料
count=0
xgl_param=[]
S_already=0
S_zuixiaogl=round(0.25*gl_min*gl_min*math.pi,2)

while S_min - S_already >= S_zuixiaogl:
    r_gl=round(random.uniform(0.5*gl_min,0.5*gl_thr), 2)
    x_gl=round(random.uniform(-0.48*length+r_gl,0.48*length-r_gl),2)
    y_gl=round(random.uniform(-0.48*width+r_gl,0.48*width-r_gl),2)

    point=[x_gl,y_gl,r_gl]
    if intercheck(point,all_yuan):
        all_yuan.append(point)
        xgl_param.append(point)
        S_already=S_already+round(math.pi*r_gl*r_gl,2)
        print(S_already)

    count+=1
    if count>count_num:
        break
print('3_completed')
print('S_min:'+str(S_min))
print('xgl_num:',len(xgl_param))

myModel = mdb.models['Model-1']
mySketch = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mySketch.rectangle(point1=(-0.5*length, -0.5*width), point2=(0.5*length, 0.5*width))
myPart = mdb.models['Model-1'].Part(name='Part-1', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
myPart.BaseShell(sketch=mySketch)
f=myPart.faces

for p in all_yuan:
    x, y,r= p[0], p[1], p[2]
    mySketch.CircleByCenterPerimeter(center=(x, y), point1=(x + r, y))
    myPart.PartitionFaceBySketch(faces=f[:], sketch=mySketch)

label1=[]
for  k in dgl_param:
    x=k[0]
    y=k[1]
    z=0
    face=f.findAt((x,y,0),)
    a=f.index(face)
    label1.append(a)
myPart.Set(faces=f[min(label1):max(label1)+1],name='dgl')

label2=[]
for  k in zgl_param:
    x=k[0]
    y=k[1]
    z=0
    face=f.findAt((x,y,z),)
    a=f.index(face)
    label2.append(a)
myPart.Set(faces=f[min(label2):max(label2)+1],name='zgl')

label3=[]
for  k in xgl_param:
    x=k[0]
    y=k[1]
    z=0
    face=f.findAt((x,y,z),)
    a=f.index(face)
    label3.append(a)
myPart.Set(faces=f[min(label3):max(label3)+1],name='xgl')

