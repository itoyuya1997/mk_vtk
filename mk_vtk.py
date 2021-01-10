###---USE ONLY IN "output/<YYYYMMDD-time>"---###

import numpy as np
import pandas as pd
import gc
import os
if os.path.dirname(__file__):       #currentdirectoryをfile位置にセット
    os.chdir(os.path.dirname(__file__))

##--read files--##
# with open("var.in") as f:
with open("var.txt") as f:
    lines = f.readlines()
    modelid = int(lines[0].split()[0])
    area_x = int(lines[1].split()[0])
    area_z = int(lines[1].split()[1])
    nx = int(lines[2].split()[0])
    nz = int(lines[2].split()[1])
    if modelid == 1:
        nx2 = int(lines[3].split()[1])
        nx1 = int(lines[3].split()[0])
        nz1 = int(lines[4].split()[0])
        nz2 = int(lines[4].split()[0])
        inputwave = lines[5].split()[1]
        fsamp = int(lines[5].split()[2])
        duration = float(lines[5].split()[3])
    else:
        inputwave = lines[3].split()[1]
        fsamp = int(lines[3].split()[2])
        duration = float(lines[3].split()[3])


with open("mesh.in") as f:
    lines = f.readlines()
    nnode,nelem,nmaterial,dof = [int(s) for s in lines[0].split()]  #cautin nelem

    irec = 1
    nodes = []
    for inode in range(nnode):
        items = lines[inode+irec].split()
        nodes += [items]        #[id,x,z,dofx,dofz]

    irec += nnode
    elements = []
    for ielem in range(nelem):
        items = lines[ielem+irec].split()
        elements += [items]         #[id,style,im,nodeid


    irec += nelem
    materials = []
    for imaterial in range(nmaterial):
        items = lines[imaterial+irec].split()

        id = int(items[0])
        style = items[1]
        param = [float(s) for s in items[2:11]]




##---var setup---##





##---set nodepoints---##
points = [ "{} {} {} \n".format("POINTS",nnode,"float") ]      #全ノード数

nodeset = []      #set node
for i in range(nnode):
    nodeset += [ "{} {} {}\n".format(nodes[i][1],0,nodes[i][2])]

##---set element---##
cellset = []
for i in range(nelem):
    if elements[i][1] == "2d9solid":
        cellset += [ "{} {}\n".format("9"," ".join(elements[i][3:]))]

nselem = len(cellset)       #connected element除く全element数
cells = [ "{} {} {} \n".format("CELLS",nselem,10*nselem) ]      #アイソ接点数+1

celltypes = [ "{} {}\n".format("CELL_TYPES",nselem)]       #"CELL_TYPES,nelement"

_celltypesset = ["28 "]     #9-nodeVTK_BIQUADRATIC_QUAD
celltypesset = []
for i in range(nselem):
    celltypesset += _celltypesset


##---read table--##
#time column省き，indexは0始まり
strxx = pd.read_table('strainxx.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
strzz = pd.read_table('strainzz.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
vstr = strxx+strzz
del strxx,strzz
gc.collect()
strxz = pd.read_table('strainxz.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
# dispx = pd.read_table('dispx.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
# dispz = pd.read_table('dispz.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
# velx = pd.read_table('velx.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')
# velz = pd.read_table('velz.dat',header=None,sep="    ",usecols=lambda x: x not in[0],engine='python')


##---cell data---##
celldatasetlines = ["{} {}\n".format("CELL_DATA",nselem)]
celldatasetlines0 = ["{} {} {}\n".format("SCALARS","materialid","int")]
celldata0 = []
for i in range(nselem):
    celldata0 += ["{}\n".format(elements[i][2])]

celldata1 = []
strxz_absmax_tim = strxz.abs().max(axis=1).idxmax()
for i in range(nselem):
    celldata1 += ["{}\n".format(strxz.iloc[strxz_absmax_tim,i])]
celldatasetlines1 = ["{} {}{} {}\n".format("SCALARS","shearstrain_max@",strxz_absmax_tim,"float")]

celldata2 = []
vstr_max_tim = vstr.max(axis=1).idxmax()      #最大volstrainのindex
for i in range(nselem):
    celldata2 += ["{}\n".format(vstr.iloc[vstr_max_tim,i])]
celldatasetlines2 = ["{} {}{} {}\n".format("SCALARS","volstrain_max@",vstr_max_tim,"float")]        #@~は最大値をとる時刻

##--node data---##


##---write vtkfile---##
os.makedirs("vtk",exist_ok=True)
with open("vtk/output.vtk","w") as f:

    ###---mesh---###
    f.write("# vtk DataFile Version 3.0\n")
    f.write("output\n")       #vtk title
    f.write("ASCII\n")
    f.write("DATASET UNSTRUCTURED_GRID\n")
    f.writelines(points)        #"POINTS",nnode,dtype
    f.writelines(nodeset)       #define nodes
    f.writelines(cells)         #"CELLS",nselem,node_in_element+1
    f.writelines(cellset)       #define cells
    f.writelines(celltypes)     #"CELL_TYPES",nselem
    f.writelines(celltypesset)  #define celltype]
    f.write("\n")

    ###---cell data---###
    f.writelines(celldatasetlines)        #"CELL_DATA",nselem

    f.writelines(celldatasetlines0)       #"SCALARS",dataname,dtype
    f.writelines("LOOKUP_TABLE default\n")      #data　reference
    f.writelines(celldata0)

    f.writelines(celldatasetlines1)       #"SCALARS",dataname,dtype
    f.writelines("LOOKUP_TABLE default\n")      #data　reference
    f.writelines(celldata1)

    f.writelines(celldatasetlines2)       #"SCALARS",dataname,dtype
    f.writelines("LOOKUP_TABLE default\n")      #data　reference
    f.writelines(celldata2)
