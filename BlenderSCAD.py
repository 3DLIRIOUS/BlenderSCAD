## OpenSCAD like Blender programming
## This is just a proof of concept implementation - Work in Progress.
## It will enhance Blender with additional Python definitions for convenience. 
## Should help in making scripting as easy as in OpenSCAD. 
##
## in a later phase, simple OpenSCAD could be transformed into something that evaluates in Blender
##  might be a way to join projects and overcome OpenSCAD performance problems?
## written by Michael Mlivoncic, December 2013

# TODOs
# - resize: adjust location
# - minkowski sum emulation?
# - $fn ...

## Instructions
#
### Open in Blenders's internal text editor and run as script.
#
## Warning: The open file will be saved as part of the blender file, be careful if you change it externally as well!
## To see output and error messages: Window->Toggle System Console  
#
### To edit in external editor and run in Blender's Python Console:
#
## filename = "O:/BlenderStuff/BlenderSCAD.py
## clearAllObjects()
## exec(compile(open(filename).read(), filename, 'exec'))
#
### Clear command history in Python Console:
## bpy.ops.console.clear(history=True)

import os
import bpy
import bpy_types

mylayers = [False]*20
mylayers[0] = True

#We create a reference to the operator that is used for creating a cube mesh primitive
add_cube = bpy.ops.mesh.primitive_cube_add
add_cylinder = bpy.ops.mesh.primitive_cylinder_add
add_cone = bpy.ops.mesh.primitive_cone_add
#translate = bpy.ops.transform.translate

# need to setup our default material
mat = bpy.data.materials.get('useObjectColor') 
if mat is None:
	mat=bpy.data.materials.new('useObjectColor')
	mat.use_object_color=1


#constants
true=True
false=False
pi = 3.141592

# some colors... 
black = (0.00,0.00,0.00,0)
silver = (0.75,0.75,0.75,0)
gray = (0.50,0.50,0.50,0)
white = (1.00,1.00,1.00,0)
maroon = (0.50,0.00,0.00,0)
red = (1.00,0.00,0.00,0)
purple = (0.50,0.00,0.50,0)
fuchsia = (1.00,0.00,1.00,0)
green = (0.00,0.50,0.00,0)
lime = (0.00,1.00,0.00,0)
olive = (0.50,0.50,0.00,0)
yellow = (1.00,1.00,0.00,0)
navy = (0.00,0.00,0.50,0)
blue = (0.00,0.00,1.00,0)
teal = (0.00,0.50,0.50,0)
aqua = (0.00,1.00,1.00,0)

defColor = (1.0,1.0,0.1,0)  

#bpy.ops.object.mode_set(mode = 'OBJECT')

# remove everything after experiments...
def clearAllObjects():
	# FIX: Call fails if there are no objects...
	#bpy.ops.object.mode_set(mode = 'OBJECT')
	bpy.ops.object.select_all()
	bpy.ops.object.delete()
	bpy.ops.object.select_all()
	bpy.ops.object.delete()


# CAUTION! clear workspace 
clearAllObjects()   
   

# Construct a cube mesh 
# bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
def cube(size=(0.0,0.0,0.0), center=False):
	add_cube(location=(0.0,0.0,0.0), layers=mylayers)	
	myC = bpy.data.objects['Cube']
	myC.dimensions=size
	myC.name='cu()' # +str(index)   
	# simple color will only display via my def. Material setting
	myC.data.materials.append(mat)  
	# just some default color
	myC.color = (1.0,1.0,0.1,0)  
	# scale
	#bpy.ops.transform.resize(value=size)
	#bpy.ops.object.transform_apply(scale=True)
	if (center==False):
		bpy.ops.transform.translate(value=(size[0]/2,size[1]/2,size[2]/2))  
	return myC
	

# Construct a cylinder mesh
# bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=1.0, depth=2.0, end_fill_type='NGON', view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
def _cylinder(h=1, r=1):
	add_cylinder(location=(0.0,0.0,0.0), radius=r , depth=h , vertices=64, layers=mylayers)  
	myC = bpy.data.objects['Cylinder']
	myC.name='cy()' # +str(index)	
	return myC
	

