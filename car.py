import bpy
import random
import math
import mathutils
import colorsys

# --- 1. Scene Setup ---
def clean_scene():
    """Cleans the scene safely."""
    if bpy.context.active_object and bpy.context.active_object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT') 
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Lighting: Sun (Bright and angled)
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    bpy.context.object.data.energy = 4.5 
    bpy.context.object.data.angle = 0.5 
    
    # Camera: Adjusted to frame the larger tree
    bpy.ops.object.camera_add(location=(0, -28, 10), rotation=(math.radians(75), 0, 0))

def get_random_deep_color():
    """Generates deep, rich colors."""
    hue = random.random()
    saturation = 1.0                
    value = random.uniform(0.5, 0.9) 
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return (r, g, b, 1)

def create_material(name, color, roughness=0.8, clearcoat=0):
    """Creates a material (Version Safe)."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = roughness
    
    if "Coat Weight" in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = clearcoat
    elif "Clearcoat" in bsdf.inputs:
        bsdf.inputs['Clearcoat'].default_value = clearcoat
    return mat

# --- 2. Realistic Grass ---
def create_grassy_ground(size=40):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0,0,0))
    ground = bpy.context.object
    ground.name = "Grassy_Ground"
    
    dirt_mat = create_material("DirtMat", (0.05, 0.03, 0.01, 1), roughness=0.9)
    ground.data.materials.append(dirt_mat)
    
    grass_mat = create_material("GrassMat", (0.02, 0.25, 0.05, 1), roughness=0.4, clearcoat=0.1)
    ground.data.materials.append(grass_mat)
    
    bpy.ops.object.particle_system_add()
    psys = ground.particle_systems.active
    pset = psys.settings
    
    pset.type = 'HAIR'
    pset.count = 3000             
    pset.hair_length = 0.6        
    pset.hair_step = 3            
    pset.material = 2 
    
    pset.use_advanced_hair = True
    pset.brownian_factor = 0.1   
    
    pset.child_type = 'INTERPOLATED'
    pset.rendered_child_count = 60 
    pset.clump_factor = 0.6
    pset.clump_shape = -0.5       

# --- 3. Realistic Fruit Tree (UPDATED) ---
class RealisticTree:
    def __init__(self):
        self.wood_mat = create_material("WoodMat", (0.05, 0.03, 0.02, 1), roughness=0.9)
        
        # CHANGED: Leaf color is now Autumn Orange/Red to contrast with grass
        self.leaf_mat = create_material("LeafMat", (0.8, 0.2, 0.05, 1), roughness=0.5, clearcoat=0.2)
        
        # NEW: Fruit Material (Bright Yellow for Mangoes)
        self.fruit_mat = create_material("FruitMat", (1.0, 0.8, 0.1, 1), roughness=0.3, clearcoat=0.5)
        
        self.all_branches = []

    def create_branch(self, start_loc, direction, length, radius, level, parent_obj):
        if level == 0:
            # Add foliage and Fruits at the tips
            self.create_foliage(start_loc, parent_obj)
            return

        # Create Cylinder for this branch segment
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radius, 
            depth=length, 
            location=(0, 0, length / 2) 
        )
        branch = bpy.context.object
        branch.name = f"Tree_Lvl{level}"
        branch.data.materials.append(self.wood_mat)
        
        up_vec = mathutils.Vector((0, 0, 1))
        rot_quat = up_vec.rotation_difference(direction)
        branch.rotation_euler = rot_quat.to_euler()
        branch.location = start_loc
        
        if parent_obj:
            branch.parent = parent_obj
            branch.matrix_world.translation = start_loc
        
        self.all_branches.append(branch)

        # Recursive splitting
        tip_loc = start_loc + (direction * length)
        num_branches = random.randint(2, 3)
        for i in range(num_branches):
            spread = 0.5 
            rand_vec = mathutils.Vector((
                random.uniform(-spread, spread),
                random.uniform(-spread, spread),
                random.uniform(0.2, 1.0)
            ))
            new_dir = (direction + rand_vec).normalized()
            
            self.create_branch(
                start_loc=tip_loc,
                direction=new_dir,
                length=length * 0.7, 
                radius=radius * 0.6, 
                level=level - 1,
                parent_obj=branch
            )

    def create_foliage(self, location, parent):
        """Creates clusters of leaves and occasionally adds a fruit."""
        
        # 1. Add Leaves
        for i in range(15): 
            offset = mathutils.Vector((
                random.uniform(-0.6, 0.6),
                random.uniform(-0.6, 0.6),
                random.uniform(-0.6, 0.6)
            ))
            
            bpy.ops.mesh.primitive_plane_add(size=0.35, location=(0,0,0))
            leaf = bpy.context.object
            leaf.data.materials.append(self.leaf_mat)
            leaf.parent = parent
            leaf.matrix_world.translation = location + offset
            leaf.rotation_euler = (
                random.uniform(0, 3.14),
                random.uniform(0, 3.14),
                random.uniform(0, 3.14)
            )

        # 2. Add Fruit (Mango) - 30% chance per branch tip
        if random.random() < 0.3:
            # Create a mango shape (Elongated sphere)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(0,0,0))
            fruit = bpy.context.object
            fruit.name = "Mango"
            fruit.data.materials.append(self.fruit_mat)
            
            # Stretch it to look like a mango
            fruit.scale = (1.0, 0.8, 1.2)
            
            fruit.parent = parent
            # Hang it slightly below the branch tip
            fruit_offset = mathutils.Vector((0, 0, -0.3))
            fruit.matrix_world.translation = location + fruit_offset

    def generate(self):
        root_start = mathutils.Vector((0, 0, 0))
        root_dir = mathutils.Vector((0, 0, 1)) 
        self.create_branch(root_start, root_dir, length=2.5, radius=0.3, level=4, parent_obj=None)
        self.root = self.all_branches[0]
        self.root.name = "Tree_Root"

    def animate(self):
        if not hasattr(self, 'root'): return
        for f in range(1, 251, 5):
            angle = math.sin(f * 0.04) * 0.03 
            self.root.rotation_euler.x = angle + self.root.rotation_euler.x 
            self.root.keyframe_insert("rotation_euler", frame=f)

# --- 4. Flowers & Butterflies ---
class ProceduralFlower:
    def __init__(self, index):
        self.index = index
        self.stem_obj = None
        self.height = random.uniform(1.5, 2.5)
        self.petal_count = random.randint(6, 12)

    def generate(self, location_range=12, avoid_radius=4):
        while True:
            x = random.uniform(-location_range, location_range)
            y = random.uniform(-location_range, location_range)
            if math.sqrt(x**2 + y**2) > avoid_radius: break
        
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=self.height, location=(x, y, self.height/2))
        self.stem_obj = bpy.context.object
        stem_mat = create_material(f"StemMat_{self.index}", (0.0, 0.3, 0.0, 1), roughness=0.3)
        self.stem_obj.data.materials.append(stem_mat)

        for i in range(self.petal_count):
            angle = (math.pi * 2 * i) / self.petal_count
            unique_color = get_random_deep_color()
            petal_mat = create_material(f"PetalMat_{self.index}_{i}", unique_color)

            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=(0,0,0))
            petal = bpy.context.object
            petal.scale = (1, 0.3, 1) 
            petal.data.materials.append(petal_mat)
            petal.parent = self.stem_obj
            petal.location = (math.cos(angle)*0.4, math.sin(angle)*0.4, self.height/2)
            petal.rotation_euler = (0, 0, angle)

    def animate(self):
        if not self.stem_obj: return
        self.stem_obj.scale = (0,0,0)
        self.stem_obj.keyframe_insert("scale", frame=1)
        self.stem_obj.scale = (1,1,1)
        self.stem_obj.keyframe_insert("scale", frame=50)
        
        for f in range(50, 251, 10):
            phase = random.uniform(0, 10)
            self.stem_obj.rotation_euler.x = math.sin(f*0.1 + phase) * 0.1
            self.stem_obj.keyframe_insert("rotation_euler", frame=f)

class Butterfly:
    def __init__(self, index):
        self.index = index
        self.body = None
        self.l_wings = [] 
        self.r_wings = []
        
    def create_wing_panel(self, mat, location, scale, rotation):
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0,0,0))
        wing = bpy.context.object
        wing.data.materials.append(mat)
        wing.scale = scale 
        wing.parent = self.body
        wing.location = location
        wing.rotation_euler = rotation
        return wing

    def generate(self, location_range=10):
        start_x = random.uniform(-location_range, location_range)
        start_y = random.uniform(-location_range, location_range)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.3, location=(start_x, start_y, 3))
        self.body = bpy.context.object
        self.body.rotation_euler.x = math.radians(90)
        body_mat = create_material(f"BugBody_{self.index}", (0.05, 0.05, 0.05, 1))
        self.body.data.materials.append(body_mat)
        
        wing_color = get_random_deep_color()
        wing_mat = create_material(f"BugWing_{self.index}", wing_color, roughness=0.2)
        
        lw_top = self.create_wing_panel(wing_mat, (-0.25, 0.1, 0.05), (0.3, 0.4, 1), (0, math.radians(20), math.radians(20)))
        lw_bot = self.create_wing_panel(wing_mat, (-0.15, -0.2, 0.0), (0.25, 0.3, 1), (0, math.radians(10), math.radians(-30)))
        self.l_wings = [lw_top, lw_bot]
        
        rw_top = self.create_wing_panel(wing_mat, (0.25, 0.1, 0.05), (0.3, 0.4, 1), (0, math.radians(-20), math.radians(-20)))
        rw_bot = self.create_wing_panel(wing_mat, (0.15, -0.2, 0.0), (0.25, 0.3, 1), (0, math.radians(-10), math.radians(30)))
        self.r_wings = [rw_top, rw_bot]

    def animate(self):
        if not self.body: return
        for f in range(1, 251, 3):
            for w in self.l_wings:
                w.rotation_euler.y = math.radians(-60)
                w.keyframe_insert("rotation_euler", frame=f)
                w.rotation_euler.y = math.radians(10)
                w.keyframe_insert("rotation_euler", frame=f+2)
            for w in self.r_wings:
                w.rotation_euler.y = math.radians(60)
                w.keyframe_insert("rotation_euler", frame=f)
                w.rotation_euler.y = math.radians(-10)
                w.keyframe_insert("rotation_euler", frame=f+2)
        
        start_loc = self.body.location.copy()
        speed_x = random.uniform(-0.04, 0.04)
        speed_y = random.uniform(-0.04, 0.04)
        for f in range(1, 251, 10):
            time = f * 0.1
            new_x = start_loc.x + (speed_x * f) + math.sin(time) * 0.5 
            new_y = start_loc.y + (speed_y * f) + math.cos(time) * 0.5
            self.body.location = (new_x, new_y, start_loc.z + math.sin(f * 0.3) * 0.2)
            self.body.keyframe_insert("location", frame=f)
            self.body.rotation_euler.z = math.cos(time) * 0.5
            self.body.keyframe_insert("rotation_euler", frame=f)

# --- 5. Main Execution ---
def setup_render():
    scene = bpy.context.scene
    scene.render.filepath = "//Mango_Tree_Scene"
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.frame_end = 250

def generate_scene(flower_count=20, butterfly_count=8):
    print("--- Generating Autumn Mango Tree Scene ---")
    clean_scene()
    setup_render()
    
    create_grassy_ground(size=40)
    
    # Generate Tree with Autumn Leaves and Mangoes
    tree = RealisticTree()
    tree.generate()
    tree.animate()
    
    for i in range(flower_count):
        flower = ProceduralFlower(i)
        flower.generate(avoid_radius=5)
        flower.animate()

    for i in range(butterfly_count):
        bug = Butterfly(i)
        bug.generate()
        bug.animate()
        
    bpy.context.scene.frame_set(1)

if __name__ == "__main__":
    generate_scene()