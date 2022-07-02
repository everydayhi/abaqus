# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2020 replay file
# Internal Version: 2019_09_14-01.49.31 163176
# Run by PC on Sat Apr 17 20:59:21 2021
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
import random

fields=(('Please input beam length(mm):','240'),#0
        ('Please input beam width(mm):','35'),#1
        ('Size of seed (integer):','1'),#2
        ('Please input the aggregate volume ratio (between 0-1):','0.8'),#3
        ('PPlease enter the maximum aggregate size:','16'),#4
        ('Please enter the second aggregate size:','10'),#5
        ('Please enter the third aggregate size:','5'),#6
        ('Please input the minimum size of aggregate:','3'),#7
        ('Please enter the volume ratio of the maximum aggregate(between 0-1);','0.3'), #8
        ('Please enter the volume ratio of the minimum aggregate (between 0-1):','0.4'),#9
        ('Please enter the maximum number of cycles (integer):','100000'))

list_all_inf=getInputs(fields=fields,label='Generation of three graded random aggregate:')

chang=float(list_all_inf[0])
kuan=float(list_all_inf[1])
buzhong=float(list_all_inf[2])


session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=119.14582824707,
    height=119.902778625488)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
cliCommand("""session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry= COORDINATE)""")

s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
    sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(point1=(-0.5*chang, -0.5*kuan), point2=(0.5*chang, 0.5*kuan))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=TWO_D_PLANAR,
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
p = mdb.models['Model-1'].parts['Part-1']
p.seedPart(size=buzhong, deviationFactor=0.1, minSizeFactor=0.1)
p.generateMesh()

S_gl=chang*kuan*float(list_all_inf[3])
S_max=S_gl*float(list_all_inf[8])
S_min=S_gl*float(list_all_inf[9])
S_mid=S_gl-S_max-S_min

print('S_max:'+str(S_max))
print('S_mid:'+str(S_mid))
print('S_min:'+str(S_min))

gl_max=float(list_all_inf[4])
gl_sec=float(list_all_inf[5])
gl_thr=float(list_all_inf[6])
gl_min=float(list_all_inf[7])



list_yuan=[]
list_dgl=[]

s_ls=0
S_ls=round(3.14*gl_sec**2/4,2)

while S_max-s_ls >= S_ls:
    if len(list_yuan) == 0:
        x_gl=round(random.uniform(-0.5*chang+0.5*gl_max,0.5*chang-0.5*gl_max),2)
        y_gl=round(random.uniform(-0.5*kuan+0.5*gl_max,0.5*kuan-0.5*gl_max),2)
        r_gl=round(random.uniform(0.5*gl_sec,0.5*gl_max),2)
        s_ls=3.14*r_gl**2+s_ls
        list_yuan.append([x_gl,y_gl,r_gl])
        list_dgl.append([x_gl,y_gl,r_gl])
    else:
        x_gl=round(random.uniform(-0.5*chang+0.5*gl_max,0.5*chang-0.5*gl_max),2)
        y_gl=round(random.uniform(-0.5*kuan+0.5*gl_max,0.5*kuan-0.5*gl_max),2)
        r_gl=round(random.uniform(0.5*gl_sec,0.5*gl_max),2)
        m0=0
        m1=len(list_yuan)
        while m0 < m1 :
            x1=list_yuan[m0][0]
            y1=list_yuan[m0][1]
            r1=list_yuan[m0][2]
            qq=((x_gl-x1)**2+(y_gl-y1)**2)**0.5
            if qq < r1+r_gl:
                break
            m0=m0+1
        else:
            s_ls=3.14*r_gl**2+s_ls
            list_yuan.append([x_gl,y_gl,r_gl])
            list_dgl.append([x_gl,y_gl,r_gl])

print('1')

list_zgl=[]

s_ls=0
S_ls=round(3.14*gl_thr**2/4,2)

