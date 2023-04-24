# Blender Mesh to RAW file Exporter

Exports your selected object's mesh as a heightmap `.raw` file.
* ushort (aka 16bit unsigned integer)
* little-endianess

Works well with [Zylann's Heightmap Plugin](https://github.com/Zylann/godot_heightmap_plugin)


## Installation

Download the file and install like any Blender Add-on.


## Restrictions

To get an accurate heightmap,
* your vertices should be on full meters (float values should equal their integer representation), i.e. the vertices should be on the Blender Grid
  * a simple check: Set `Viewport Shading` to `Wireframe` and look orthogonal from above. Mesh vertices should align perfectly with Blender Grid
* width and detph (x- and y-axis) must be equal the object Dimensions should be a power of 2 (e.g. 128x128, 256x256, 512x512, 1024x1024, etc.), which creates a resolution of power of 2 plus 1 (e.g. 129x129, etc.)
