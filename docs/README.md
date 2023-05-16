# How-to

## Blender

Example Process
* Create a new A.N.T. Landscape (_install the A.N.T. addon if not already done so_) and set
  * Mesh Size to 128x128, and
  * Subdivision to 129x129 (_NOTE_: subdivision must always be 1 higher)
    * **this value is the resolution (power of 2 + 1)**
  * Make sure the Object's Origin is at the bottom-left of your Mesh (then all vertices have positive positions on the x- and y-axis).
* While in `Object Mode`, open the `BMesh Map`-tools-tab,
  * click `Get Status`: shows you info on your Mesh: check your resolution and copy your min and max height values,
  * specify the location and filename to save to
  * **for Godot (Zylann's Heightmap Plugin)**: make sure that `Invert X-axis` is toggled, else your map is mirrored on the x-axis
  * choose your bit-depth
    * 24-bit: good choice
    * 16-bit: known to introduce precision issues
  * choose your endianness (default: little)
  * click `Export` and you get your mesh as a heightmap file (`.raw`)
* Done

![Mesh in Blender](images/blender.png)


## Godot

In Godot, with Zylann's Heightmap Plugin, you import your `.raw` file like `.png`, `.exr`, etc.

Import settings
* Raw Endianess: The one you chose on your export
* godot4 branch:
  * Once [this PR](https://github.com/Zylann/godot_heightmap_plugin/pull/369) is merged, you can import 24-bit raw files. Bit-depth is auto-detected.
* main branch (for Godot 3.x)
  * expects 16-bit raw file; **does not support 24-bit import!**
* `Min Height` + `Max Height`: take them from the Add-on Panel in Blender, see `Min-Max`.

![Imported map in Godot using Zylann's Heightmap Plugin](images/godot_zylanns_hm_plugin.png)

Enjoy the beautiful export!