while S_mid - s_ls >= S_ls:
    x_gl=round(random.uniform(-0.5*chang+0.5*gl_sec,0.5*chang-0.5*gl_sec),2)
    y_gl=round(random.uniform(-0.5*kuan+0.5*gl_sec,0.5*kuan-0.5*gl_sec),2)
    r_gl=round(random.uniform(0.5*gl_thr,0.5*gl_sec),2)
    m0=0
    m1=len(list_yuan)
    while m0 < m1 :
        x1=list_yuan[m0][0]
        y1=list_yuan[m0][1]
        r1=list_yuan[m0][2]
        qq=((x_gl-x1)**2+(y_gl-y1)**2)**0.5
        if qq < r1+r_gl:
            break
        m0=m0+1
    else:
        s_ls=3.14*r_gl**2+s_ls
        list_yuan.append([x_gl,y_gl,r_gl])
        list_zgl.append([x_gl,y_gl,r_gl])

print('2')

list_xgl=[]

s_ls=0
S_ls=round(3.14*gl_min**2/4,2)
xh=0
xh_max=float(list_all_inf[10])

while S_min - s_ls >= S_ls and xh < xh_max:
    x_gl=round(random.uniform(-0.5*chang+0.5*gl_thr,0.5*chang-0.5*gl_thr),2)
    y_gl=round(random.uniform(-0.5*kuan+0.5*gl_thr,0.5*kuan-0.5*gl_thr),2)
    r_gl=round(random.uniform(0.5*gl_min,0.5*gl_thr),2)
    xh=xh+1
    m0=0
    m1=len(list_yuan)
    while m0 < m1 :
        x1=list_yuan[m0][0]
        y1=list_yuan[m0][1]
        r1=list_yuan[m0][2]
        qq=((x_gl-x1)**2+(y_gl-y1)**2)**0.5
        if qq < r1+ r_gl:
            break
        m0=m0+1
    else:
        s_ls=3.14*r_gl**2+s_ls
        list_yuan.append([x_gl,y_gl,r_gl])
        list_xgl.append([x_gl,y_gl,r_gl])

print('3')


p = mdb.models['Model-1'].parts['Part-1']
m=p.elements



for i in range(len(list_dgl)):
    if i==0:
        x1=list_dgl[i][0]
        y1=list_dgl[i][1]
        r1=list_dgl[i][2]
        dgl=m.getByBoundingSphere(center=(x1,y1,0),radius=r1)
    else:
        x1=list_dgl[i][0]
        y1=list_dgl[i][1]
        r1=list_dgl[i][2]
        dgl=m.getByBoundingSphere(center=(x1,y1,0),radius=r1)+dgl


for i in range(len(list_zgl)):
    if i==0:
        x1=list_zgl[i][0]
        y1=list_zgl[i][1]
        r1=list_zgl[i][2]
        zgl=m.getByBoundingSphere(center=(x1,y1,0),radius=r1)
    else:
        x1=list_zgl[i][0]
        y1=list_zgl[i][1]
        r1=list_zgl[i][2]
        zgl=m.getByBoundingSphere(center=(x1,y1,0),radius=r1)+zgl

if len(list_xgl)!=0:
    for i in range(len(list_xgl)):
        if i==0:
            x1=list_xgl[i][0]
            y1=list_xgl[i][1]
            r1=list_xgl[i][2]
            xgl=m.getByBoundingSphere(center=(x1,y1,0),radius=r1)
        else:
            x1=list_xgl[i][0]
            y1=list_xgl[i][1]
            r1=list_xgl[i][2]
            xgl=m.getByBoundingSphere(center=(x1,y1,0),radius=r1)+xgl

p.Set(elements=dgl,name='daguliao')
p.Set(elements=zgl,name='zhongguliao')
if len(xgl)!=0:
    p.Set(elements=xgl,name='xiaoguliao')


all_elements=len(p.elements)
list_bh=list(range(1,all_elements+1))

dgl=p.sets['daguliao']

for i in range(len(dgl.elements)):
    label=dgl.elements[i].label
    list_bh.remove(label)

zgl=p.sets['zhongguliao']

for i in range(len(zgl.elements)):
    label=zgl.elements[i].label
    list_bh.remove(label)

xgl=p.sets['xiaoguliao']

for i in range(len(xgl.elements)):
    label=xgl.elements[i].label
    list_bh.remove(label)

set_lq=[]
for ii in range(len(list_bh)):
    rr=list_bh[ii]
    set_lq.append(p.elements[rr-1:rr])


p.Set(elements=set_lq,name='Set-liqing')

print('done')











