import math
import vtk
import BVtkRenderWindow as RW
R = RW.Init()

def Show(data,pos=(0,0,0)):
    # Show a vtkData by creating a Mapper, an Actor
    # and inserting the Actor in the Renderer.
    # also add a text label with the data classname
    global R
    if data.IsA('vtkPolyData'):
        M = vtk.vtkPolyDataMapper()
    else:
        M = vtk.vtkDataSetMapper()
    M.SetInputData( data )
    A = vtk.vtkActor()
    A.SetMapper(M)
    A.GetProperty().EdgeVisibilityOn()
    A.GetProperty().SetEdgeColor(.3,.3,.3)
    A.SetPosition(pos)    
    TA3 = vtk.vtkTextActor3D()
    TA3.SetInput(data.GetClassName())
    TA3.GetTextProperty().SetFontSize(24)
    TA3.SetScale(.02)
    TA3.SetPosition(pos[0], pos[1]-1, pos[2]+.1)
    R.AddActor(TA3)
    R.AddActor(A)
    return A

def normalize(pts):
    # take a list of verts(x,y,z) and normalize them ( center and scale to unity )
    # plus there is some extra shift and scale for the pourpose of this example
    x_lst = sorted( [i[0] for i in pts ] )
    y_lst = sorted( [i[1] for i in pts ] )
    z_lst = sorted( [i[2] for i in pts ] )
    min_x, max_x = x_lst[0], x_lst[-1]
    min_y, max_y = y_lst[0], y_lst[-1]
    min_z, max_z = z_lst[0], z_lst[-1]
    cx, sx = (min_x+max_x)/2.0, (max_x-min_x)*.6
    cy, sy = (min_y+max_y)/2.0, (max_y-min_y)*.6
    cz, sz = (min_z+max_z)/2.0, (max_z-min_z)*.6
    return [ ( (i[0]-cx)/sx, (i[1]-cy)/sy+.5, (i[2]-cz)/sz+.8 ) for i in pts ]  

# vtkStructuredPoints example

SP = vtk.vtkStructuredPoints()
SP.SetOrigin(0,0,0)
SP.SetDimensions(6,4,3)
SP.SetSpacing(1,1,1)

Show(SP,(-8,0,0))

# vtkRectilinearGrid example

Coords = vtk.vtkFloatArray()
for x in [0,.5,1,2,4]: 
    Coords.InsertNextTuple1(x)

RG = vtk.vtkRectilinearGrid()
RG.SetDimensions(5,5,5)
RG.SetXCoordinates(Coords)
RG.SetYCoordinates(Coords)
RG.SetZCoordinates(Coords)

Show(RG,(-2,0,0))

# vtkStructuredGrid example

pts = vtk.vtkPoints()
for i in range(0,100,10):
    a = i*math.pi/180.0
    ca = cos(a)
    sa = sin(a)
    pts.InsertNextPoint( ca,   0,   sa )
    pts.InsertNextPoint( 2*ca, 0, 2*sa )
    pts.InsertNextPoint( 4*ca, 0, 4*sa )
    pts.InsertNextPoint( ca,   2,   sa )
    pts.InsertNextPoint( 2*ca, 2, 2*sa )
    pts.InsertNextPoint( 4*ca, 2, 4*sa )

SG = vtk.vtkStructuredGrid()
SG.SetDimensions(3,2,10)
SG.SetPoints(pts)
Show(SG,(3,0,0))


# vtkPolyData example

lst = [(0,0,0),(1,0,0),(1,1,0),(0,1,0),
       (2,0,0),(3,0,0),(3,1,0),(2,1,0),
       (4,0,0),(5,0,0),(5,1,0),(4,1,0)]

pts = vtk.vtkPoints()
for pt in lst:
    pts.InsertNextPoint( pt )
    
verts = vtk.vtkCellArray()    
verts.InsertNextCell(4)
for i in range(4): verts.InsertCellPoint(i)

lines = vtk.vtkCellArray()    
lines.InsertNextCell(4)
for i in range(4,8): lines.InsertCellPoint(i)

polys = vtk.vtkCellArray()    
polys.InsertNextCell(4)
for i in range(8,12): polys.InsertCellPoint(i)

PD = vtk.vtkPolyData()
PD.SetPoints(pts)
PD.SetVerts(verts)
PD.SetLines(lines)
PD.SetPolys(polys)

PDA = Show(PD,(-3,-4, .1))
P = PDA.GetProperty()
P.SetEdgeColor(1,0,0)
P.SetPointSize(3)

# vtkUnstructuredGrid example

points = vtk.vtkPoints()
UG = vtk.vtkUnstructuredGrid()
UG.SetPoints(points)

# vtkTetra
np = points.GetNumberOfPoints()   
lst = normalize([(0,0,0),(1,0,0),(1,1,0),(1,0,1)])
for x,y,z in lst: points.InsertNextPoint(x,y,z)  

cell = vtk.vtkTetra()
for i in range(len(lst)): cell.GetPointIds().SetId(i, i+np)

UG.InsertNextCell(cell.GetCellType(), cell.GetPointIds() )

# vtkPyramid
np = points.GetNumberOfPoints()   
lst = normalize([( 1, 1, 0),(-1, 1, 0),(-1,-1, 0),( 1,-1, 0),( 0, 0, 1)])
for x,y,z in lst: points.InsertNextPoint(x+2,y,z) 