# Construct a conic mesh 
#  bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=1.0, radius2=0.0, depth=2.0, end_fill_type='NGON', view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
def _cone(h=1, r1=1, r2=2):
	add_cone(location=(0.0,0.0,0.0), radius1=r1, radius2=r2, depth=h , vertices=64, layers=mylayers)	 
	myC = bpy.data.objects['Cone']
	myC.name='cn()' # +str(index)   
	return myC

	
# OpenSCAD: cylinder(h = <height>, r1 = <bottomRadius>, r2 = <topRadius>, center = <boolean>);
#		cylinder(h = <height>, r = <radius>);   
def cylinder(h = 1, r=1, r1 = -1, r2 = -1, center = False):
	if r1 != -1 and r2 != -1 :
		myC=_cone(h,r1,r2)
	else:   
		myC=_cylinder(h,r)
	# just a suitable default material and some default color
	myC.data.materials.append(mat)  
	myC.color = defColor
	if center==False:
		bpy.ops.transform.translate(value=(0,0,h/2))						
	return myC

	
# OpenSCAD: sphere(r=1, d=-1)   
# bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, size=1.0, view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), layers=(False,   
def sphere(r=1, d=-1, center=true):
	if d != -1 : 
		  r= d/2;
	bpy.ops.mesh.primitive_uv_sphere_add(size=r , segments=32, ring_count=16,location=(0.0,0.0,0.0), layers=mylayers)	
	myC = bpy.data.objects['Sphere']
	myC.name='sp()' # +str(index)   
	# simple color will only display via my def. Material setting
	myC.data.materials.append(mat)  
	# just some default color
	myC.color = (1.0,1.0,0.1,0)  
	# scale
	#bpy.ops.transform.resize(value=size)
	#bpy.ops.object.transform_apply(scale=True)
	return myC  

	
# OpenSCAD: translate(v = [x, y, z]) { ... }
def translate( v=(0.0,0.0,0.0), obj_A=None):	
	if obj_A is None: 
		obj_A = bpy.context.object  
	bpy.ops.object.select_all(action = 'DESELECT')
	obj_A.select = True
	bpy.ops.transform.translate(value=v)		
	return obj_A	

	
# OpenSCAD: rotate(a = deg, v = [x, y, z]) { ... }
# Rotation in Blender: http:#pymove3d.sudile.com/stationen/kc_objekt_rotation/rotation.html#eulerrotation
# todo: implement optional v?
def rotate( a=[0.0,0.0,0.0], obj_A=None):   
	if obj_A is None: 
		obj_A = bpy.context.object  
	bpy.ops.object.select_all(action = 'DESELECT')
	obj_A.select = True 
	deg = (pi/180)  # one degree is 2*pi/360
	obj_A.rotation_euler = ( a[0]*deg, a[1]*deg, a[2]*deg)
	return obj_A	
	
# OpenSCAD: scale(v = [x, y, z]) { ... }
def scale(v=[1.0,1.0,1.0], obj_A=None): 
	if obj_A is None: 
		obj_A = bpy.context.object  
	bpy.ops.object.select_all(action = 'DESELECT')
	obj_A.select = True
	# location needs to be scaled as well..
	l= obj_A.location   
	obj_A.location = [l[0]*v[0],l[1]*v[1],l[2]*v[2]]
	bpy.ops.transform.resize(value=v)
	bpy.ops.object.transform_apply(scale=True)  
	return obj_A
	
# OpenSCAD: resize(newsize=[30,60,10])  
def resize( newsize=(1.0,1.0,1.0), obj_A=None): 
	if obj_A is None: 
		obj_A = bpy.context.object  
	bpy.ops.object.select_all(action = 'DESELECT')
	# TODO: location!!
	obj_A.select = True 
	obj_A.dimensions=newsize	
	return obj_A	
	
def color( rgba=(1.0,1.0,1.0,1.0), obj_A=None): 
	if obj_A is None: 
		obj_A = bpy.context.object
	obj_A.color = rgba
	return obj_A		
									
