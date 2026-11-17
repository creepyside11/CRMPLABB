"""Generate the original CRMPLAB prototype town and individual GLB models. Blender 3.6+."""
import bpy, math, os, random
from mathutils import Vector
random.seed(17)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'assets', 'city')
os.makedirs(OUT, exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

def mat(name, color, metallic=0.0, roughness=.8):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*color,1); p.inputs['Roughness'].default_value=roughness; p.inputs['Metallic'].default_value=metallic
    return m
cream=mat('Warm plaster',(.69,.63,.52)); dark=mat('Charcoal roof',(.12,.15,.19)); glass=mat('Blue glass',(.20,.38,.46),.15,.25); trim=mat('Light concrete',(.74,.75,.71)); brick=mat('Terracotta',(.48,.30,.24)); asphalt=mat('Asphalt',(.115,.13,.15)); marking=mat('Road markings',(.88,.85,.70)); grass=mat('Grass',(.28,.39,.24)); green=mat('Trees',(.17,.30,.17)); trunk=mat('Tree trunks',(.28,.20,.13)); red=mat('Platform canopy',(.38,.15,.16)); blue=mat('Bus stop',(.16,.27,.39)); pavement=mat('Paving',(.49,.49,.46)); yellow=mat('Sign lettering',(.96,.80,.38))
collections={}
for name in ['Station','Road','Town']:
    c=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); collections[name]=c

def place(obj, group, material):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    collections[group].objects.link(obj); obj.data.materials.append(material); return obj

def box(name, pos, size, material, group='Town'):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos); o=bpy.context.object; o.name=name; o.dimensions=size; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); return place(o,group,material)

def tree(x,y):
    box('Tree trunk',(x,y,1),(0.35,.35,2),trunk)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(x,y,3)); o=bpy.context.object; o.name='Tree crown'; o.scale=(1.35,1.35,1.8); place(o,'Town',green)

def station():
    box('Station main hall',(0,0,3),(26,11,6),cream,'Station')
    box('Left wing',(-17,0,2.4),(8,9,4.8),cream,'Station'); box('Right wing',(17,0,2.4),(8,9,4.8),cream,'Station')
    box('Main roof',(0,0,6.3),(27,12,0.6),dark,'Station')
    for x in [-17,17]: box('Wing roof',(x,0,5.0),(8.5,9.5,.5),dark,'Station')
    box('Entrance facade',(0,-5.65,3.0),(9,.3,5.4),trim,'Station')
    box('Entrance glass',(0,-5.84,2.1),(4.8,.12,4),glass,'Station')
    for x in [-1.65,0,1.65]: box('Door frame',(x,-5.94,2.0),(.12,.12,4),trim,'Station')
    for x in [-10,-7,7,10]:
        box('Front window',(x,-5.57,3.25),(2.0,.14,2.7),glass,'Station')
        box('Window sill',(x,-5.67,1.85),(2.3,.35,.18),trim,'Station')
    for x in [-18.5,-15.5,15.5,18.5]: box('Wing window',(x,-4.57,2.5),(1.7,.14,2.2),glass,'Station')
    box('Entrance canopy',(0,-7.15,4.6),(8,2.8,.28),red,'Station')
    for x in [-3.5,3.5]: box('Canopy column',(x,-8.2,2.25),(.25,.25,4.5),trim,'Station')
    box('Station sign',(0,-5.85,5.15),(7,.2,.65),dark,'Station')
    # Graphic bars avoid nonportable fonts while marking a space for a future sign texture.
    for x in [-2.2,-1.3,-.4,.5,1.4,2.3]: box('Sign detail',(x,-5.98,5.15),(.5,.08,.15),yellow,'Station')
    box('Station steps',(0,-6.8,.15),(8,2.4,.3),pavement,'Station')

def road():
    # One 20x12 metre tile. Road surface top is z=0.
    box('Road surface',(0,0,-.15),(20,12,.3),asphalt,'Road')
    for x in [-7.5,-2.5,2.5,7.5]: box('Center marking',(x,0,.008),(2.5,.16,.016),marking,'Road')
    for y in [-5.4,5.4]: box('Edge marking',(0,y,.008),(20,.12,.016),marking,'Road')
    for y in [-6.65,6.65]: box('Sidewalk',(0,y,.10),(20,1.3,.2),pavement,'Road')
