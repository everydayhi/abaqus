# encoding=utf-8
from abaqus import *
from abaqusConstants import *
from scipy.spatial import *
import numpy as np
import random
import mesh
import regionToolset


#initial variables
fields = (('Model Name:', 'Model-1'), ('Point Number:', '200'), ('Length:', '100'),
          ('Width:', '100'), ('Height:', '100'), ('Seed Size:', '2.5'))
name, point_number, length, width, height, seedsize = getInputs(fields=fields, label='Creat Voronoi')
point_number = int(point_number)
length = float(length)
width = float(width)
seedsize = float(seedsize)


#rve size
size = float(height)
# extend size
ex = 5

#create Voronoi
points = np.array([[random.uniform(0,length*ex),random.uniform(0,width*ex),random.uniform(0,size*ex)] for i in range(point_number)])
vor = Voronoi(points)
#get attributes
vertices = vor.vertices
edges = vor.ridge_vertices

for edge in edges:
    for number in edge:
        if number !=-1 :
            for coord in vertices[number]:
                if coord >= max(length, width, size) * ex or coord <= 0:
                    edges[edges.index(edge)].append(-1)
                    break

face_points = []
for edge in np.array(edges):
    edge = np.array(edge)
    temp = []
    if np.all(edge >= 0):
            for i in edge:
                temp.append(tuple(vertices[i]))
            temp.append(vertices[edge[0]])
    if (len(temp)>0):
        face_points.append(temp)

# create voronoi
myModel = mdb.models['Model-1']
myPart = myModel.Part(name='Part-vor3', dimensionality=THREE_D, type=DEFORMABLE_BODY)

for i in range(len(face_points)):
    wire = myPart.WirePolyLine(mergeType=SEPARATE, meshable=ON, points=(face_points[i]))
    face_edge = myPart.getFeatureEdges(name=wire.name)
    myPart.CoverEdges(edgeList = face_edge, tryAnalytical=True)

faces = myPart.faces[:]
myPart.AddCells(faceList = faces)

# cut Voronoi
#create core
myPart2 = myModel.Part(name='Part-core', dimensionality=THREE_D, type=DEFORMABLE_BODY)
mySketch2 = myModel.ConstrainedSketch(name="mysketch-2",sheetSize = 200)
mySketch2.rectangle(point1=(0,0), point2=(length,width))
myPart2.BaseSolidExtrude(sketch=mySketch2, depth=size)

#create base
myPart3 = myModel.Part(name='Part-base', dimensionality=THREE_D, type=DEFORMABLE_BODY)
mySketch3 = myModel.ConstrainedSketch(name='__profile__', sheetSize=200.0)
mySketch3.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
curve = mySketch3.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(size*10,0.0))
mySketch3.Line(point1=(0.0, 10*size), point2=(0.0, -10*size))
mySketch3.autoTrimCurve(curve1=curve, point1=(-size*10,0.0))
myPart3.BaseSolidRevolve(sketch=mySketch3, angle=360.0, flipRevolveDirection=OFF)

# instance
myAssembly = myModel.rootAssembly
myAssembly.Instance(name='Part-base-1', part=myModel.parts["Part-base"], dependent=ON)
myAssembly.Instance(name='Part-core-1', part=myModel.parts["Part-core"], dependent=ON)
myAssembly.translate(instanceList=('Part-core-1', ), vector=((ex-1)*length/2,(ex-1)*width/2,(ex-1)*size/2))
myAssembly.InstanceFromBooleanCut(name='Part-base-cut',instanceToBeCut=myAssembly.instances['Part-base-1'],
                                  cuttingInstances=(myAssembly.instances['Part-core-1'], ), originalInstances=DELETE)
# cut voronoi
myAssembly.Instance(name='Part-cut-1', part=myModel.parts["Part-base-cut"], dependent=ON)
myAssembly.Instance(name='Part-vor3-1', part=myModel.parts["Part-vor3"], dependent=ON)
myAssembly.InstanceFromBooleanCut(name='Part-voronoi',instanceToBeCut=myAssembly.instances['Part-vor3-1'],
                                  cuttingInstances=(myAssembly.instances['Part-cut-1'], ), originalInstances=DELETE)