def booleanOp(obj_A,obj_B, boolOp='DIFFERENCE'):
	scn = bpy.context.scene 
	#bpy.ops.object.select_all(action = 'DESELECT')
	#obj_A.select = True
	boo = obj_A.modifiers.new('MyBool', 'BOOLEAN')
	boo.object = obj_B
	boo.operation = boolOp  #  { 'DIFFERENCE', 'INTERSECT' , 'UNION' }
	# often forgotten: needs to be active!!
	scn.objects.active = obj_A
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier='MyBool')
	obj_A.name = boolOp+'('+obj_A.name+','+obj_B.name+')'   
	scn = bpy.context.scene 
	scn.objects.unlink(obj_B)
	return obj_A

def union(o1,*objs):
	res = o1
	for obj in objs:
		if obj != None:
  			res = booleanOp(res,obj, boolOp='UNION')
	return res
		
def difference(o1,o2,*objs):
	return booleanOp(o1,union(o2,*objs), boolOp='DIFFERENCE')

def intersection(o1,o2,*objs):
	return booleanOp(o1,union(o2,*objs), boolOp='INTERSECT')


# NO OpenSCAD thing, but nice alternative to union(). It preserves the objects and
# therefore different colors. However, need to rework subsequent modifiers?
# bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
def group(o1,*objs):
	res = o1
	o1.select = True
	bpy.context.scene.objects.active = o1   
	for obj in objs:
		if obj != None:
			obj.select = True
	bpy.ops.object.parent_set(type='OBJECT',keep_transform=True)
	return res


#   bpy.ops.mesh.convex_hull(delete_unused_vertices=True, use_existing_faces=True)
#   Enclose selected vertices in a convex polyhedron   
def hull(o1,o2=None,o3=None,o4=None,o5=None,o6=None,o7=None,o8=None,o9=None,o10=None):
  objA = union(o1,o2,o3,o4,o5,o6,o7,o8,o9,o10)
  #
  bpy.ops.object.mode_set(mode = 'EDIT')
  for v in objA.data.vertices:
	  v.select = True
  #for v in objB.data.vertices:
  # v.select = True
  #bpy.ops.mesh.convex_hull(delete_unused_vertices=True, use_existing_faces=True)   
  bpy.ops.mesh.convex_hull(use_existing_faces=True)  
  #bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action='SELECT')
  bpy.ops.mesh.remove_doubles()
  bpy.ops.object.mode_set(mode = 'OBJECT')
  objA.name= "hull(" + objA.name + ")"
  return objA   


# also an extra not present in OpenSCAD
def round_edges(width=0.1, segments=32, angle_limit=30, apply=False ,obj=None):
	scn = bpy.context.scene 
	#bpy.ops.object.select_all(action = 'DESELECT')
	#obj_A.select = True
	bev = obj.modifiers.new('MyBevel', 'BEVEL')
	bev.width = width
	bev.segments = segments
	bev.angle_limit = angle_limit
	# often forgotten: needs to be active!!
	scn.objects.active = obj
	if apply==True:
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier='MyBevel')
	obj.name = 'Bevel('+obj.name+')'   
	return obj
	
#################################################################
#################################################################   
	

#rotate( (90*pi/180,0,90*pi/180), cylinder(h=10,r=3) )

#cylinder(r=10,h=20)	
#cylinder(r=10,h=20, center=true)


# A few OpenSCAD like operations... need to substitute brackets
#  and need to change call order... implicit unions, etc.   
def OpenSCADtests():
	c0 = cube((5,10,4),center=true) 
	c1 = cube((5,10,4),center=true)
	translate(v=(10,10,10))
	color(blue)
	color(red,c0)
	scale((5,9,4),c0)
	# bpy.context.object.data.materials.append(mat)
	# set red...
	# bpy.context.object.color = (1,0,0,0)
	#   
	c0 = cube((12,12,4),center=true)
	c1 = cube((6,6,4),center=true)  
	color(green)
	difference(c0,c1)
	#intersection(c0,c1)
	#  already almost OpenSCAD like...
	difference (
			   color(red,cube((12,12,4),center=true)), 
			   cube((6,6,4),center=true)
			   )
	#
	union (
			   color(green, cube((12,12,4),center=true) ), 
			   color(blue, cube((6,6,9),center=false) )
			   )
	#
	color(green, cylinder(h=10,r=2))
	#
	scale( (0.5,0.5,0.5) ,rotate( (90,0,90) , hull ( union( sphere(r=4),
		#cylinder(r1=10,r2=20,h=20) 
		translate( (20,20,-10) , cylinder(r1=4,r2=8,h=20,center=true)   )
	))))
	#

