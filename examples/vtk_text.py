'''
 'vtkBillboardTextActor3D',
 'vtkMathTextFreeTypeTextRenderer',
 'vtkMathTextUtilities',
 'vtkMathTextUtilitiesCleanup',
 'vtkScaledTextActor',
 'vtkTextActor',
 'vtkTextActor3D',
 'vtkTextCodec',
 'vtkTextCodecFactory',
 'vtkTextMapper',
 'vtkTextProperty',
 'vtkTextRenderer',
 'vtkTextRendererCleanup',
 'vtkTextRendererStringToImage',
 'vtkTextRepresentation',
 'vtkTextSource',
 'vtkTextWidget',
 'vtkUTF16TextCodec',
 'vtkUTF8TextCodec',
 'vtkVectorText',
'''

import vtk
import BVtkRenderWindow as RW
R = RW.Init() # remove any previous actor

'''
vtkTextActor: An actor that displays text. Scaled or unscaled.
vtkTextActor can be used to place text annotation into a window.
When TextScaleMode is NONE, the text is fixed font and operation
is the same as a vtkPolyDataMapper2D/vtkActor2D pair.
When TextScaleMode is VIEWPORT, the font resizes such that it maintains
a consistent size relative to the viewport in which it is rendered.
When TextScaleMode is PROP, the font resizes such that the text fits
inside the box defined by the position 1 & 2 coordinates.
This class replaces the deprecated vtkScaledTextActor
and acts as a convenient wrapper for a vtkTextMapper/vtkActor2D pair.
Set the text property/attributes through the vtkTextProperty associated
to this actor.
'''

TA = vtk.vtkTextActor()
TA.SetInput('TextActor')
TA.GetTextProperty().SetFontSize(24)
R.AddActor(TA)

'''
vtkTextActor3D: An actor that displays text.
The input text is rendered into a buffer, which in turn
is used as a texture applied onto a quad (a vtkImageActor is used under the hood).
'''
TA3 = vtk.vtkTextActor3D()
TA3.SetInput('TextActor3D')
TA3.GetTextProperty().SetFontSize(24)
TA3.SetScale(.01)
R.AddActor(TA3)

'''
vtkVectorText: create polygonal text
vtkVectorText generates vtkPolyData from an input text string.
Besides the ASCII alphanumeric characters a-z,A-Z, 0-9, vtkVectorText also supports ASCII punctuation marks.
(The supported ASCII character set are the codes (33-126) inclusive.)
The only control character supported is the line feed character "\n", which advances to a new line.
To use thie class, you normally couple it with a vtkPolyDataMapper and a vtkActor.
In this case you would use the vtkActors transformation methods to position, orient, and scale the text.
You may also wish to use a vtkFollower to orient the text so that it always faces the camera.
'''
VT = vtk.vtkVectorText()
VT.SetText('vtkVectorText')
VTM = vtk.vtkPolyDataMapper()
VTM.SetInputConnection( VT.GetOutputPort() )
VTA = vtk.vtkActor()
VTA.SetMapper(VTM)
VTA.SetScale(.1)
VTA.SetPosition(0,-0.5,0)
R.AddActor(VTA)

'''
You may also wish to use a vtkFollower to orient the text so that it always faces the camera.
'''
VT2 = vtk.vtkVectorText()
VT2.SetText('vtkFollower')
VTM2 = vtk.vtkPolyDataMapper()
VTM2.SetInputConnection( VT2.GetOutputPort() )
VTAF = vtk.vtkFollower()
VTAF.SetMapper(VTM2)
VTAF.SetScale(.1)
VTAF.SetPosition(0,-1,0)
VTAF.SetCamera( R.GetActiveCamera() )
R.AddActor(VTAF)


