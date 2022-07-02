# encoding=utf-8
from abaqus import *
from abaqusConstants import *
import random
import math


fields=(('Please input basic length(mm):','100'),  #0
        ('Please input basic width(mm):','100'),  #1
        ('Please input basic height(mm):','100'),  #2
        ('Please input the ratio of b(long axis) to a(short axis):','1.42'),  # 3  banjing
        ('Please input the aggregate volume ratio (between 0-1):','0.4'),  #4
        ('Please enter the maximum aggregate size:','20'),  #5
        ('Please enter the second aggregate size:','15'),  #6
        ('Please enter the third aggregate size:','10'),  #7
        ('Please input the minimum size of aggregate:','5'),  #8
        ('Please enter the volume ratio of the maximum aggregate(between 0-1);','0.25'),  #9
        ('Please enter the volume ratio of the minimum aggregate (between 0-1):','0.5'),  #10
        ('Please enter the maximum number of cycles (integer):','800000'))#11
modelparam=getInputs(fields=fields,label='Generation of three graded random ellipsoidal aggregate:')

length=float(modelparam[0])
width=float(modelparam[1])
height=float(modelparam[2])

max_ratio=float(modelparam[3])

V_gl=length*width*height*float(modelparam[4])

gl_max=float(modelparam[5])
gl_sec=float(modelparam[6])
gl_thr=float(modelparam[7])
gl_min=float(modelparam[8])

V_max=V_gl*float(modelparam[9])
V_min=V_gl*float(modelparam[10])
V_mid=V_gl-V_max-V_min

count_num=float(modelparam[11])

print(V_max,V_mid,V_min)

#check
def intercheck(point,center):
    for p in center:
        if sqrt((p[0]-point[0])**2+(p[1]-point[1])**2+(p[2]-point[2])**2)<=point[4]+p[4]:
            sign=False
            break
        else:
            sign=True
    return sign

ratio = max_ratio
all_yuan=[]

#大椭球骨料
dgl_param=[]
V_already=0
V_zuixiaogl=round(4*math.pi*(0.5*gl_sec/max_ratio)*(0.5*gl_sec)*(0.5*gl_sec/max_ratio)/3,2)

while V_max - V_already >= V_zuixiaogl:
    r_gl=round(random.uniform(0.5*gl_sec,0.5*gl_max), 2)
    x_gl=round(random.uniform(-0.5*length+r_gl,0.5*length-r_gl),2)
    y_gl=round(random.uniform(-0.5*width+r_gl,0.5*width-r_gl),2)
    z_gl=round(random.uniform(r_gl,height-r_gl),2)

    duan_axis=round(r_gl/ratio,2)

    point=[x_gl,y_gl,z_gl,duan_axis,r_gl]
    if len(all_yuan):
        if intercheck(point,all_yuan):
            all_yuan.append(point)
            dgl_param.append(point)
            V_already=V_already+round(4*math.pi*duan_axis*r_gl*duan_axis/3,2)
            print('-----%.2f%%-----' % (V_already * 100 / V_max))
    else:
        all_yuan.append(point)
        dgl_param.append(point)
        V_already = V_already + round(4 * math.pi * duan_axis * r_gl * duan_axis / 3, 2)
        print('-----%.2f%%-----' % (V_already * 100 / V_max))

print('dgl_num:',len(dgl_param))
print('1_completed!')

#中椭球骨料
zgl_param=[]
V_already=0
V_zuixiaogl=round(4*math.pi*(0.5*gl_thr/max_ratio)*(0.5*gl_thr)*(0.5*gl_thr/max_ratio)/3,2)

while V_mid - V_already >= V_zuixiaogl:
    r_gl=round(random.uniform(0.5*gl_thr,0.5*gl_sec), 2)
    x_gl=round(random.uniform(-0.5*length+r_gl,0.5*length-r_gl),2)
    y_gl=round(random.uniform(-0.5*width+r_gl,0.5*width-r_gl),2)
    z_gl=round(random.uniform(r_gl,height-r_gl),2)

    duan_axis=round(r_gl/ratio,2)
    point=[x_gl,y_gl,z_gl,duan_axis,r_gl]

    if intercheck(point,all_yuan):
        all_yuan.append(point)
        zgl_param.append(point)
        V_already=V_already+round(4*math.pi*duan_axis*r_gl*duan_axis/3,2)
        print('-----%.2f%%-----' % (V_already * 100 / V_mid))