cell = vtk.vtkPyramid()
for i in range(len(lst)): cell.GetPointIds().SetId(i, i+np)

UG.InsertNextCell(cell.GetCellType(), cell.GetPointIds() )


# vtkWedge
np = points.GetNumberOfPoints()   
lst = normalize([(0, 1, 0),(0, 0, 0),(0,.5,.5),(1, 1, 0),(1,.0,.0),(1,.5,.5)])
for x,y,z in lst: points.InsertNextPoint(x+4,y,z) 

cell = vtk.vtkWedge()
for i in range(len(lst)): cell.GetPointIds().SetId(i, i+np)

UG.InsertNextCell(cell.GetCellType(), cell.GetPointIds() )

# vtkHexahedron 
np = points.GetNumberOfPoints()   
lst = normalize([(0, 0, 0),(1, 0, 0),(1, 1, 0),(0, 1, 0),
                 (0, 0, 1),(1, 0,.6),(1, 1,.6),(0, 1, 1)])

for x,y,z in lst: points.InsertNextPoint(x+6,y,z) 

cell = vtk.vtkHexahedron()
for i in range(len(lst)): cell.GetPointIds().SetId(i, i+np)

UG.InsertNextCell(cell.GetCellType(), cell.GetPointIds() )

# vtkVoxel
np = points.GetNumberOfPoints()   
lst = normalize([(0, 0, 0),(1, 0, 0),(0, 1, 0),(1, 1, 0),
                 (0, 0, 1),(1, 0, 1),(0, 1, 1),(1, 1, 1)])
for x,y,z in lst: points.InsertNextPoint(x+8,y,z) 

cell = vtk.vtkVoxel()
for i in range(len(lst)): cell.GetPointIds().SetId(i, i+np)  

UG.InsertNextCell(cell.GetCellType(), cell.GetPointIds() )

# vtkPentagonalPrism
np = points.GetNumberOfPoints()   
lst = normalize([(1, 0, 0),(3, 0, 0),(4, 2, 0),(2, 4, 0),(0, 2, 0),
                 (1, 0, 1),(3, 0, 1),(4, 2, 1),(2, 4, 1),(0, 2, 1)])
for x,y,z in lst: points.InsertNextPoint(x+10,y,z)

cell = vtk.vtkPentagonalPrism()
for i in range(len(lst)): cell.GetPointIds().SetId(i, i+np)

UG.InsertNextCell(cell.GetCellType(), cell.GetPointIds() )

# vtkHexagonalPrism
np = points.GetNumberOfPoints()   
lst = normalize([( 0, 0, 2),( 2, 0, 2),( 3, 1, 2),( 2, 2, 2),( 0, 2, 2),(-1, 1, 2),
                 ( 0, 0, 0),( 2, 0, 0),( 3, 1, 0),( 2, 2, 0),( 0, 2, 0),(-1, 1, 0) ])
for x,y,z in lst: points.InsertNextPoint(x+12,y,z)
  
cell = vtk.vtkHexagonalPrism()
for i in range(len(lst)): cell.GetPointIds().SetId(i, i+np)

UG.InsertNextCell(cell.GetCellType(), cell.GetPointIds() )

# polyhedron ( VTK_POLYHEDRON )
np = points.GetNumberOfPoints()   
lst = normalize([
( 1.21,  0,      1.59),
( 0.37,  1.1547, 1.59),
(-0.99,  0.71,   1.59),
(-0.99, -0.71,   1.59),
( 0.37, -1.15,   1.59),
( 1.96,  0,      0.37),
( 0.60,  1.86,   0.37),
(-1.59,  1.15,   0.37),
(-1.59, -1.15,   0.37),
( 0.60, -1.86,   0.37),
( 1.59,  1.15,  -0.37),
(-0.60,  1.86,  -0.37),
(-1.96,  0,     -0.37),
(-0.60, -1.86,  -0.37),
( 1.59, -1.15,  -0.37),
( 0.98,  0.71,  -1.59),
(-0.37,  1.15,  -1.59),
(-1.21,  0,     -1.59),
(-0.37, -1.15,  -1.59),
( 0.98, -0.71,  -1.59)])

for x,y,z in lst: points.InsertNextPoint(x+14,y,z)  
    
faces = [
(0,   1,   2,  3,   4),
(0,   5,  10,  6,   1),
(1,   6,  11,  7,   2),
(2,   7,  12,  8,   3),
(3,   8,  13,  9,   4),
(4,   9,  14,  5,   0),
(15, 10,   5,  14, 19),
(16, 11,   6,  10, 15),
(17, 12,   7,  11, 16),
(18, 13,   8,  12, 17),
(19, 14,   9,  13, 18),
(19, 18,  17,  16, 15)]

faces_ids  = vtk.vtkIdList()
faces_ids.InsertNextId( len(faces) )            # number of faces 
for f in faces:
    faces_ids.InsertNextId(len(f))              # number of points in this face
    for i in f : faces_ids.InsertNextId(i+np)   # pointIds of this face.

UG.InsertNextCell(vtk.VTK_POLYHEDRON, faces_ids )

UGA = Show(UG,(-7,-8,0))


