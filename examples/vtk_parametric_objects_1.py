import math
import vtk
import BVtkRenderWindow as RW
R = RW.Init()

P1 = vtk.vtkProperty()
P1.SetColor(.8,.8,.8)
P2 = vtk.vtkProperty()
P2.SetColor(.8, 0, 0)

def Show( func, pos=(0,0,0) ):
    global R
    PFS = vtk.vtkParametricFunctionSource()
    PFS.SetParametricFunction(func)
    M = vtk.vtkPolyDataMapper()
    M.SetInputConnection( PFS.GetOutputPort() )
    A = vtk.vtkActor()
    A.SetPosition(pos)
    A.SetMapper(M)
    A.SetProperty(P1)
    A.SetBackfaceProperty(P2)
    R.AddActor(A)
    TA3 = vtk.vtkTextActor3D()
    TA3.SetInput(func.GetClassName().replace('vtkParametric',''))
    TA3.GetTextProperty().SetFontSize(20)
    TA3.SetScale(.02)
    TA3.SetPosition(pos[0], pos[1]-2, pos[2]+.1)
    R.AddActor(TA3)
    return A

lst = [
vtk.vtkParametricBoy(),            
vtk.vtkParametricConicSpiral(),    
vtk.vtkParametricCrossCap(),       
vtk.vtkParametricDini(),           
vtk.vtkParametricFigure8Klein(),   
vtk.vtkParametricKlein(),
vtk.vtkParametricKuen(),           
vtk.vtkParametricMobius(),
vtk.vtkParametricPseudosphere(),   
vtk.vtkParametricRoman(),          
#vtk.vtkParametricCatalanMinimal(), 
#vtk.vtkParametricEllipsoid(),      
#vtk.vtkParametricEnneper(),        
#vtk.vtkParametricHenneberg(),      
#vtk.vtkParametricPluckerConoid(),  
#vtk.vtkParametricRandomHills(),    
#vtk.vtkParametricSpline(),         
#vtk.vtkParametricSuperEllipsoid(), 
#vtk.vtkParametricSuperToroid(),    
#vtk.vtkParametricTorus(),          
]

x0 = 14 #len(lst)*3/2.0
for i,f in enumerate( lst ):
    Show( f, ( i*3-x0, 0, 0 ) )
                  
