# encoding=utf-8
import random
from abaqus import *
from abaqusConstants import *
import numpy as np
import math
import itertools
from numpy import pi,sin,cos,arccos

fields=(('Please input basic length(mm):','100'),  #0
        ('Please input basic width(mm):','100'),  #1
        ('Please input basic height(mm):','100'),  #2
        ('Please input the number of vertices of the polygon:','25'),  # 3
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

agg_vertice_Number=float(modelparam[3])

V_gl=length*width*height*float(modelparam[4])

gl_max=float(modelparam[5])
gl_sec=float(modelparam[6])
gl_thr=float(modelparam[7])
gl_min=float(modelparam[8])

V_max=V_gl*float(modelparam[9])
V_min=V_gl*float(modelparam[10])
V_mid=V_gl-V_max-V_min

print(V_max,V_mid,V_min)
count_num=float(modelparam[11])

#判断球是否相交
def intercheck(points,center):
    sign = True
    for point in points:
        if sqrt((point[0]-center[0])**2 + (point[1]-center[1])**2 + (point[2]-center[2])**2) < (center[3]+point[3]):
            sign=False
            break
    return sign

# 判断顶点间距是否过小
def verticesCheck(vertice, vertices,radius):
    sign = True
    if radius<5:
        d =1
    elif 5<radius<7.5:
        d = 2
    elif 7.5<radius < 10:
        d = 4
    for v in vertices:
        x1, y1, z1 = v[0], v[1], v[2]
        x2, y2, z2 = vertice[0], vertice[1], vertice[2]
        distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
        if distance < d:
            sign = False
            break
    return sign

# 方向向量计算
def directN(coords):
    coord1, coord2, coord3 = coords[0],coords[1],coords[2]
    x1, y1, z1 = coord1[0], coord1[1], coord1[2]
    x2, y2, z2 = coord2[0], coord2[1], coord2[2]
    x3, y3, z3 = coord3[0], coord3[1], coord3[2]
    #向量叉乘求法向量
    a = (y2-y1)*(z3-z1) - (y3-y1)*(z2-z1)
    b = (z2-z1)*(x3-x1) - (z3-z1)*(x2-x1)
    c = (x2-x1)*(y3-y1) - (x3-x1)*(y2-y1)
    n = np.array([a, b, c])
    #二范数，求单位向量，模为1
    n = n/np.linalg.norm(n)
    #点积，求向量coord1与法线向量的夹角
    d = arccos(np.dot(n, coord1)/np.linalg.norm(coord1))
    if d>pi/2.:
        n = -n#保证法线必须指向外侧
    return n

# 平面判断
def chosenPlane(vertices):
    vertices = [np.array(vertice) for vertice in vertices]
    threePoints = list(itertools.combinations(vertices, 3))
    chosenPlane = []
    for threePoint in threePoints:
        n = directN(threePoint)
        sign = True
        for vertice in vertices:
            #点在面的一侧，并在内侧
            vector1 = threePoint[0]-vertice
            #点在内测，与外法线的夹角必小于90度
            result = np.dot(vector1, n)
            if result<-1e-10:
                sign = False
                break
        if sign:
            chosenPlane.append(list(threePoint))
    return chosenPlane

all_centers = []
#大骨料
count=0
dgl_centers = []

V_already=0
V_zuixiaogl=round(4*pi*(0.5*gl_sec)**3/3,2)

while V_max - V_already >= V_zuixiaogl:
    radius = random.uniform(0.5*gl_sec,0.5*gl_max)
    x=random.uniform(radius,length-radius)
    y=random.uniform(radius,width-radius)
    z=random.uniform(radius,height-radius)

    center = [x,y,z,radius]
    if len(all_centers):
        if intercheck(all_centers, center):
            all_centers.append(center)
            dgl_centers.append(center)
            V_already = V_already + round(4 * pi * radius **3/ 3, 2)
            print('-----%.2f%%-----' % (V_already*100/V_max))

    else:
        all_centers.append(center)
        dgl_centers.append(center)

        V_already=V_already+round(4*pi*radius**3/3,2)
        print('-----%.2f%%-----' % (V_already*100/V_max))
print('dgl_num:',len(dgl_centers))
print('dgl_completed!')

# 中骨料
zgl_centers = []

V_already = 0
V_zuixiaogl = round(4*pi*(0.5*gl_thr)**3/3,2)

while V_mid - V_already >= V_zuixiaogl:
    radius = random.uniform(gl_thr*0.5, gl_sec*0.5)
    x = random.uniform(radius, length - radius)
    y = random.uniform(radius, width - radius)
    z = random.uniform(radius, height - radius)

    center = [x, y, z, radius]
    if len(all_centers):
        if intercheck(all_centers, center):
            all_centers.append(center)
            zgl_centers.append(center)
            V_already = V_already + round(4 * pi * radius**3/ 3, 2)
            print('-----%.2f%%-----' % (V_already*100/V_mid))

    else:
        all_centers.append(center)
        zgl_centers.append(center)

        V_already = V_already + round(4 * pi *radius**3 / 3, 2)
        print('-----%.2f%%-----' % (V_already*100/V_mid))
print('zgl_num:',len(zgl_centers))
print('zgl_completed!')

# 小骨料
count=0
xgl_centers = []

V_already = 0
V_zuixiaogl = round(4*pi*(0.5*gl_min)**3/3,2)

while V_min - V_already >= V_zuixiaogl:
    radius = random.uniform(gl_min*0.5, gl_thr*0.5)
    x = random.uniform(radius, length - radius)
    y = random.uniform(radius, width - radius)
    z = random.uniform(radius, height - radius)

    center = [x, y, z, radius]
    if len(all_centers):
        if intercheck(all_centers, center):
            all_centers.append(center)
            xgl_centers.append(center)
            V_already = V_already + round(4 * pi * radius**3/ 3, 2)
            print('-----%.2f%%-----' % (V_already*100/V_min))

    else:
        all_centers.append(center)
        xgl_centers.append(center)

        V_already = V_already + round(4 * pi * radius**3 / 3, 2)
        print('-----%.2f%%-----' % (V_already*100/V_min))

    count+=1
    if count>count_num:
        break
print('xgl_num:',len(xgl_centers))
print('xgl_completed!')

#生成随机顶点
#局部变量
for i in  range(len(all_centers)):
    vertices = []
    while len(vertices)< agg_vertice_Number:
        radius=all_centers[i][3]

        angle1 = np.random.uniform(0, pi)
        angle2 = np.random.uniform(0, pi * 2)

        # 随机生成顶点坐标 x,y,z
        x1 =radius* sin(angle1) * cos(angle2)
        y1 =radius* sin(angle1) * sin(angle2)
        z1 =radius* cos(angle1)

        if len(vertices):
            if verticesCheck([x1, y1, z1], vertices,radius):
                vertices.append([x1, y1, z1])
        else:
            vertices.append([x1, y1, z1])

    all_centers[i].append(vertices)

if mdb.models.has_key("Model-test"):
    del mdb.models["Model-test"]
model = mdb.Model(name="Model-test", modelType=STANDARD_EXPLICIT)

#生成骨料
for i in range(len(all_centers)):
    myPart = model.Part(name="part-test-{}".format(i), dimensionality=THREE_D, type=DEFORMABLE_BODY)
    chosePlane = chosenPlane(all_centers[i][4])  # 调用骨料平面判断的函数

    # create point
    '''for vertice1 in all_centers[i][4]:
        myPart.DatumPointByCoordinate(coords=tuple(vertice1))'''

    # create plane
    for coords in chosePlane:
        coords.append(coords[0])#构成封闭坐标
        wire = myPart.WirePolyLine(mergeType=SEPARATE, meshable=ON, points=(coords))
        face_edge = myPart.getFeatureEdges(name=wire.name)
        myPart.CoverEdges(edgeList=face_edge, tryAnalytical=True)

    # shell to solid
    faces = myPart.faces[:]
    myPart.AddCells(faceList=faces)

# 生成实体
dgl_instances=[]
zgl_instances=[]
xgl_instances=[]

assembly = model.rootAssembly
for i in range(len(all_centers)):
    part = model.parts["part-test-{}".format(i)]
    instanceName = 'instance-test-{}'.format(i)
    instance=assembly.Instance(name=instanceName, part=part, dependent=ON)
    assembly.translate(instanceList=(instanceName, ), vector=tuple((all_centers[i][0],all_centers[i][1],all_centers[i][2])))

    if i<len(dgl_centers):
        dgl_instances.append(instance)
    elif len(dgl_centers)-1<i<len(dgl_centers+zgl_centers):
        zgl_instances.append(instance)
    elif i>len(dgl_centers+zgl_centers)-1:
        xgl_instances.append(instance)

assembly.InstanceFromBooleanMerge(name='Part-dgl', instances=tuple(dgl_instances), originalInstances=SUPPRESS, domain=GEOMETRY)
assembly.InstanceFromBooleanMerge(name='Part-zgl', instances=tuple(zgl_instances), originalInstances=SUPPRESS, domain=GEOMETRY)
assembly.InstanceFromBooleanMerge(name='Part-xgl', instances=tuple(xgl_instances), originalInstances=SUPPRESS, domain=GEOMETRY)

for i in range(len(all_centers)):
    del mdb.models['Model-test'].parts['part-test-{}'.format(i)]
    del assembly.features['instance-test-{}'.format(i)]
print('done!')
