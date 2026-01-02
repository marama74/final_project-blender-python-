# OOP Solar System Generator for Blender

A procedurally generated, animated solar system built using **Object-Oriented Programming principles** in Python for Blender 3D.

## Project Overview

This project demonstrates advanced Python programming and 3D procedural generation by creating a complete animated solar system with planets, orbits, twinkling stars, and a dynamic camera system—all generated through code.

## Features

### Core Functionality
- **Central Sun** - Emissive glowing sphere at the solar system center
- **9 Planets** - Mercury through Pluto with accurate relative characteristics
- **Saturn's Rings** - Special ringed planet implementation
- **Orbit Rings** - Visual orbit paths that remain stationary
- **Twinkling Stars** - 20+ procedurally generated background stars
- **Orbiting Camera** - Animated camera for cinematic views
- **Text Labels** - Planet names displayed above each body

### Object-Oriented Design
- **8 Core Classes** implementing proper OOP principles
- **Inheritance hierarchy** for celestial bodies
- **Encapsulation** of object creation and animation logic
- **Polymorphism** through shared interfaces
- **Composition** for scene management

## Class Architecture

```
MaterialFactory
    ├── create_emissive()
    └── create_planet_material()

CelestialBody (Abstract Base)
    ├── Star (Sun)
    ├── Planet
    │   └── RingedPlanet (Saturn)
    └── BackgroundStar

OrbitingCamera

SolarSystem (Main Orchestrator)
```

### Class Descriptions

| Class | Purpose | Key Methods |
|-------|---------|-------------|
| `MaterialFactory` | Creates Blender materials | `create_emissive()`, `create_planet_material()` |
| `CelestialBody` | Base class for space objects | `create()`, `add_label()` |
| `Star` | Central sun | `create()` |
| `Planet` | Orbiting planets | `create()`, `animate_orbit()` |
| `RingedPlanet` | Planets with rings (Saturn) | `create()`, `_create_rings()` |
| `BackgroundStar` | Distant stars | `create()`, `animate_twinkle()` |
| `OrbitingCamera` | Camera system | `create()`, `animate_orbit()` |
| `SolarSystem` | Scene manager | `build()`, `add_planet()`, `generate_background_stars()` |

## Educational Requirements Met

- **Object-Oriented Design** - All code structured around classes
- **Procedural Generation** - 20+ stars with randomized properties
- **Runtime Variations** - Random positions, sizes, brightness, twinkling
- **Animation** - Keyframed planet orbits, star twinkling, camera movement
- **Encapsulation** - Each class manages its own data and behavior
- **Complete Scene** - Fully functional solar system environment
- **No External Dependencies** - Pure Python + Blender API

## Installation & Usage

### Prerequisites
- **Blender 3.0+** (with Python 3.9+)
- No additional packages required

### Running the Script

#### Method 1: Blender Scripting Tab
1. Open Blender
2. Switch to **Scripting** workspace
3. Click **New** to create a new text file
4. Paste the solar system code
5. Click **Run Script** (play button)

#### Method 2: External Python File
1. Save the script as `solar_system.py`
2. Open Blender
3. Go to **Scripting** → **Open** → Select `solar_system.py`
4. Click **Run Script**

#### Method 3: Command Line
```bash
blender --python solar_system.py
```

### Expected Output
- Scene clears automatically
- 9 planets created with orbit rings
- 20 twinkling background stars
- Camera positioned and animated
- 150-frame animation ready to play

## Animation Details

### Timeline
- **Total Frames**: 150
- **Frame Rate**: 12 FPS
- **Duration**: ~12.5 seconds

### Animations
1. **Planet Orbits** - Each planet moves along circular path at different speed
2. **Star Twinkling** - Emission strength varies randomly over time
3. **Camera Orbit** - Full 360° rotation around solar system

### Keyframe Intervals
- Planets: Every 5 frames
- Camera: Every 5 frames
- Stars: Every 10 frames

## Planet Configuration

| Planet | Size | Orbit Radius | Speed | Color |
|--------|------|--------------|-------|-------|
| Mercury | 0.4 | 5 | 0.9 | Gray |
| Venus | 0.9 | 7 | 0.8 | Yellow-Orange |
| Earth | 1.0 | 10 | 0.7 | Blue |
| Mars | 0.5 | 13 | 0.65 | Red |
| Jupiter | 2.2 | 18 | 0.55 | Orange-Brown |
| Saturn | 1.9 | 24 | 0.5 | Yellow (with rings) |
| Uranus | 1.4 | 30 | 0.45 | Cyan |
| Neptune | 1.4 | 36 | 0.4 | Dark Blue |
| Pluto | 0.3 | 42 | 0.35 | Gray-Brown |