print('zgl_num:',len(zgl_param))
print('2_completed!')

#小椭球骨料
count=0
xgl_param=[]
V_already=0
V_zuixiaogl=round(4*math.pi*(0.5*gl_min/max_ratio)*(0.5*gl_min)*(0.5*gl_min/max_ratio)/3,2)

while V_min - V_already >= V_zuixiaogl:
    r_gl=round(random.uniform(0.5*gl_min,0.5*gl_thr), 2)
    x_gl=round(random.uniform(-0.5*length+r_gl,0.5*length-r_gl),2)
    y_gl=round(random.uniform(-0.5*width+r_gl,0.5*width-r_gl),2)
    z_gl=round(random.uniform(r_gl,height-r_gl),2)

    duan_axis=round(r_gl/ratio,2)
    point=[x_gl,y_gl,z_gl,duan_axis,r_gl]

    if intercheck(point,all_yuan):
        all_yuan.append(point)
        xgl_param.append(point)
        V_already=V_already+round(4*math.pi*duan_axis*r_gl*duan_axis/3,2)
        print('-----%.2f%%-----' % (V_already * 100 / V_min))

    count+=1
    if count>count_num:
        break

print('xgl_num:',len(xgl_param))
print('3_completed!')

dgl_instances=[]
zgl_instances=[]
xgl_instances=[]

a = mdb.models['Model-1'].rootAssembly
for i in range(len(all_yuan)):
    myModel = mdb.models['Model-1']
    partName = "part-{}".format(i+1)
    mysketch_1 = myModel.ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mysketch_1.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    curve = mysketch_1.EllipseByCenterPerimeter(center=(0.0, 0.0), axisPoint1=(all_yuan[i][3],0.0),axisPoint2=(0, all_yuan[i][4]))
    mysketch_1.autoTrimCurve(curve1=curve, point1=(-100,0.1))
    mysketch_1.Line(point1=(0, all_yuan[i][4]), point2=(0, -all_yuan[i][4]))
    myPart1 = myModel.Part(name=partName, dimensionality=THREE_D, type=DEFORMABLE_BODY)
    myPart1.BaseSolidRevolve(sketch=mysketch_1, angle=360.0, flipRevolveDirection=OFF)

    a.Instance(name='part-{}-1'.format(i+1), part=mdb.models['Model-1'].parts['part-{}'.format(i+1)], dependent=ON)
    a.rotate(instanceList=('part-{}-1'.format(i+1),),
             axisPoint=(0, 0, 0),
             axisDirection=(random.uniform(-0.5*length, 0.5*length), random.uniform(-0.5*width, 0.5*width), random.uniform(-0.5*height, 0.5*height)),
             angle=random.uniform(30, 180))
    a.translate(instanceList=('part-{}-1'.format(i+1),), vector=(all_yuan[i][0], all_yuan[i][1],all_yuan[i][2]))

    if i<len(dgl_param):
        instance=a.instances['part-{}-1'.format(i+1)]
        dgl_instances.append(instance)
    elif len(dgl_param)-1<i<len(dgl_param+zgl_param):
        instance = a.instances['part-{}-1'.format(i+1)]
        zgl_instances.append(instance)
    elif i>len(dgl_param+zgl_param)-1:
        instance = a.instances['part-{}-1'.format(i+1)]
        xgl_instances.append(instance)

a.InstanceFromBooleanMerge(name='Part-dgl', instances=tuple(dgl_instances), originalInstances=SUPPRESS, domain=GEOMETRY)
a.InstanceFromBooleanMerge(name='Part-zgl', instances=tuple(zgl_instances), originalInstances=SUPPRESS, domain=GEOMETRY)
a.InstanceFromBooleanMerge(name='Part-xgl', instances=tuple(xgl_instances), originalInstances=SUPPRESS, domain=GEOMETRY)

for i in range(len(all_yuan)):
    del mdb.models['Model-1'].parts['part-{}'.format(i + 1)]
    del a.features['part-{}-1'.format(i + 1)]
print('done！')