#OpenSCADtests()

def Demo1():
	scale([3,3,3],
		union(
			rotate( [90,0,90], cylinder(h=10,r=3) )   
		,   rotate( [90,0,0], cylinder(h=10,r=3) )  
		,   rotate( [0,0,90], cylinder(h=10,r=3) )   
	  )
	) 

#Demo1()

# OpenJSCAD.org Logo :-)	  
def Demo2():  
	scale([10,10,10], 
	   translate([0,0,1.5] 
		 , group(   
			 color(purple, difference(
				 cube([3,3,3], center=true)
			   , sphere(r=2, center=true)
			 ))
		   , color(yellow, intersection(
				 sphere(r=1.3, center=true)
			   , cube([2.1,2.1,2.1], center=true)
		   ))	  
		 )
	 )
	)

#Demo2()

# OpenJSCAD.org Logo :-)	  
def Demo2b_tripleGrouping():  
	scale([10,10,10], 
	   translate([0,0,1.5] 
		 , group(   
			 color(purple, difference(
				 cube([3,3,3], center=true)
			   , sphere(r=2, center=true)
			 ))
		   , color(yellow, intersection(
				 sphere(r=1.3, center=true)
			   , cube([2.1,2.1,2.1], center=true)
		   ))	  
		   , cube([1,1,5])
		 )
	 )
	)
	  
#Demo2b_tripleGrouping()
	

# My Filament Holder (rough version without rounded corners)
def FilamentHolderSimple(D,A,b) :
   return union(
		difference(
			union(
			   cylinder(r1 = D/2, r2=D/2-1 , h = b, center = true)
			 , translate([0,0,-b/2+1] , cylinder(r1 = D/2+2, r2=D/2+1.5,h = 2, center = true))
			)  
		  , cylinder(r = D/2-3, h = b, center = true)
		) # difference
	,   difference(
			union(
				cylinder(r = A/2+4, h = b, center = true)
			  , cube([D-4,4,b],center=true) 
			  , cube([4,D-4,b],center=true) 
			)
		  , cylinder(r = A/2, h = b, center = true)
		)
	)

# Drumm inner diameter in mm
D = 52
# axis diameter
A = 7  #Actually 6mm
b=14 # holder height
FilamentHolderSimple(D,A,b)









###########################################################################################
##
## Playground: Below are some experimental script blocks. Potential reuse...  
##
###########################################################################################

# round_edges(width=0.1, segments=32, angle_limit=30, apply=False ,obj=None):
def round_edgesTEST(*pargs, **kwargs):
	width = kwargs.pop('width', 0.1)
	segments = kwargs.pop('segments', 16)
	angle_limit = kwargs.pop('angle_limit', 0.1)
	apply = kwargs.pop('apply', False)
	obj = kwargs.pop('obj', None)
	for a in pargs:	
		print(a)
	#
	if type(obj) is  bpy_types.Object:
		print(type(obj)) # bpy_types.Object		
	scn = bpy.context.scene 
	#bpy.ops.object.select_all(action = 'DESELECT')
	#obj_A.select = True
	bev = obj.modifiers.new('MyBevel', 'BEVEL')
	bev.width = width
	bev.segments = segments
	bev.angle_limit = angle_limit
	# often forgotten: needs to be active!!
	scn.objects.active = obj
	if apply==True:
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier='MyBevel')
	obj.name = 'Bevel('+obj.name+')'   
	return obj

# playing with arguments...
def round_edgesTEST2( *pargs):
	for a in pargs:	
		print(a)
	
#round_edges(obj=cube([15,4,1]) )
#round_edgesTEST2( 0.1,w=2, cube([15,4,3]) )