## Rendering Settings

### Default Configuration
- **Engine**: Cycles (ray-tracing)
- **Samples**: 64
- **Background**: Dark blue (0, 0, 0.03)
- **Camera Angle**: 55° tilt

### Customization Options
Modify these parameters in the `SolarSystem` class:

```python
# Change animation length
solar_system = SolarSystem(animation_frames=300)

# Modify camera settings
camera = OrbitingCamera(distance=80, height=40, tilt_angle=60)

# Add more stars
solar_system.generate_background_stars(count=50)
```

## Customization Guide

### Adding New Planets
```python
# Create a custom planet
custom_planet = Planet(
    name="CustomPlanet",
    size=1.5,
    color=(1.0, 0.5, 0.0),  # RGB color
    orbit_radius=15,
    orbit_speed=0.6
)
solar_system.add_planet(custom_planet)
```

### Creating Ringed Planets
```python
# Create another ringed planet
uranus = RingedPlanet(
    name="Uranus",
    size=1.4,
    color=(0.4, 0.8, 0.9),
    orbit_radius=30,
    orbit_speed=0.45,
    ring_major_radius=2.5,
    ring_minor_radius=0.1
)
```

### Adjusting Star Field
```python
# More/fewer stars
solar_system.generate_background_stars(count=50, min_distance=60)
```

## Performance Considerations

### Optimization Tips
- Reduce `cycles.samples` for faster preview (default: 64)
- Decrease star count for simpler scenes
- Adjust keyframe intervals for smoother/faster animation
- Use Eevee engine for real-time preview

### Typical Render Times (per frame)
- **Eevee**: ~1-2 seconds
- **Cycles (64 samples)**: ~5-10 seconds
- **Cycles (128 samples)**: ~10-20 seconds

## Learning Objectives

This project demonstrates:
1. **OOP Principles** - Inheritance, encapsulation, polymorphism
2. **Procedural Generation** - Runtime object creation with variations
3. **3D Mathematics** - Trigonometric calculations for orbits
4. **Animation Techniques** - Keyframe insertion and interpolation
5. **Material Systems** - Node-based shader creation
6. **Scene Management** - Organizing complex 3D environments

## Code Structure

```
solar_system.py
├── MaterialFactory          # Material creation utilities
├── CelestialBody           # Base class for space objects
│   ├── Star                # Sun implementation
│   ├── Planet              # Regular planets
│   │   └── RingedPlanet   # Saturn-type planets
│   └── BackgroundStar      # Distant stars
├── OrbitingCamera          # Camera animation system
└── SolarSystem             # Main orchestrator
    └── build()             # Entry point
```

## Troubleshooting

### Common Issues

**"No module named 'bpy'"**
- Script must run inside Blender, not standard Python

**Objects not appearing**
- Check if scene was cleared properly
- Verify camera is set correctly

**Animation not playing**
- Click the play button in timeline
- Check frame range (should be 0-150)

**Render is black**
- Ensure Cycles engine is selected
- Check camera is set as active camera

## Future Enhancements

Potential additions:
- Moons orbiting planets
- Asteroid belt between Mars and Jupiter
- Comet with trailing particles
- Planet rotation on axis
- Realistic planet textures
- Scale-accurate sizes and distances
- Day/night lighting on planets
- User input for custom configurations

## License

This project is created for educational purposes. Feel free to use, modify, and distribute with attribution.

## Contributing

Suggestions for improvements:
- Add more celestial bodies
- Implement realistic physics
- Create texture mapping system
- Add particle systems for effects
- Optimize rendering performance

## Acknowledgments

- Built using **Blender 3D** and Python API
- Inspired by real solar system mechanics
- Designed for educational demonstration of OOP principles
  
## Authors
Maryam Arshad(498506),Shahab Shinwari
(539515),
Usama Bin Nadeem (539308),
Naveed Anjum (577607)


---

**Created for learning Object-Oriented Programming in 3D**

Made with Blender | Python | Procedural Generation
