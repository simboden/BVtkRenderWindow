# <pep8 compliant>

# TODO
# [ok]-- fix viewport pos,size
# [ok]-- transparent background
# [ok]-- sync camera position,target,viewup,clipping
# [ok]-- synch camera parallel/perspective,fov
# [ok]-- synch light
# [ok]-- vtk grid
# match grids size,scale,num,....
# synch solid/wireframe
# .... keep the zbuffer ....
# .... implement reset camera, ( reset vtkCamera and copy it on the Blender Camera )

# refs
#https://blender.stackexchange.com/questions/75612/how-do-you-remove-a-draw-handler-after-its-been-added

#---------------------------------------------------------------------------------
# ADDON HEADER SECTION
#---------------------------------------------------------------------------------

bl_info = {
    "name": "BVtkRenderWindow",
    "author": "Silvano Imboden",
    "version": (0, 0),
    "blender": (2, 79,  0),
    "location": "View3D > UI",
    "description": "create a vtkRenderWindow which draws inside the Blender View3D",
    "warning": "require VTK compiled using OpenGL1 and wrapped in python using Python3.5",
    "wiki_url": "",
    "category": "Misc",
    }

#---------------------------------------------------------------------------------
# MODULES IMPORT
#---------------------------------------------------------------------------------
try: 
    print( 'import vtk begin, please wait')
    import vtk
    print( 'import vtk done')
except: 
    pass

if 'vtk' not in globals() and 'vtk' not in locals():
    message = '''\n\n
    The BVtkRenWin addon depends on the vtk library.
    Unfortunately the Blender build you are using does not have access to this library.
    Please install vtk, and ensure that the blender python is able to import it.\n'''
    raise Exception(message)

Reloading = "bpy" in locals()
import bpy
import blf
import mathutils
import math

#---------------------------------------------------------------------------------
# VTK TEST PIPELINE
#---------------------------------------------------------------------------------

import vtk

CS=vtk.vtkConeSource()
CS.SetResolution(50)
M=vtk.vtkPolyDataMapper()
M.SetInputConnection( CS.GetOutputPort())
A=vtk.vtkActor()
A.SetMapper(M)

grid_actor   = None
grid_actor_x = None
grid_actor_y = None

def Init():

    global C,R,RW,RWI,OMW,grid_actor
    C=vtk.vtkCamera()
    R=vtk.vtkRenderer()
    R.SetActiveCamera(C)
    #R.AddActor(A)

    RW=vtk.vtkGenericOpenGLRenderWindow()
    RW.AddRenderer(R)
    RW.SetIsDirect(True)
    RW.SetSupportsOpenGL(True)

    RWI = vtk.vtkGenericRenderWindowInteractor()
    RWI.SetRenderWindow(RW)

    AA  = vtk.vtkAxesActor()
    OMW = vtk.vtkOrientationMarkerWidget()
    OMW.SetOrientationMarker( AA );
    OMW.SetInteractor( RWI );
    OMW.SetEnabled( 1 );
    OMW.SetInteractive(0);

    Lights = []
    for l in bpy.context.user_preferences.system.solid_lights:
        L = vtk.vtkLight()
        L.SetLightTypeToCameraLight()
        L.SetDiffuseColor( l.diffuse_color )
        L.SetSpecularColor( l.specular_color )
        L.SetPosition( l.direction )
        R.AddLight(L)
        Lights.append(L)
    grid_actor = None
    return R

Init()
R.AddActor(A)


def update_grid( show_grid ):
    global grid_actor,grid_actor_x,grid_actor_y,R
    if show_grid and not grid_actor:
        pd = vtk.vtkPolyData()
        pts = vtk.vtkPoints()
        cells = vtk.vtkCellArray()
        for x in range(-8,9):  
            if x != 0:      
                np = pts.GetNumberOfPoints()
                pts.InsertNextPoint( x,-8, 0)
                pts.InsertNextPoint( x, 8, 0)
                pts.InsertNextPoint(-8, x, 0)
                pts.InsertNextPoint( 8, x, 0)
                cells.InsertNextCell(2)
                cells.InsertCellPoint(np)
                cells.InsertCellPoint(np+1)
                cells.InsertNextCell(2)
                cells.InsertCellPoint(np+2)
                cells.InsertCellPoint(np+3)
        pd.SetPoints(pts)            
        pd.SetLines(cells)
        m=vtk.vtkPolyDataMapper()
        m.SetInputData( pd )
        grid_actor=vtk.vtkActor()
        grid_actor.SetMapper(m)
        grid_actor.GetProperty().SetColor(.27, .27, .27 )
        R.AddActor(grid_actor)

        lx = vtk.vtkLineSource()
        lx.SetPoint1(-8, 0, 0)
        lx.SetPoint2( 8, 0, 0)
        mx=vtk.vtkPolyDataMapper()
        mx.SetInputConnection( lx.GetOutputPort())
        grid_actor_x=vtk.vtkActor()
        grid_actor_x.SetMapper(mx)
        grid_actor_x.GetProperty().SetColor(.5, 0, 0 )
        R.AddActor(grid_actor_x)
        
        ly = vtk.vtkLineSource()
        ly.SetPoint1( 0,-8, 0)
        ly.SetPoint2( 0, 8, 0)
        my=vtk.vtkPolyDataMapper()
        my.SetInputConnection( ly.GetOutputPort())
        grid_actor_y=vtk.vtkActor()
        grid_actor_y.SetMapper(my)
        grid_actor_y.GetProperty().SetColor( 0, .5, 0 )
        R.AddActor(grid_actor_y)

    elif not show_grid and grid_actor:
        R.RemoveActor(grid_actor)
        R.RemoveActor(grid_actor_x)
        R.RemoveActor(grid_actor_y)
        grid_actor   = None    
        grid_actor_x = None    
        grid_actor_y = None    


