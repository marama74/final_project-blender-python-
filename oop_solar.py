import bpy
import math
import random
from typing import Tuple, List, Optional


class MaterialFactory:
    """Factory class for creating various Blender materials."""
    
    @staticmethod
    def create_emissive(name: str, color: Tuple[float, float, float], 
                       strength: float) -> bpy.types.Material:
        """Create an emissive material for glowing objects."""
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
    
    @staticmethod
    def create_planet_material(name: str, color: Tuple[float, float, float], 
                              roughness: float = 0.6) -> bpy.types.Material:
        """Create a material for planet surfaces."""
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*color, 1)
        bsdf.inputs["Roughness"].default_value = roughness
        return mat


class CelestialBody:
    """Base class for all celestial objects."""
    
    def __init__(self, name: str, size: float, color: Tuple[float, float, float], 
                 location: Tuple[float, float, float] = (0, 0, 0)):
        self.name = name
        self.size = size
        self.color = color
        self.location = location
        self.blender_object: Optional[bpy.types.Object] = None
    
    def create(self):
        """Create the Blender object. To be implemented by subclasses."""
        raise NotImplementedError
    
    def add_label(self, text: str, offset_z: float = 2.0):
        """Add a text label above the celestial body."""
        if not self.blender_object:
            return
        
        bpy.ops.object.text_add(location=(0, 0, offset_z))
        label = bpy.context.active_object
        label.data.body = text
        label.data.size = 0.7
        label.rotation_euler = (math.radians(90), 0, 0)
        label.parent = self.blender_object


class Star(CelestialBody):
    """Represents the central star (Sun)."""
    
    def __init__(self, name: str = "Sun", size: float = 3.0, 
                 emission_strength: float = 10.0):
        super().__init__(name, size, (1.0, 0.9, 0.2))
        self.emission_strength = emission_strength
    
    def create(self):
        """Create the sun at the center of the solar system."""
        bpy.ops.mesh.primitive_uv_sphere_add(radius=self.size, location=self.location)
        self.blender_object = bpy.context.active_object
        self.blender_object.name = self.name
        
        mat = MaterialFactory.create_emissive(
            f"{self.name}_Mat", self.color, self.emission_strength
        )
        self.blender_object.data.materials.append(mat)


class Planet(CelestialBody):
    """Represents a planet orbiting the star."""
    
    def __init__(self, name: str, size: float, color: Tuple[float, float, float],
                 orbit_radius: float, orbit_speed: float):
        super().__init__(name, size, color)
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.orbit_ring: Optional[bpy.types.Object] = None
    
    def create(self):
        """Create the planet with its orbit system."""
        # Create orbit ring (stationary)
        self._create_orbit_ring()
        
        # Create planet sphere directly at starting position
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=self.size, 
            location=(self.orbit_radius, 0, 0)
        )
        self.blender_object = bpy.context.active_object
        self.blender_object.name = self.name
        
        # Apply material
        mat = MaterialFactory.create_planet_material(f"{self.name}_Mat", self.color)
        self.blender_object.data.materials.append(mat)
        
        # Add label
        self.add_label(self.name)
    
    def _create_orbit_ring(self):
        """Create a visual orbit ring."""
        bpy.ops.curve.primitive_bezier_circle_add(
            radius=self.orbit_radius, location=(0, 0, 0)
        )
        self.orbit_ring = bpy.context.active_object
        self.orbit_ring.data.bevel_depth = 0.08
        self.orbit_ring.data.bevel_resolution = 8
        
        mat = MaterialFactory.create_emissive("Orbit_Mat", (0.3, 0.6, 1.0), 0.4)
        self.orbit_ring.data.materials.append(mat)
    
    def animate_orbit(self, total_frames: int, keyframe_interval: int = 5):
        """Animate the planet moving along its orbit path."""
        if not self.blender_object:
            return
        
        for frame in range(0, total_frames + 1, keyframe_interval):
            angle = self.orbit_speed * 2 * math.pi * frame / total_frames
            
            # Calculate position on orbit circle
            x = self.orbit_radius * math.cos(angle)
            y = self.orbit_radius * math.sin(angle)
            
            self.blender_object.location = (x, y, 0)
            self.blender_object.keyframe_insert("location", frame=frame)


