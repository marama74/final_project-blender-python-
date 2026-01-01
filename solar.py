import bpy
import math
import random

# ------------------- CONFIG -------------------
ANIMATION_FRAMES = 150
PLANET_KEYFRAME_INTERVAL = 5
CAMERA_KEYFRAME_INTERVAL = 5
STAR_COUNT = 20

# ------------------- CLEAR SCENE -------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ------------------- MATERIALS -------------------
def emissive_material(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*color, 1)
    emission.inputs["Strength"].default_value = strength
    mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    return mat

def planet_material(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = 0.6
    return mat

# ------------------- ORBIT RING -------------------
def create_orbit(radius):
    bpy.ops.curve.primitive_bezier_circle_add(radius=radius, location=(0, 0, 0))
    orbit = bpy.context.active_object
    orbit.data.bevel_depth = 0.08
    orbit.data.bevel_resolution = 8
    orbit.data.materials.append(
        emissive_material("Orbit_Mat", (0.3, 0.6, 1.0), 0.4)
    )
    # Orbit stays in place - NOT parented to anything

# ------------------- TEXT LABEL -------------------
def add_label(text, parent):
    bpy.ops.object.text_add(location=(0, 0, 2))
    label = bpy.context.active_object
    label.data.body = text
    label.data.size = 0.7
    label.rotation_euler = (math.radians(90), 0, 0)
    label.parent = parent

# ------------------- SATURN RINGS -------------------
def create_saturn_rings(parent):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=3.2,
        minor_radius=0.15,
        rotation=(math.radians(90), 0, 0)
    )
    rings = bpy.context.active_object
    rings.parent = parent
    rings.data.materials.append(
        planet_material("Saturn_Rings_Mat", (0.8, 0.7, 0.5))
    )

# ------------------- SUN (STATIONARY) -------------------
bpy.ops.mesh.primitive_uv_sphere_add(radius=3, location=(0, 0, 0))
sun = bpy.context.active_object
sun.name = "Sun"
sun.data.materials.append(
    emissive_material("Sun_Mat", (1.0, 0.9, 0.2), 10)
)

# ------------------- PLANET DATA -------------------
planet_data = [
    ("Mercury", 0.4, (0.6, 0.6, 0.6), 5, 0.9),
    ("Venus", 0.9, (0.9, 0.7, 0.3), 7, 0.8),
    ("Earth", 1.0, (0.2, 0.5, 1.0), 10, 0.7),
    ("Mars", 0.5, (0.9, 0.3, 0.2), 13, 0.65),
    ("Jupiter", 2.2, (0.8, 0.6, 0.4), 18, 0.55),
    ("Saturn", 1.9, (0.9, 0.8, 0.5), 24, 0.5),
    ("Uranus", 1.4, (0.4, 0.8, 0.9), 30, 0.45),
    ("Neptune", 1.4, (0.3, 0.4, 0.9), 36, 0.4),
    ("Pluto", 0.3, (0.7, 0.6, 0.5), 42, 0.35),
]

# ------------------- CREATE PLANETS -------------------
for name, size, color, radius, speed in planet_data:

    # Create orbit ring (stays stationary)
    create_orbit(radius)

    # Create empty for planet rotation (NOT parented to sun, stays at origin)
    bpy.ops.object.empty_add(location=(0, 0, 0))
    empty = bpy.context.active_object
    empty.name = f"{name}_Orbit"

    # Create planet
    bpy.ops.mesh.primitive_uv_sphere_add(radius=size, location=(radius, 0, 0))
    planet = bpy.context.active_object
    planet.name = name
    planet.parent = empty
    planet.data.materials.append(
        planet_material(f"{name}_Mat", color)
    )

    add_label(name, planet)

    if name == "Saturn":
        create_saturn_rings(planet)

    # Animate planet orbit around sun
    for frame in range(0, ANIMATION_FRAMES + 1, PLANET_KEYFRAME_INTERVAL):
        angle = speed * 2 * math.pi * frame / ANIMATION_FRAMES
        empty.rotation_euler = (0, 0, angle)
        empty.keyframe_insert("rotation_euler", frame=frame)

# ------------------- STARS (WITH TWINKLING) -------------------
for i in range(STAR_COUNT):
    x, y, z = random.uniform(-80,80), random.uniform(-80,80), random.uniform(-40,40)
    if math.sqrt(x*x + y*y) < 50:
        continue
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(x, y, z))
    star = bpy.context.active_object
    
    # Create material with animated emission strength
    base_strength = random.uniform(2, 4)
    mat = emissive_material(f"Star_Mat_{i}", (1, 1, 1), base_strength)
    star.data.materials.append(mat)
    
    # Animate star twinkling (emission strength varies)
    emission_node = mat.node_tree.nodes["Emission"]
    for frame in range(0, ANIMATION_FRAMES + 1, 10):
        # Random strength variation for twinkling effect
        strength = base_strength + random.uniform(-0.5, 0.5)
        emission_node.inputs["Strength"].default_value = strength
        emission_node.inputs["Strength"].keyframe_insert("default_value", frame=frame)

# ------------------- CAMERA -------------------
bpy.ops.object.camera_add(location=(0, -60, 30))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(55), 0, 0)
bpy.context.scene.camera = camera

# Animate camera orbiting around the solar system
for frame in range(0, ANIMATION_FRAMES + 1, CAMERA_KEYFRAME_INTERVAL):
    angle = 2 * math.pi * frame / ANIMATION_FRAMES
    camera.location = (-60 * math.sin(angle), -60 * math.cos(angle), 30)
    camera.keyframe_insert("location", frame=frame)
    camera.rotation_euler = (math.radians(55), 0, angle)
    camera.keyframe_insert("rotation_euler", frame=frame)

# ------------------- SCENE SETTINGS -------------------
scene = bpy.context.scene
scene.frame_end = ANIMATION_FRAMES
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.render.fps = 12
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0.03, 1)

print(" COMPLETE SOLAR SYSTEM CREATED (150 frames)")
print("   - Sun: Stationary at center")
print("   - Orbit rings: Fixed in place")
print("   - Planets: Revolving around sun along orbit rings")
print("   - Stars: Twinkling in place")
print("   - Camera: Rotating around the scene")