#---------------------------------------------------------------------------------
# DRAW_CALLBACK
#---------------------------------------------------------------------------------
def draw_callback(context):

    global R,RW,C

    if context.scene.vtk_transparent_background:
        R.SetBackgroundAlpha (1)
        R.SetPreserveColorBuffer(1)
    else:
        R.SetBackground(.224,.224,.224)
        R.SetBackgroundAlpha (0)
        R.SetPreserveColorBuffer(0)

    update_grid( context.scene.vtk_grid )

    # the viewport is in the region ( == context.region )
    # camera lens and clipping range are in the space ( == context.space_data )
    # camera location and rotation are in region_3d ( == context.space_data.region_3d )
    # r3.view_location is the vtk_target
    # r3.view_distance is the distance of the camera from the target
    # r3.view_rotation is a quaternion

    s  = context.space_data
    r3 = context.space_data.region_3d
    r  = context.region
    x,y,w,h = r.x, r.y, r.width, r.height

    up_v = mathutils.Vector((0,1,0))
    up_v.rotate( r3.view_rotation )
    dist_v = mathutils.Vector((0,0,r3.view_distance))
    dist_v.rotate( r3.view_rotation )
    
    C.SetFocalPoint( r3.view_location  )
    C.SetPosition( r3.view_location + dist_v )
    C.SetViewUp( up_v )
    C.SetClippingRange( s.clip_start, s.clip_end )

    # retrieve the fov from camera lens and aspect ratio is not trivial
    m = vtk.vtkMatrix4x4()
    bm = r3.window_matrix
    for i in range(4):
        for j in range(4): 
            m.SetElement(i,j, bm[i][j] )
    C.SetExplicitProjectionTransformMatrix(m)
    C.UseExplicitProjectionTransformMatrixOn()

    vx = x/float(w+x)
    vy = y/float(h+y)
    R.SetViewport( vx, vy, 1, 1 )
    RW.SetSize(x+w,y+h)
    OMW.SetViewport( .8,.8,1,1 );

    RW.SetIsCurrent(True)
    RW.PushState()
    RW.OpenGLInitState()
    RW.Render()
    RW.PopState()


    font_id = 0 
    blf.size(font_id, 10, 100)
    #blf.position(font_id, 65, 30, 0)
    if context.scene.vtk_transparent_background:
        blf.position(font_id, 75, 30, 0)
        blf.draw(font_id, 'vtk overlay' )
    else:
        blf.position(font_id, 10, 10, 0)
        blf.draw(font_id, 'vtk' )

#---------------------------------------------------------------------------------
# DRAW_CALLBACK_HANDLE
#---------------------------------------------------------------------------------
draw_callback_handle = None

def vtk_rendering_toggled(self,context):
    # self is the panel, contex is as in panel.draw
    global draw_callback_handle
    space = context.space_data

    if self.vtk_rendering_enabled and draw_callback_handle is None:

        draw_callback_handle = space.draw_handler_add(draw_callback, (context,), 'WINDOW','POST_PIXEL')

    elif not self.vtk_rendering_enabled and not draw_callback_handle is None:

        space.draw_handler_remove(draw_callback_handle, 'WINDOW')
        draw_callback_handle = None

#---------------------------------------------------------------------------------
# UI
#---------------------------------------------------------------------------------
# Properties can only be attached to blender 'TYPES' derived from 'ID',
# so to Scene,Objects,Materials,Nodes ... but not to Panels or Views,Spaces,Regions,Areas....
# For the moment I'll attach this property to the Scene

bpy.types.Scene.vtk_rendering_enabled = bpy.props.BoolProperty(
    name='vtk_rendering_enabled', 
    default=False,  
    update=vtk_rendering_toggled )

bpy.types.Scene.vtk_transparent_background = bpy.props.BoolProperty(
    name='vtk_transparent_background', 
    default=False )

bpy.types.Scene.vtk_grid = bpy.props.BoolProperty(
    name='vtk_grid', 
    default=True )

class View3DVTKPanel(bpy.types.Panel):
    bl_idname      = "VIEW3D_VTK_Panel"
    bl_label       = "VTK Rendering"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        self.layout.prop( context.scene, 'vtk_rendering_enabled',      'enable' )
        self.layout.prop( context.scene, 'vtk_transparent_background', 'overlay' )
        self.layout.prop( context.scene, 'vtk_grid',                   'grid' )

#---------------------------------------------------------------------------------
# Clear
#---------------------------------------------------------------------------------
def Clear_old():
    global grid_actor, R, C, RW
    RW.RemoveRenderer(R)
    R= vtk.vtkRenderer()
    R.SetActiveCamera(C)
    RW.AddRenderer(R)
    grid_actor = None # will be remade
    return R

#---------------------------------------------------------------------------------
# Update
#---------------------------------------------------------------------------------
def Update():
    #bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    bpy.data.scenes[0].update()
    
#---------------------------------------------------------------------------------
# Register
#---------------------------------------------------------------------------------
def register():
    bpy.utils.register_class(View3DVTKPanel)

def unregister():
    bpy.utils.unregister_class(View3DVTKPanel)

if __name__ == "__main__":
    register()