class RingedPlanet(Planet):
    """Represents a planet with rings (like Saturn)."""
    
    def __init__(self, name: str, size: float, color: Tuple[float, float, float],
                 orbit_radius: float, orbit_speed: float,
                 ring_major_radius: float = 3.2, ring_minor_radius: float = 0.15):
        super().__init__(name, size, color, orbit_radius, orbit_speed)
        self.ring_major_radius = ring_major_radius
        self.ring_minor_radius = ring_minor_radius
        self.rings: Optional[bpy.types.Object] = None
    
    def create(self):
        """Create the planet and add rings."""
        super().create()
        self._create_rings()
    
    def _create_rings(self):
        """Create the planet's ring system."""
        if not self.blender_object:
            return
        
        bpy.ops.mesh.primitive_torus_add(
            major_radius=self.ring_major_radius,
            minor_radius=self.ring_minor_radius,
            rotation=(math.radians(90), 0, 0)
        )
        self.rings = bpy.context.active_object
        self.rings.parent = self.blender_object
        
        mat = MaterialFactory.create_planet_material(
            f"{self.name}_Rings_Mat", (0.8, 0.7, 0.5)
        )
        self.rings.data.materials.append(mat)


class BackgroundStar:
    """Represents a distant twinkling star."""
    
    def __init__(self, location: Tuple[float, float, float], 
                 size: float = 0.12, base_strength: float = 3.0):
        self.location = location
        self.size = size
        self.base_strength = base_strength
        self.blender_object: Optional[bpy.types.Object] = None
        self.material: Optional[bpy.types.Material] = None
    
    def create(self):
        """Create the star sphere."""
        bpy.ops.mesh.primitive_uv_sphere_add(radius=self.size, location=self.location)
        self.blender_object = bpy.context.active_object
        
        # Create material
        self.material = MaterialFactory.create_emissive(
            f"Star_Mat_{id(self)}", (1, 1, 1), self.base_strength
        )
        self.blender_object.data.materials.append(self.material)
    
    def animate_twinkle(self, total_frames: int, interval: int = 10):
        """Animate the star's twinkling effect."""
        if not self.material:
            return
        
        emission_node = self.material.node_tree.nodes["Emission"]
        for frame in range(0, total_frames + 1, interval):
            strength = self.base_strength + random.uniform(-0.5, 0.5)
            emission_node.inputs["Strength"].default_value = strength
            emission_node.inputs["Strength"].keyframe_insert("default_value", frame=frame)


class OrbitingCamera:
    """Camera that orbits around the scene."""
    
    def __init__(self, distance: float = 60.0, height: float = 30.0, 
                 tilt_angle: float = 55.0):
        self.distance = distance
        self.height = height
        self.tilt_angle = tilt_angle
        self.blender_object: Optional[bpy.types.Object] = None
    
    def create(self):
        """Create the camera."""
        initial_x = 0
        initial_y = -self.distance
        
        bpy.ops.object.camera_add(location=(initial_x, initial_y, self.height))
        self.blender_object = bpy.context.active_object
        self.blender_object.rotation_euler = (math.radians(self.tilt_angle), 0, 0)
        bpy.context.scene.camera = self.blender_object
    
    def animate_orbit(self, total_frames: int, keyframe_interval: int = 5):
        """Animate the camera orbiting around the scene."""
        if not self.blender_object:
            return
        
        for frame in range(0, total_frames + 1, keyframe_interval):
            angle = 2 * math.pi * frame / total_frames
            x = -self.distance * math.sin(angle)
            y = -self.distance * math.cos(angle)
            
            self.blender_object.location = (x, y, self.height)
            self.blender_object.keyframe_insert("location", frame=frame)
            
            self.blender_object.rotation_euler = (math.radians(self.tilt_angle), 0, angle)
            self.blender_object.keyframe_insert("rotation_euler", frame=frame)