#create analys
myPart_analys = myModel.Part(name='Part-analys', dimensionality=THREE_D, type=DEFORMABLE_BODY)
mySketch4 = myModel.ConstrainedSketch(name="mysketch-4",sheetSize = 200)
mySketch4.rectangle(point1=(0,0), point2=(length,width))
myPart_analys.BaseSolidExtrude(sketch=mySketch4, depth=size)
myPart_analys.seedPart(size=seedsize , deviationFactor=0.1, minSizeFactor=0.1)
myPart_analys.generateMesh()

myPart_vor3_cut = myModel.parts['Part-voronoi']
myCells = myPart_vor3_cut.cells

myNodes = myPart_analys.nodes
myElement = myPart_analys.elements

# create cell_element
element_number = []
for i in range(len(myCells)):
    element_number.append([])

for element in myElement:
    points = []
    for index in element.connectivity:
        points.append(list(myNodes[index].coordinates))
    junzhi = np.array(points).mean(axis=0)
    center = junzhi.astype('float64')+np.array([(ex-1)*length/2,(ex-1)*width/2,(ex-1)*size/2]).astype('float64')#two different locations for two cubes
    index1 = myCells.findAt(center).index
    for i in range(len(myCells)):
        if index1 == i:
            element_number[i].append(element.label-1)

# create cell_element set
ii=0
for set_element in element_number:
    #print(set_element[0])
    if len(set_element):
        ii+=1
        element = myElement[set_element[0]:set_element[0]+1]
        for i in range(1, len(set_element)):
            element += myElement[set_element[i]:set_element[i]+1]
        region = myPart_analys.Set(elements=element, name="Set-{}".format(ii))

for key in myAssembly.instances.keys():
    del myAssembly.instances[key]
for key in myModel.parts.keys():
    if key != "Part-analys":
        if key != "Part-voronoi":
            del myModel.parts[key]

s=myPart_analys.sets
elements=myPart_analys.elements
elementFaces=myPart_analys.elementFaces

# 遍历set
if len(s)!=0:
    set_ele_labels=[]
    for key in s.keys():
        temp=[]
        for set_ele in s['{}'.format(key)].elements:
            temp.append(set_ele.label)
        set_ele_labels.append(temp)

    #遍历每个单元每个面
    FacesLabel = [[], [], [], [], [], []]
    for elementFace in elementFaces:
        label1=[]
        two_element = elementFace.getElements()
        if len(two_element)==2:
            for i in range(len(two_element)):
                label1.append(two_element[i].label)
            x = 0
            for i in range(len(set_ele_labels)):
                if set(label1) < set(set_ele_labels[i]):#如果getElements得到的两个单元都在一个set里面
                    break
                x += 1
            if x == len(set_ele_labels):#两个单元不在一起
                if elementFace.face == FACE1:
                    FacesLabel[0].append(elementFace.label)
                elif elementFace.face == FACE2:
                    FacesLabel[1].append(elementFace.label)
                elif elementFace.face == FACE3:
                    FacesLabel[2].append(elementFace.label)
                elif elementFace.face == FACE4:
                    FacesLabel[3].append(elementFace.label)
                elif elementFace.face == FACE5:
                    FacesLabel[4].append(elementFace.label)
                else:
                    FacesLabel[5].append(elementFace.label)

    #把单元面label转换为element
    faceElements = [[], [], [], [], [], []]
    for i in range(6):
        if len(FacesLabel[i]):
            for ii in range(len(FacesLabel[i])):
                faceElements[i].append(elements[FacesLabel[i][ii] - 1])
            faceElements[i] = mesh.MeshElementArray(elements=faceElements[i])

    myPart_analys.Surface(face1Elements=faceElements[0], face2Elements=faceElements[1],
        face3Elements=faceElements[2], face4Elements=faceElements[3],
        face5Elements=faceElements[4], face6Elements=faceElements[5], name='Surf-1')

    myPart_analys.PartFromMesh(name='Part-analys-mesh-1', copySets=True)