# Solar System Animation - Blender Script

An animated 3D solar system visualization created in Blender using Python scripting. Features all 9 planets (including Pluto) orbiting around the sun with glowing orbit rings, twinkling stars, and a rotating camera view.

## Features

- **Stationary Sun**: Bright glowing sun at the center (radius: 3 units)
- **9 Orbiting Planets**: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, and Pluto
- **Glowing Orbit Rings**: Blue neon-style rings showing each planet's path
- **Saturn's Rings**: Special torus rings for Saturn
- **Planet Labels**: Text labels above each planet
- **Twinkling Stars**: 20 randomly placed stars with pulsing animation
- **Rotating Camera**: 360° orbiting camera view
- **150 Frame Animation**: Smooth looping animation at 12 FPS

## Visual Style

- Dark space background with deep blue-black color
- Emissive materials for glowing effects on sun, stars, and orbit rings
- Realistic planet colors and sizes (scaled for visibility)
- Clean educational visualization style

## Requirements

- **Blender 3.0+** (tested on Blender 3.x and 4.x)
- No additional add-ons required

## Installation and Usage

### Method 1: Run in Blender Scripting Tab

1. Open Blender
2. Switch to the **Scripting** workspace (top menu bar)
3. Click **New** to create a new text file
4. Copy and paste the script
5. Click **Run Script** button (or press `Alt + P`)
6. Press **Spacebar** in the viewport to play the animation

### Method 2: Run from Command Line

```bash
blender --python solar_system.py
```

## Configuration

You can customize the animation by modifying these variables at the top of the script:

```python
ANIMATION_FRAMES = 150           # Total animation length
PLANET_KEYFRAME_INTERVAL = 5     # Planet animation smoothness
CAMERA_KEYFRAME_INTERVAL = 5     # Camera movement smoothness
STAR_COUNT = 20                  # Number of background stars
```

## Planet Data

| Planet   | Size | Color          | Orbit Radius | Speed |
|----------|------|----------------|--------------|-------|
| Mercury  | 0.4  | Gray           | 5            | 0.9   |
| Venus    | 0.9  | Yellow-Orange  | 7            | 0.8   |
| Earth    | 1.0  | Blue           | 10           | 0.7   |
| Mars     | 0.5  | Red            | 13           | 0.65  |
| Jupiter  | 2.2  | Brown-Orange   | 18           | 0.55  |
| Saturn   | 1.9  | Yellow (w/rings)| 24          | 0.5   |
| Uranus   | 1.4  | Cyan           | 30           | 0.45  |
| Neptune  | 1.4  | Deep Blue      | 36           | 0.4   |
| Pluto    | 0.3  | Gray-Brown     | 42           | 0.35  |

## Animation Details

- **Planets**: Revolve around the sun at different speeds (inner planets faster)
- **Orbit Rings**: Remain stationary in place
- **Sun**: Fixed at origin (0, 0, 0)
- **Stars**: Twinkle with random emission strength variations
- **Camera**: Orbits at 60 units distance, elevated at 30 units height, angled at 55 degrees

## Rendering

The script is configured to use **Cycles** render engine with 64 samples. To render:

1. Go to **Render** then **Render Animation** (or press `Ctrl + F12`)
2. Set output path in **Output Properties**
3. Choose desired format (MP4, PNG sequence, etc.)

### Recommended Settings

- Render Engine: Cycles
- Samples: 64 (faster) or 128+ (higher quality)
- Resolution: 1920x1080 or higher
- Frame Rate: 12 FPS (can be changed to 24 or 30 FPS)

## Customization Ideas

- **Add moons**: Create additional spheres parented to planets
- **Adjust planet speeds**: Modify the `speed` value in `planet_data`
- **Change colors**: Modify RGB values in the planet data tuples
- **More stars**: Increase `STAR_COUNT`
- **Different camera angles**: Modify camera location and rotation
- **Add textures**: Replace solid colors with image textures
- **Asteroid belt**: Add small spheres between Mars and Jupiter

## Technical Notes

- Uses **Empty objects** as rotation pivots for planetary orbits
- **Keyframe animation** for smooth motion
- **Emissive materials** for self-illuminating objects
- **Curve objects** for orbit rings with bevel for thickness
- **Parenting system** to link planets to rotation empties

## Troubleshooting

**Script doesn't run:**
- Make sure you're using Blender 3.0 or newer
- Check the console for error messages (Window, Toggle System Console)

**Nothing appears:**
- The script clears the entire scene first - this is normal
- Make sure camera view is active (press `Numpad 0`)

**Animation is choppy:**
- Reduce `CYCLES.samples` for faster preview
- Use EEVEE engine for real-time preview: `scene.render.engine = 'BLENDER_EEVEE'`

**Stars not visible:**
- Stars are placed outside a 50-unit radius from center
- Zoom out or adjust camera distance to see them

## License

Free to use for educational and personal projects. Feel free to modify and share.

## Author

Created as an educational Blender Python scripting example for visualizing our solar system.

## Credits

- Inspired by real astronomical data (sizes and distances scaled for visibility)
- Built using Blender's Python API (bpy)

---

**Enjoy your animated solar system!**