# testbed to emulate some minkowski like behavior
# see: http://blenderartists.org/forum/showthread.php?282214-door-frame-disaster-how-do-I-make-one&p=2310204&viewfull=1#post2310204
def minkowskiLike():
	translate([4,0,0] , cube([15,4,1]) )
	rotate([0,90,0] ,cylinder(r=3,h=1))

#minkowskiLike()

def dummy():
	difference( sphere(r=15),
	   #cylinder(r1=10,r2=20,h=20)  
	   translate( (3,3,3) , cylinder(r1=10,r2=20,h=20,center=true)	)
	)
	hull ( union (
		   color(green, cube((12,12,4),center=true) ), 
		   color(blue, cube((6,6,9),center=false) )
		   ))
		
#dummy()	
#cylinder(r=10,h=20)	
#cylinder(r=10,h=20, center=true)   

 
#Now in a for loop, we create the five objects like this (In the screenshot above, I used another method) Press ENTER-KEY twice after entering the command at the shell prompt.   
def Test1():
	for index in range(0, 5):
		#add_cylinder(location =(index*5, 0, index*5), radius=index+5 , depth=index*2+10 , vertices=64, layers=mylayers)
		#myC = bpy.data.objects['Cylinder']
		#myC.name='MyCylinder'+str(index)
		add_cube(location=(index*3, 5, index*4), layers=mylayers)	
		myC = bpy.data.objects['Cube']
		myC.name='MyCube'+str(index)
		# translate
		bpy.ops.transform.translate(value=(0, index*15, 0))
		# scale
		bpy.ops.transform.resize(value=(3+index*5, 3+index*5, 12))
		bpy.ops.object.transform_apply(scale=True)
		# set def material and enable object color (red)
		myC.data.materials.append(mat)
		# bpy.context.object.data.materials.append(mat)
		# bpy.context.object.color = (1,0,0,0)
		myC.color = (1,0,0,0)
	
#  MM: working code to set the native color of an object to display...
##   via a Material...
def Test3():
	mat=bpy.data.materials.new('useObjectColor')
	mat.use_object_color=1
	bpy.context.object.data.materials.append(mat)
	# set red...
	bpy.context.object.color = (1,0,0,0)

  ###bpy.ops.mesh.select_all(action='TOGGLE') #maybe needed?
  #cd.vertices[0].select = True   
  #cd.vertices[5].select = True
  #tmp = [el.select for el in cd.vertices]
  ##c.update(bpy.context.scene)
  #for el in cd.vertices:
  # print (el.select)
  #   bpy.ops.mesh.convex_hull(delete_unused_vertices=True, use_existing_faces=True)

############################################################
# HUGE todo: auto convert and exec .scad files :-)
# from:
# http://timhatch.com/projects/pybraces/#example
current_depth = 0
indent_width = 4

def braces_decode(input, errors='strict'):	
	if not input: return (u'', 0)
	length = len(input)
	# Deal with chunked reading, where we don't get
	# data containing a complete line of source
	if not input.endswith('\n'):
		length = input.rfind('\n') + 1
	input = input[:length]
	#
	acc = []
	global indent_width, current_depth
	lines = input.split('\n')
	for l in [x.strip().replace('++', '+=1') for x in lines]:
		if l.endswith(';'):
			l = l[:-1]

		if l.endswith('{'):
			acc.append(' ' * current_depth + l[:-1].strip() + ':')
			current_depth += indent_width
		elif l.endswith('}'):
			acc.append(' ' * current_depth + l[:-1].strip())
			current_depth -= indent_width
		else:
			acc.append(' ' * current_depth + l)
	return (u'\n'.join(acc)+'\n', length)


def convertOpenSCAD():
	filenameSCAD = "O:/BlenderStuff/demo.scad"
	filenameConverted = "O:/BlenderStuff/demo.scad.py"
	##clearAllObjects()
	txt = open(filenameSCAD).read()
	#print (txt)
	decodedTxt = braces_decode(txt)  
	#print (decodedTxt)
	myFile = open(filenameConverted, 'w')
	myFile.write(decodedTxt[0])
	myFile.close()
	#exec(compile( decodedTxt, filename, 'exec'))

#convertOpenSCAD()
