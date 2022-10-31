# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
import random
import math
import numpy as np

fields = (('Basic:','Part-1'),
          ('Embedded1:', 'Part-dg'),
          ('Creat set_name1:', 'dgl'),
          ('Embedded2:', 'Part-zgl'),
          ('Creat set_name2:', 'zgl'),
          ('Embedded3:', 'Part-xgl'),
          ('Creat set_name3:', 'xgl'),
          ('Creat set_name4:', 'shajiang'))

param=getInputs(fields=fields,)
Basic=param[0]
Embedded1,set_name1=param[1],param[2]
Embedded2,set_name2=param[3],param[4]
Embedded3,set_name3=param[5],param[6]
set_name4=param[7]

p = mdb.models['Model-1'].parts[Basic]
p1 = mdb.models['Model-1'].parts[Embedded1]
p2 = mdb.models['Model-1'].parts[Embedded2]
p3 = mdb.models['Model-1'].parts[Embedded3]

c= mdb.models['Model-1'].rootAssembly
c1 = c.instances['{}-1'.format(Embedded1)]
c2 = c.instances['{}-1'.format(Embedded2)]
c3 = c.instances['{}-1'.format(Embedded3)]

elements = p.elements
nodes = p.nodes

dgl_node_labels=[]
zgl_node_labels=[]
xgl_node_labels=[]
sj_node_labels=[]

for node_i in range(len(nodes)):
    coordinate = nodes[node_i].coordinates

    if len(c1.cells.findAt((coordinate,), printWarning=False)):
        dgl_node_labels.append(node_i)
    elif len(c2.cells.findAt((coordinate,), printWarning=False)):
        zgl_node_labels.append(node_i)
    elif len(c3.cells.findAt((coordinate,), printWarning=False)):
        xgl_node_labels.append(node_i)
    else:
        sj_node_labels.append(node_i)

dgl_elem_lists = []
zgl_elem_lists = []
xgl_elem_lists = []
sj_elem_lists = []

for elem_i in range(len(elements)):
    x1 = set(dgl_node_labels)
    x2 = set(zgl_node_labels)
    x3 = set(xgl_node_labels)
    y = set(elements[elem_i].connectivity)

    if y <= x1:
        dgl_elem_lists.append(elem_i+1)
    elif y <= x2:
        zgl_elem_lists.append(elem_i+1)
    elif y <= x3:
        xgl_elem_lists.append(elem_i+1)
    else:
        sj_elem_lists.append(elem_i+1)


p.Set(elements=elements.sequenceFromLabels(labels=dgl_elem_lists), name=set_name1)
p.Set(elements=elements.sequenceFromLabels(labels=zgl_elem_lists), name=set_name2)
p.Set(elements=elements.sequenceFromLabels(labels=xgl_elem_lists), name=set_name3)
p.Set(elements=elements.sequenceFromLabels(labels=sj_elem_lists), name=set_name4)


