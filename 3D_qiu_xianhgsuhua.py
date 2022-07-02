# encoding=utf-8
from abaqus import *
from abaqusConstants import *
import random
from caeModules import *
import numpy as np
import math
from numpy import pi,sin,cos,arccos

fields=(('Please input the length of the test piece(mm):','100'),#0
        ('Please input the width of the test piece(mm):','100'),#1
        ('Please input the height of the test piece(mm):','100'),#2
        ('Size of seed (integer):','2.5'),#3
        ('Please input the aggregate volume ratio (between 0-1):','0.4'),#4
        ('PPlease enter the maximum aggregate size:','20'),#5
        ('Please enter the second aggregate size:','15'),#6
        ('Please enter the third aggregate size:','10'),#7
        ('Please input the minimum size of aggregate:','5'),#8
        ('Please enter the volume ratio of the maximum aggregate(between 0-1);','0.25'), #9
        ('Please enter the volume ratio of the minimum aggregate (between 0-1):','0.5'),#10
        ('Please enter the maximum number of cycles (integer):','800000'))#11
modelparam=getInputs(fields=fields,label='Generation of three graded random aggregate:')

chang=float(modelparam[0])
kuan=float(modelparam[1])
gao=float(modelparam[2])
buzhong=float(modelparam[3])

V_gl=chang*kuan*gao*float(modelparam[4])

gl_max=float(modelparam[5])
gl_sec=float(modelparam[6])
gl_thr=float(modelparam[7])
gl_min=float(modelparam[8])

V_max=V_gl*float(modelparam[9])
V_min=V_gl*float(modelparam[10])
V_mid=V_gl-V_max-V_min

xh_max=float(modelparam[11])

print(V_max,V_mid,V_min)

list_qiu=[]
#大骨料
list_dgl=[]
v_ls=0
V_ls=round(pi*gl_max**3/6,2)

while V_max-v_ls >=V_ls:
    if len(list_qiu)== 0:
        x_gl=round(random.uniform(-0.5*chang+0.5*gl_max,0.5*chang-0.5*gl_max),2)
        y_gl=round(random.uniform(-0.5*kuan+0.5*gl_max,0.5*kuan-0.5*gl_max),2)
        z_gl=round(random.uniform(0.5*gl_max,gao-0.5*gl_max),2)

        r_gl=round(random.uniform(0.5*gl_sec,0.5*gl_max),2)

        list_qiu.append([x_gl,y_gl,z_gl,r_gl])
        list_dgl.append([x_gl,y_gl,z_gl,r_gl])

        v_ls = round(4 *pi* r_gl ** 3 / 3, 2) + v_ls
        print('-----%.2f%%-----' % (v_ls * 100 / V_max))
    else:
        x_gl=round(random.uniform(-0.5*chang+0.5*gl_max,0.5*chang-0.5*gl_max),2)
        y_gl=round(random.uniform(-0.5*kuan+0.5*gl_max,0.5*kuan-0.5*gl_max),2)
        z_gl=round(random.uniform(0.5*gl_max,gao-0.5*gl_max),2)

        r_gl=round(random.uniform(0.5*gl_sec,0.5*gl_max),2)

        m0=0
        m1=len(list_qiu)
        while m0 < m1 :
            x1=list_qiu[m0][0]
            y1=list_qiu[m0][1]
            z1=list_qiu[m0][2]

            r1=list_qiu[m0][3]

            qq=((x_gl-x1)**2+(y_gl-y1)**2+(z_gl-z1)**2)**0.5
            if qq < r1+r_gl:
                break
            m0+=1
        else:
            list_qiu.append([x_gl,y_gl,z_gl,r_gl])
            list_dgl.append([x_gl,y_gl,z_gl,r_gl])

            v_ls = round(4 * pi * r_gl ** 3 / 3, 2) + v_ls
            print('-----%.2f%%-----' % (v_ls * 100 / V_max))

print('dgl_num:', len(list_dgl))
print('dgl_completed!')

#中骨料
list_zgl=[]
v_ls=0
V_ls=round(pi*gl_sec**3/6,2)

while V_mid-v_ls >=V_ls:
    x_gl=round(random.uniform(-0.5*chang+0.5*gl_sec,0.5*chang-0.5*gl_sec),2)
    y_gl=round(random.uniform(-0.5*kuan+0.5*gl_sec,0.5*kuan-0.5*gl_sec),2)
    z_gl=round(random.uniform(0.5*gl_sec,gao-0.5*gl_sec),2)

    r_gl=round(random.uniform(0.5*gl_thr,0.5*gl_sec),2)

    m0=0
    m1=len(list_qiu)
    while m0 < m1 :
        x1=list_qiu[m0][0]
        y1=list_qiu[m0][1]
        z1=list_qiu[m0][2]
        r1=list_qiu[m0][3]
        qq=((x_gl-x1)**2+(y_gl-y1)**2+(z_gl-z1)**2)**0.5
        if qq < r1+r_gl:
            break
        m0+=1
    else:
        list_qiu.append([x_gl,y_gl,z_gl,r_gl])
        list_zgl.append([x_gl,y_gl,z_gl,r_gl])
        v_ls=round(4*pi*r_gl**3/3,2)+v_ls
        print('-----%.2f%%-----' % (v_ls * 100 / V_mid))
