## Simple Workflow Example

**Blender**

* Create a new A.N.T. Landscape (_install the A.N.T. addon if not already done so_) and set
  * Mesh Size to 128x128, and
  * Subdivision to 129x129 (_NOTE_: subdivision must always be 1 higher)
    * **this value is the resolution (power of 2 + 1)**
* While in `Object Mode`, open the `BMesh Map`-tools-tab,
  * clicking on `Get Status` gives you feedback on your Mesh: check your resolution and copy your min and max height values,
  * specify the location and filename to save to
  * choose your bit-depth
    * 32-bit (best results)
    * 24-bit (good results)
    * 16-bit (potentially bad results)
  * choose your endianness (default: little)
  * click `Export` and you get your mesh as a heightmap file (`.raw`)
* Done

![Mesh in Blender](images/blender_raw.png)


**Godot**

In Godot, with Zylann's Heightmap Plugin, you import your `.raw` file like `.png`, `.exr`, etc.

Import settings
* Bit depth and Raw Endianess: The ones you chose on your export
* for Godot 3.x:
  * only supports 16-bit raw file
* `Min Height` + `Max Height`: take them from the Add-on Panel in Blender, see `Min-Max`.

![Imported map in Godot using Zylann's Heightmap Plugin](images/godot_zylanns_hm_plugin.png)

Enjoy the beautiful export!