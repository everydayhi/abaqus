# -*- coding: mbcs -*-

from abaqus import *
from abaqusConstants import *
import random
import math
import numpy as np

fields=(('Please input the length of the test piece(mm):','100'),#0
        ('Please input the width of the test piece(mm):','100'),#1
        ('Please input the aggregate volume ratio (between 0-1):','0.4'),#2
        ('PPlease enter the maximum aggregate size:','20'),#3
        ('Please enter the second aggregate size:','15'),#4
        ('Please enter the third aggregate size:','10'),#5
        ('Please input the minimum size of aggregate:','5'),#6
        ('Please enter the volume ratio of the maximum aggregate(between 0-1);','0.25'), #7
        ('Please enter the volume ratio of the minimum aggregate (between 0-1):','0.5'),#8
        ('Please enter the maximum number of cycles (integer):','600000'),#9
        ('Please enter the minmum number of edges (integer):','4'),#10
        ('Please enter the maximum number of edges (integer):','6'),#11
        ('Please enter the pore ratio:', '0.05'))  # 12
modelparam=getInputs(fields=fields,label='Generation of three graded random aggregate:')

length=float(modelparam[0])
width=float(modelparam[1])

S_gl=length*width*float(modelparam[2])
S_max=S_gl*float(modelparam[7])
S_min=S_gl*float(modelparam[8])
S_mid=S_gl-S_max-S_min
S_kongxi=length*width*float(modelparam[12])

gl_max=float(modelparam[3])
gl_sec=float(modelparam[4])
gl_thr=float(modelparam[5])
gl_min=float(modelparam[6])

count_num=float(modelparam[9])

edge_min=float(modelparam[10])
edge_max=float(modelparam[11])

def intercheck(point,center1):
    sign=True
    for center in center1:
        if sqrt((center[0]-point[0])**2+(center[1]-point[1])**2)<=center[2]+point[2]+0.5:
            sign=False
            break
    return sign

s1=mdb.models['Model-1'].ConstrainedSketch(name='Partition',sheetSize=282, gridSpacing=7, )

center1=[]

#大骨料
count=0
area1=0
S_already=0
dgl_param=[]
S_zuixiaogl=round(0.25*gl_sec*gl_sec*math.pi,2)

while S_max - S_already >= S_zuixiaogl:
    radius=random.uniform(0.5*gl_sec,0.5*gl_max)
    x=random.uniform(-0.48*length+radius,0.48*length-radius)
    y=random.uniform(-0.48*width+radius,0.48*width-radius)
    point=(x,y,radius)
    p1 =np.array([x,y])#圆心点

    if len(center1)==0:
        center1.append(point)
        dgl_param.append(point)
        edge = random.randint(edge_min,edge_max)#定边

        points=[]  #给每个区域确定一个点
        for g in range(edge):
            angle=random.uniform(2*math.pi*g/edge+math.pi/9, 2*math.pi*(g+1)/edge-math.pi/9)
            dx=x+radius*math.cos(angle)
            dy=y+radius*math.sin(angle)
            points.append([dx,dy])

        #把点连成线
        for edge_num in  range(edge-1):
            s1.Line(point1=points[edge_num],point2=points[edge_num+1])
            # 计算多边形面积
            A =np.array(points[edge_num])  - p1
            B =np.array(points[edge_num+1] ) - p1
            A_B = np.cross(A,B)
            AB_mo1 = np.linalg.norm(A_B)
            area1 =area1+AB_mo1 / 2

        s1.Line(point1=points[-1],point2=points[0])
        A = np.array(points[0]) - p1
        B = np.array(points[-1]) - p1
        A_B = np.cross(A, B)
        AB_mo2 = np.linalg.norm(A_B)
        S_already = S_already+area1+(AB_mo2/2)
        print(S_already)

    area2 = 0
    if intercheck(point,center1):
        center1.append(point)
        dgl_param.append(point)
        edge = random.randint(edge_min, edge_max)#定边

        points1 = []  # 给每个区域确定一个点
        for g in range(edge):
            angle = random.uniform(2 * math.pi * g / edge + math.pi / 9, 2 * math.pi * (g + 1) / edge - math.pi / 9)
            dx = x + radius * math.cos(angle)
            dy = y + radius * math.sin(angle)
            points1.append([dx,dy])
        #把点连成线
        for edge_num in  range(edge-1):
            s1.Line(point1=points1[edge_num],point2=points1[edge_num+1])
            # 计算多边形面积
            A =np.array(points1[edge_num])  - p1
            B =np.array(points1[edge_num+1] ) - p1
            A_B = np.cross(A,B)
            AB_mo = np.linalg.norm(A_B)
            area2 =area2+AB_mo / 2

        s1.Line(point1=points1[-1],point2=points1[0])
        A = np.array(points1[-1]) - p1
        B = np.array(points1[0]) - p1
        A_B = np.cross(A, B)
        AB_mo = np.linalg.norm(A_B)
        S_already = S_already+area2+(AB_mo/2)
        print(S_already)

    count += 1
    if count > count_num:
        break

print('1_completed')
print('S_max:'+str(S_max))
print('dgl_num:',len(dgl_param))


#中骨料
count=0
S_already=0
zgl_param=[]
S_zuixiaogl=round(0.25*gl_thr*gl_thr*math.pi,2)