print('zgl_num:', len(list_zgl))
print('zgl_completed!')

#小骨料
list_xgl=[]
v_ls=0
xh=0
V_ls=round(pi*gl_thr**3/6,2)

while V_min - v_ls >= V_ls and xh <xh_max:
    x_gl=round(random.uniform(-0.5*chang+0.5*gl_thr,0.5*chang-0.5*gl_thr),2)
    y_gl=round(random.uniform(-0.5*kuan+0.5*gl_thr,0.5*kuan-0.5*gl_thr),2)
    z_gl=round(random.uniform(0.5*gl_thr,gao-0.5*gl_thr),2)

    r_gl=round(random.uniform(0.5*gl_min,0.5*gl_thr),2)

    xh=xh+1
    m0=0
    m1=len(list_qiu)
    while m0 < m1 :
        x1=list_qiu[m0][0]
        y1=list_qiu[m0][1]
        z1=list_qiu[m0][2]
        r1=list_qiu[m0][3]
        qq=((x_gl-x1)**2+(y_gl-y1)**2+(z_gl-z1)**2)**0.5
        if qq < r1+r_gl:
            break
        m0+=1
    else:
        list_qiu.append([x_gl,y_gl,z_gl,r_gl])
        list_xgl.append([x_gl,y_gl,z_gl,r_gl])
        v_ls=round(4*3.14*r_gl**3/3,2)+v_ls
        print('-----%.2f%%-----' % (v_ls * 100 / V_min))
print('xgl_num:', len(list_xgl))
print('xgl_completed!')

#生成实体
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',sheetSize=200.0)
s.rectangle(point1=(-0.5*chang, -0.5*kuan), point2=(0.5*chang, 0.5*kuan))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D,type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=gao)
del mdb.models['Model-1'].sketches['__profile__']
p.seedPart(size=buzhong, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

#设置set
p = mdb.models['Model-1'].parts['Part-1']
m=p.elements

for i in range(len(list_dgl)):
    x1 = list_dgl[i][0]
    y1 = list_dgl[i][1]
    z1 = list_dgl[i][2]
    r1 = list_dgl[i][3]
    if i==0:
        dgl=m.getByBoundingSphere(center=(x1,y1,z1),radius=r1)
    else:
        dgl=m.getByBoundingSphere(center=(x1,y1,z1),radius=r1)+dgl

for i in range(len(list_zgl)):
    x1 = list_zgl[i][0]
    y1 = list_zgl[i][1]
    z1 = list_zgl[i][2]
    r1 = list_zgl[i][3]
    if i==0:
        zgl=m.getByBoundingSphere(center=(x1,y1,z1),radius=r1)
    else:
        zgl=m.getByBoundingSphere(center=(x1,y1,z1),radius=r1)+zgl

if len(list_xgl)!=0:
    for i in range(len(list_xgl)):
        x1 = list_xgl[i][0]
        y1 = list_xgl[i][1]
        z1 = list_xgl[i][2]
        r1 = list_xgl[i][3]
        if i==0:
            xgl=m.getByBoundingSphere(center=(x1,y1,z1),radius=r1)
        else:
            xgl=m.getByBoundingSphere(center=(x1,y1,z1),radius=r1)+xgl

p.Set(elements=dgl,name='daguliao')
p.Set(elements=zgl,name='zhongguliao')
if len(xgl)!=0:
    p.Set(elements=xgl,name='xiaoguliao')

#设置砂浆set
all_elements=len(p.elements)
list_bh=list(range(1,all_elements+1))

dgl=p.sets['daguliao']
zgl=p.sets['zhongguliao']
xgl=p.sets['xiaoguliao']

for i in range(len(dgl.elements)):
    label1=dgl.elements[i].label
    list_bh.remove(label1)

for i in range(len(zgl.elements)):
    label2 = zgl.elements[i].label
    list_bh.remove(label2)

for i in range(len(xgl.elements)):
    label3 = xgl.elements[i].label
    list_bh.remove(label3)

set_sj=[]
for ii in range(len(list_bh)):
    rr=list_bh[ii]
    set_sj.append(p.elements[rr-1:rr])

p.Set(elements=set_sj,name='shajiang')
print('done!')





