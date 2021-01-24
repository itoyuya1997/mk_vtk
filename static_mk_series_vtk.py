###---USE ONLY IN "output/<YYYYMMDD-time>"---###

#for dispwarp and materialid

import numpy as np
import pandas as pd
import gc
import os
if os.path.dirname(__file__):       #currentdirectoryをfile位置にセット
    os.chdir(os.path.dirname(__file__))

os.makedirs("vtk",exist_ok=True)
##--read files--##
with open("var.txt") as f:
    lines = f.readlines()
    modelid = int(lines[0].split()[0])
    area_x = float(lines[1].split()[0])
    area_z = float(lines[1].split()[1])
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
        elements += [items]         #[id,style,im,nodeid]


    irec += nelem
    materials = []
    for imaterial in range(nmaterial):
        items = lines[imaterial+irec].split()

        id = int(items[0])
        style = items[1]
        param = [float(s) for s in items[2:11]]


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

nselem = len(cellset)
cells = [ "{} {} {} \n".format("CELLS",nselem,10*nselem) ]      #アイソ接点数+1

celltypes = [ "{} {}\n".format("CELL_TYPES",nselem)]       #"CELL_TYPES,nelement"

_celltypesset = ["28 "]     #9-nodeVTK_BIQUADRATIC_QUAD
celltypesset = []
for i in range(nselem):
    celltypesset += _celltypesset


##---read table--##
#time column省き，ilocのindexは0始まり
# strxx = pd.read_table('strainxx.dat',header=None,sep="    ",engine='python')
# strzz = pd.read_table('strainzz.dat',header=None,sep="    ",engine='python')
# vstr = strxx+strzz
# del strxx,strzz
# gc.collect()
strxz = pd.read_table('strainxz.dat',header=None,sep="    ",engine='python')
dispx = pd.read_table('dispx.dat',header=None,sep="    ",engine='python')
dispz = pd.read_table('dispz.dat',header=None,sep="    ",engine='python')
# velx = pd.read_table('velx.dat',header=None,sep="    ",engine='python')
# velz = pd.read_table('velz.dat',header=None,sep="    ",engine='python')

a =  200   #define read time interval
n = 1       #vtk file number

##---cell data---##
celldatasetlines = ["{} {}\n".format("CELL_DATA",nselem)]
celldatasetlines0 = ["{} {} {}\n".format("SCALARS","materialid","int")]
celldata0 = []

# celldatasetlines1 = ["{} {} {}\n".format("SCALARS","shearstrain","float")]
# celldata1 = []
#
# celldatasetlines2 = ["{} {} {}\n".format("SCALARS","volstrain","float")]
# celldata2 = []


##--node data---##
pointdatasetlines = ["{} {}\n".format("POINT_DATA",nnode)]

pointdatasetlines1 = ["{} {} {}\n".format("VECTORS","displacement","float")]
pointdata1 = []
# pointdatasetlines2 = ["{} {} {}\n".format("VECTORS","velosity","float")]
# pointdata2 = []


##---write vtkfile---##

for i in range(int(fsamp*duration)):        #fsamp*duration
    if i%a == 0:
        pointdata1.clear()
        # pointdata2.clear()
        for k in range(nnode):
            pointdata1 += ["{} {} {}\n".format(dispx[k+1][i],"0.0",dispz[k+1][i])]
            # pointdata2 += ["{} {} {}\n".format(velx[k+1][i],"0.0",velz[k+1][i])]

        celldata0.clear()
        # celldata1.clear()
        # # celldata2.clear()
        for j in range(nselem):
            celldata0 += ["{}\n".format(elements[j][2])]
        #     # celldata1 += ["{}\n".format(strxz[j+1][i])]
        #     celldata2 += ["{}\n".format(vstr[j+1][i])]
        outputvtk = "{}{}{}".format("vtk/series-",str(n).zfill(7),".vtk")
        n += 1
        with open(outputvtk,"w") as f:
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
            ##---node data---##
            f.writelines(pointdatasetlines)        #"POINT_DATA",nnode

            f.writelines(pointdatasetlines1)       #"VECTORS",dataname,dtype
            f.writelines(pointdata1)
            # f.writelines(pointdatasetlines2)       #"VECTORS",dataname,dtype
            # f.writelines(pointdata2)

            ###---cell data---###
            f.writelines(celldatasetlines)        #"CELL_DATA",nselem

            f.writelines(celldatasetlines0)       #"SCALARS",dataname,dtype
            f.writelines("LOOKUP_TABLE default\n")      #data　reference
            f.writelines(celldata0)

            # f.writelines(celldatasetlines1)       #"SCALARS",dataname,dtype
            # f.writelines("LOOKUP_TABLE default\n")      #data　reference
            # f.writelines(celldata1)

            # f.writelines(celldatasetlines2)       #"SCALARS",dataname,dtype
            # f.writelines("LOOKUP_TABLE default\n")      #data　reference
            # f.writelines(celldata2)