while S_mid - S_already >= S_zuixiaogl:
    radius=random.uniform(0.5*gl_thr,0.5*gl_sec)
    x=random.uniform(-0.48*length+radius,0.48*length-radius)
    y=random.uniform(-0.48*width+radius,0.48*width-radius)
    point=(x,y,radius)
    p1 =np.array([x,y])

    if intercheck(point,center1):
        center1.append(point)
        zgl_param.append(point)
        edge = random.randint(edge_min, edge_max)#定边

        points2=[]#给每个区域确定一个点
        for g in range(edge):
            angle=random.uniform(2*math.pi*g/edge+math.pi/9, 2*math.pi*(g+1)/edge-math.pi/9)
            dx=x+radius*math.cos(angle)
            dy=y+radius*math.sin(angle)
            points2.append([dx,dy])
        area = 0
        #把点连成线
        for edge_num in  range(edge-1):
            s1.Line(point1=points2[edge_num],point2=points2[edge_num+1])
            # 计算多边形面积
            A =np.array(points2[edge_num])  - p1
            B =np.array(points2[edge_num+1] ) - p1
            A_B = np.cross(A,B)
            AB_mo = np.linalg.norm(A_B)
            area =area+(AB_mo/2)

        s1.Line(point1=points2[-1],point2=points2[0])
        A = np.array(points2[-1]) - p1
        B = np.array(points2[0]) - p1
        A_B = np.cross(A, B)
        AB_mo = np.linalg.norm(A_B)
        S_already =S_already+area+(AB_mo/2)
        print(S_already)

    count += 1
    if count > count_num:
        break

print('2_completed')
print('S_mid:'+str(S_mid))
print('zgl_num:',len(zgl_param))

#小骨料
count=0
S_already=0
xgl_param=[]
S_zuixiaogl=round(0.25*gl_min*gl_min*math.pi,2)

while S_min - S_already >= S_zuixiaogl:
    radius=random.uniform(0.5*gl_min,0.5*gl_thr)
    x=random.uniform(-0.48*length+radius,0.48*length-radius)
    y=random.uniform(-0.48*width+radius,0.48*width-radius)
    point=(x,y,radius)
    p1 =np.array([x,y])

    if intercheck(point,center1):
        center1.append(point)
        xgl_param.append(point)
        edge = random.randint(edge_min, edge_max)#定边

        points3=[]#给边划分区域并在每个区域确定一个点
        for g in range(edge):
            angle=random.uniform(2*math.pi*g/edge+math.pi/9, 2*math.pi*(g+1)/edge-math.pi/9)
            dx=x+radius*math.cos(angle)
            dy=y+radius*math.sin(angle)
            points3.append([dx,dy])

        area = 0
        #把点连成线
        for edge_num in  range(edge-1):
            s1.Line(point1=points3[edge_num],point2=points3[edge_num+1])
            # 计算多边形面积
            A =np.array(points3[edge_num])  - p1
            B =np.array(points3[edge_num+1] ) - p1
            A_B = np.cross(A,B)
            AB_mo = np.linalg.norm(A_B)
            area =area+(AB_mo/2)

        s1.Line(point1=points3[-1],point2=points3[0])
        A = np.array(points3[-1]) - p1
        B = np.array(points3[0]) - p1
        A_B = np.cross(A, B)
        AB_mo = np.linalg.norm(A_B)
        S_already=S_already+area+(AB_mo/2)
        print(S_already)

    count += 1
    if count > count_num:
        break

print('3_completed')
print('S_min:'+str(S_min))
print('xgl_num:',len(xgl_param))

#孔洞
count=0
kongxi_param=[]
S_already=0
r_gl=1.5

while S_kongxi > S_already:
    x_gl=round(random.uniform(-0.49*length+r_gl,0.49*length-r_gl),2)
    y_gl=round(random.uniform(-0.49*width+r_gl,0.49*width-r_gl),2)

    point=[x_gl,y_gl,r_gl]
    if intercheck(point,center1):
        center1.append(point)
        kongxi_param.append(point)
        s1.CircleByCenterPerimeter(center=(point[0], point[1]), point1=(point[0] + r_gl, point[1]))
        S_already=S_already+round(math.pi*r_gl*r_gl,2)
        print(S_already)

    count+=1
    if count>count_num:
        break
print('4_completed')
print('S_kongxi:'+str(S_already))
print('kongxi_num:',len(kongxi_param))

if mdb.models.has_key('Model-1'):
    mymodel=mdb.models['Model-1']
else:
    mymodel=mdb.Model(name='Model-1',modelType=STANDRD_EXPLICIT)
s = mdb.models['Model-1'].ConstrainedSketch(name='base', sheetSize=200.0)
s.rectangle(point1=(-0.5*length,-0.5*width), point2=(0.5*length,0.5*width))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=TWO_D_PLANAR,
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseShell(sketch=s)
p.PartitionFaceBySketch(faces=p.faces[:], sketch=s1)
f=p.faces

face1=[]
for  k in dgl_param:
    a=f.findAt(((k[0],k[1], 0), ))
    face1.append(a)
p.Set(faces=face1,name='dgl')

face2=[]
for  k in zgl_param:
    a=f.findAt(((k[0],k[1], 0), ))
    face2.append(a)
p.Set(faces=face2,name='zgl')

face3=[]
for  k in xgl_param:
    a=f.findAt(((k[0],k[1], 0), ))
    face3.append(a)
p.Set(faces=face3,name='xgl')

for  k in kongxi_param:
    x=k[0]
    y=k[1]
    z=0
    face=f.findAt((x,y,z),)
    a=f.index(face)
    p.RemoveFaces(faceList=f[a:a+1], deleteCells=False)