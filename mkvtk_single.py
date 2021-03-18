import numpy as np
import pandas as pd
import gc
import os

###---singlevtkファイルを書き出し---###
os.makedirs("vtk",exist_ok=True)

###---define input---###
strainxx = "xx.str"
strainzz = "zz.str"
strainxz = "xz.str"
displacementx = "x.disp"
displacementz = "z.disp"
# velocityx = "x.vel"
# velocityz = "z.vel"

##--read files--##
# with open("var.txt") as f:
#     lines = f.readlines()
#     modelid = int(lines[0].split()[0])
#     area_x = float(lines[1].split()[0])
#     area_z = float(lines[1].split()[1])
#     nx = int(lines[2].split()[0])
#     nz = int(lines[2].split()[1])
#     if modelid == 1:
#         nx2 = int(lines[3].split()[1])
#         nx1 = int(lines[3].split()[0])
#         nz1 = int(lines[4].split()[0])
#         nz2 = int(lines[4].split()[0])
#         inputwave = lines[5].split()[1]
#         fsamp = int(lines[5].split()[2])
#         duration = float(lines[5].split()[3])
#     else:
#         inputwave = lines[3].split()[1]
#         fsamp = int(lines[3].split()[2])
#         duration = float(lines[3].split()[3])

with open("mesh.in") as f:
    lines = f.readlines()
    nnode,nelem,nmaterial,dof = [int(s) for s in lines[0].split()]      #connected elementなども含む

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


###---define mesh shape---###
##---set nodepoints---##
points = [ "{} {} {} \n".format("POINTS",nnode,"float") ]      #全ノード数

nodeset = []
for i in range(nnode):
    nodeset += [ "{} {} {}\n".format(nodes[i][1],0,nodes[i][2])]

##---set element---##
cellset = []
for i in range(nelem):
    if elements[i][1] == "2d9solid":
        cellset += [ "{} {}\n".format("9"," ".join(elements[i][3:]))]

n9elem = len(cellset)       #9-node isoparametric element総数
cells = [ "{} {} {} \n".format("CELLS",n9elem,10*n9elem) ]      #(アイソ接点数+1)*nelemnt
celltypes = [ "{} {}\n".format("CELL_TYPES",n9elem)]       #CELL_TYPES,nelement
celltypesset = []
for i in range(n9elem):
    celltypesset += ["28 "]   #9-nodeVTK_BIQUADRATIC_QUAD


###---read table--###
strxx = pd.read_table(strainxx,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
strzz = pd.read_table(strainzz,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
strv = strxx+strzz      #体積ひずみ
del strxx,strzz
gc.collect()
strxz = pd.read_table(strainxz,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
dispx = pd.read_table(displacementx,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
dispz = pd.read_table(displacementz,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
velx = pd.read_table(velocityx,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')
velz = pd.read_table(velocityz,header=None,sep=" ",usecols=lambda x: x not in[0],engine='python')


##---cell data---##
strxz_absmax_tim = strxz.abs().max(axis=1).idxmax()    #shearstrain絶対値の最大値のindex
strv_max_tim = strv.abs().max(axis=1).idxmax()      #volstrain絶対値の最大値のindex

celldatasetlines = ["{} {}\n".format("CELL_DATA",n9elem)]
celldatasetlines0 = ["{} {} {}\n".format("SCALARS","materialid","int")]
celldata0 = []
celldatasetlines1 = ["{} {}{} {}\n".format("SCALARS","shearstrain_max@",strxz_absmax_tim,"float")]
celldata1 = []
celldatasetlines2 = ["{} {}{} {}\n".format("SCALARS","volstrain_max@",strv_max_tim,"float")]        #@~は最大値をとる時刻
celldata2 = []

for i in range(n9elem):
    celldata0 += ["{}\n".format(elements[i][2])]
    celldata1 += ["{}\n".format(strxz.iloc[strxz_absmax_tim,i])]
    celldata2 += ["{}\n".format(strv.iloc[strv_max_tim,i])]


##--node data---##
pointdatasetlines = ["{} {}\n".format("POINT_DATA",nnode)]
pointdatasetlines1 = ["{} {} {}\n".format("VECTORS","disp@shearstrain_max","float")]        #nax~時のメッシュ変形用
pointdata1 = []
pointdatasetlines2 = ["{} {} {}\n".format("VECTORS","disp@volstrain_max","float")]
pointdata2 = []

for k in range(nnode):
    pointdata1 += ["{} {} {}\n".format(dispx.iloc[i,k],"0.0",dispz.iloc[i,k])]
    # pointdata2 += ["{} {} {}\n".format(velx.iloc[i,k],"0.0",velz.iloc[i,k])]


##---write vtkfile---##
os.makedirs("vtk",exist_ok=True)
with open("vtk/output.vtk","w") as f:

    ###---mesh---###
    f.writelines(["# vtk DataFile Version 3.0\n", "output\n", "ASCII\n", "DATASET UNSTRUCTURED_GRID\n"])
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
