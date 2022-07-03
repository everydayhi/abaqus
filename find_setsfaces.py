# encoding=utf-8
from abaqus import *
from abaqusConstants import *
from scipy.spatial import *
import numpy as np
import random
import mesh
import regionToolset

ff = (('ModelName:', 'Model-1'), ('partName:', "Part-analys" ))
modelName,partBaseName= getInputs(fields=ff, label='Creat a shared surface set')

m = mdb.models[modelName]
p1= m.parts[partBaseName]

s=p1.sets
myElement = p1.elements
elementFaces=p1.elementFaces

# 遍历set
if len(s)!=0:
    set_ele_labels=[]
    for key in s.keys():
        temp=[]
        for set_ele in s['{}'.format(key)].elements:
            temp.append(set_ele.label)
        set_ele_labels.append(temp)
    print(set_ele_labels)

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
                faceElements[i].append(myElement[FacesLabel[i][ii] - 1])
            print(faceElements)
            faceElements[i] = mesh.MeshElementArray(elements=faceElements[i])

    #creat cohesive
    pickedElemFaces = p1.Surface(face1Elements=faceElements[0], face2Elements=faceElements[1],
                                 face3Elements=faceElements[2], face4Elements=faceElements[3],
                                 face5Elements=faceElements[4], face6Elements=faceElements[5], name='Surf-1')

p1.PartFromMesh(name='{}-mesh-1'.format(partBaseName), copySets=True)

'''
pickedElemFaces = regionToolset.Region(face1Elements=faceElements[0],
                                       face4Elements=faceElements[3],
                                       face5Elements=faceElements[4])
p1.insertElements(elemFaces=pickedElemFaces)
'''