class SolarSystem:
    """Main class that manages the entire solar system scene."""
    
    def __init__(self, animation_frames: int = 150):
        self.animation_frames = animation_frames
        self.sun: Optional[Star] = None
        self.planets: List[Planet] = []
        self.background_stars: List[BackgroundStar] = []
        self.camera: Optional[OrbitingCamera] = None
    
    def clear_scene(self):
        """Remove all objects from the scene."""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
    
    def create_sun(self):
        """Create the central star."""
        self.sun = Star()
        self.sun.create()
    
    def add_planet(self, planet: Planet):
        """Add a planet to the solar system."""
        planet.create()
        planet.animate_orbit(self.animation_frames)
        self.planets.append(planet)
    
    def generate_background_stars(self, count: int = 20, 
                                  min_distance: float = 50.0):
        """Procedurally generate distant stars."""
        for _ in range(count):
            # Generate random position
            x = random.uniform(-80, 80)
            y = random.uniform(-80, 80)
            z = random.uniform(-40, 40)
            
            # Skip if too close to center
            if math.sqrt(x*x + y*y) < min_distance:
                continue
            
            # Create star with random brightness
            base_strength = random.uniform(2, 4)
            star = BackgroundStar((x, y, z), base_strength=base_strength)
            star.create()
            star.animate_twinkle(self.animation_frames)
            self.background_stars.append(star)
    
    def setup_camera(self):
        """Create and configure the camera."""
        self.camera = OrbitingCamera()
        self.camera.create()
        self.camera.animate_orbit(self.animation_frames)
    
    def configure_scene(self):
        """Configure rendering and scene settings."""
        scene = bpy.context.scene
        scene.frame_end = self.animation_frames
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 64
        scene.render.fps = 12
        
        # Set background color
        scene.world.use_nodes = True
        bg_node = scene.world.node_tree.nodes["Background"]
        bg_node.inputs[0].default_value = (0, 0, 0.03, 1)
    
    def build(self):
        """Build the complete solar system."""
        print("Building Solar System...")
        
        # Clear existing scene
        self.clear_scene()
        
        # Create sun
        self.create_sun()
        
        # Define planet data
        planet_configs = [
            ("Mercury", 0.4, (0.6, 0.6, 0.6), 5, 0.9),
            ("Venus", 0.9, (0.9, 0.7, 0.3), 7, 0.8),
            ("Earth", 1.0, (0.2, 0.5, 1.0), 10, 0.7),
            ("Mars", 0.5, (0.9, 0.3, 0.2), 13, 0.65),
            ("Jupiter", 2.2, (0.8, 0.6, 0.4), 18, 0.55),
        ]
        
        # Create regular planets
        for name, size, color, radius, speed in planet_configs:
            planet = Planet(name, size, color, radius, speed)
            self.add_planet(planet)
        
        # Create Saturn with rings
        saturn = RingedPlanet("Saturn", 1.9, (0.9, 0.8, 0.5), 24, 0.5)
        self.add_planet(saturn)
        
        # Add remaining planets
        remaining_planets = [
            ("Uranus", 1.4, (0.4, 0.8, 0.9), 30, 0.45),
            ("Neptune", 1.4, (0.3, 0.4, 0.9), 36, 0.4),
            ("Pluto", 0.3, (0.7, 0.6, 0.5), 42, 0.35),
        ]
        
        for name, size, color, radius, speed in remaining_planets:
            planet = Planet(name, size, color, radius, speed)
            self.add_planet(planet)
        
        # Generate background stars
        self.generate_background_stars(count=20)
        
        # Setup camera
        self.setup_camera()
        
        # Configure scene settings
        self.configure_scene()
        
        print(f"✓ Solar System Complete!")
        print(f"  - Sun: {self.sun.name}")
        print(f"  - Planets: {len(self.planets)}")
        print(f"  - Background Stars: {len(self.background_stars)}")
        print(f"  - Animation: {self.animation_frames} frames")


# ------------------- MAIN EXECUTION -------------------
if __name__ == "__main__":
    solar_system = SolarSystem(animation_frames=150)
    solar_system.build()