station(); road()
# Arrange the 3D town as an independent editable prototype, not GTA map objects.
for o in collections['Station'].objects: o.location += Vector((0,20,0))
for o in collections['Road'].objects: o.location += Vector((0,-3,0))
# Additional road tiles, using the same dimensions; junction is a simple cross.
for x in [-40,-20,20,40]:
    box('Road segment',(x,-3,-.15),(20,12,.3),asphalt)
    for dx in [-7.5,-2.5,2.5,7.5]: box('Road dash',(x+dx,-3,.008),(2.5,.16,.016),marking)
    for y in [-9.65,3.65]: box('Sidewalk',(x,y,.1),(20,1.3,.2),pavement)
box('Crossroad',(40,-3,-.12),(12,12,.28),asphalt)
for y in [-19,13,33]:
    box('Side street',(40,y,-.15),(12,20,.3),asphalt)
    for dy in [-7.5,-2.5,2.5,7.5]: box('Side street dash',(40,y+dy,.008),(.16,2.5,.016),marking)
box('Ground',(0,5,-.42),(130,110,.5),grass)
box('Station square',(0,8,-.10),(42,11,.2),pavement)
# Apartment blocks in a consistent, deliberately simple style.
for x in [-43,-25,6,25]:
    box('Apartment block',(x,-24,5),(14,10,10),brick)
    box('Apartment roof',(x,-24,10.2),(14.5,10.5,.4),dark)
    for dx in [-5,-2,2,5]:
        for z in [2,4.5,7]: box('Apartment window',(x+dx,-18.94,z),(1.5,.14,1.5),glass)
    box('Apartment entrance',(x,-18.86,1.4),(1.5,.18,2.8),dark)
box('Shop',(-39,22,2.4),(13,9,4.8),cream)
box('Shop roof',(-39,22,4.9),(14,10,.4),red)
box('Shop window',(-39,17.43,2.3),(8,.15,2.5),glass)
box('Bus shelter',(19,5,2.3),(5,1.5,.25),blue)
for x in [16.8,21.2]: box('Bus shelter post',(x,5,1.15),(.14,.14,2.3),blue)
box('Shelter back',(19,5.65,1.25),(5,.1,2.0),glass)
for x,y in [(-52,13),(-50,37),(-28,40),(22,41),(33,30),(-52,-37),(-16,-37),(10,-37),(30,-37),(54,24),(54,-19)]: tree(x,y)
# Save each model in local origin for reuse.
def export_group(name, filename, offset):
    bpy.ops.object.select_all(action='DESELECT')
    obs=list(collections[name].objects)
    for o in obs: o.location -= Vector(offset); o.select_set(True)
    bpy.context.view_layer.objects.active=obs[0]
    bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,filename),export_format='GLB',use_selection=True)
    for o in obs: o.location += Vector(offset)
export_group('Station','station.glb',(0,20,0))
export_group('Road','road_tile.glb',(0,-3,0))
bpy.ops.object.select_all(action='DESELECT')
for c in collections.values():
    for o in c.objects: o.select_set(True)
bpy.context.view_layer.objects.active=collections['Station'].objects[0]
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'town.glb'),export_format='GLB',use_selection=True)
# Camera and lights are only for the overview, excluded from the exported GLBs.
bpy.ops.object.camera_add(location=(96,-120,98)); cam=bpy.context.object; cam.rotation_euler=(Vector((0,4,0))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.type='ORTHO'; cam.data.ortho_scale=140; bpy.context.scene.camera=cam
bpy.ops.object.light_add(type='AREA',location=(-20,-40,90)); bpy.context.object.data.energy=2600; bpy.context.object.data.shape='DISK'; bpy.context.object.data.size=70
bpy.ops.object.light_add(type='SUN', location=(0,0,50)); bpy.context.object.rotation_euler=(0.4,-0.5,-0.5); bpy.context.object.data.energy=2.0
scene=bpy.context.scene; scene.world.use_nodes=True; scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=0.65; scene.render.engine='CYCLES'; scene.cycles.samples=16; scene.cycles.use_denoising=False; scene.world.color=(.32,.32,.32); scene.render.resolution_x=1500; scene.render.resolution_y=1050; scene.render.resolution_percentage=100
scene.view_settings.view_transform='Standard'; scene.render.image_settings.file_format='PNG'; scene.render.filepath=os.path.join(OUT,'town_preview.png'); bpy.ops.render.render(write_still=True)
