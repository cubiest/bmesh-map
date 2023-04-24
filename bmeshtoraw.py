bl_info = {
    "name": "Mesh To Raw",
    "author": "Cubiest, Benjamin Lösch",
    "version": (1, 2, 0),
    "blender": (3, 3, 0),
    "description": "Export your mesh as a RAW heightmap (uint16 little-endian)",
    "doc_url": "https://github.com/cubiest/bmesh-to-raw/blob/main/docs/README.md",
    "category": "Object",
}

import bpy, math, struct
from bpy import context


class MTR_PT_ExportSetting(bpy.types.PropertyGroup):
    EXPORT_FILE: bpy.props.StringProperty(name="Filename:", default="heightmap", maxlen=30)
    EXPORT_ERROR: bpy.props.BoolProperty() # is True if last execution failed or `object.stat_mesh` found an error
    EXPORT_INVERT_Y: bpy.props.BoolProperty(name="Invert Y-axis")
    EXPORT_INVERT_X: bpy.props.BoolProperty(name="Invert X-axis", default=True)

    OBJ_PROP_FULL_NAME: bpy.props.StringProperty()
    OBJ_PROP_RES: bpy.props.StringProperty()
    OBJ_PROP_BOTTOM: bpy.props.StringProperty()
    OBJ_PROP_TOP: bpy.props.StringProperty()


class MTR_PT_ExportPanel(bpy.types.Panel):
    """Mesh to Raw (unsigned 16-bit-integer in little-endian)"""
    bl_label = "RAW Heightmap Exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Heightmap"


    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'


    def get_version(self):
        version = ""
        for v in bl_info["version"]:
            version += str(v) + "."
        if version.endswith("."):
            version = version[:-1]
        return version


    def draw(self, context):
        layout = self.layout
        global_settings = context.scene.MTR_ExportProperties

        name = context.active_object.name
        res = "?"
        bottom = "?"
        top = "?"

        if context.active_object.name == global_settings.OBJ_PROP_FULL_NAME:
            res = global_settings.OBJ_PROP_RES
            bottom = global_settings.OBJ_PROP_BOTTOM
            top = global_settings.OBJ_PROP_TOP

        res = f"Res: {res}x{res}"
        range = f"Min-Max: {bottom} - {top}"

        col = layout.column()
        col.label(text="Stats:")
        col.operator("object.stat_mesh", text="Get Status")

        box = col.box()
        box.label(text="Name: " + name)
        box.label(text=res)
        box.label(text=range)

        col.separator() # close box

        col.label(text="Export:")

        box = col.box()
        if global_settings.EXPORT_ERROR:
            box.alert = global_settings.EXPORT_ERROR
        box.prop(global_settings, "EXPORT_FILE")
        box.prop(global_settings, "EXPORT_INVERT_Y")
        box.prop(global_settings, "EXPORT_INVERT_X")
        box.operator("object.mesh_to_raw", text="Export")

        col.separator() # close box

        col.label(text="ver " + self.get_version())


class MTR_StatMesh(bpy.types.Operator):
    bl_label = "Get mesh's heightmap info and check for errors"
    bl_idname = "object.stat_mesh"


    def execute(self, context):
        result = fullcheck(self, context)

        global_settings = context.scene.MTR_ExportProperties
        global_settings.OBJ_PROP_RES = str(result[1])
        global_settings.OBJ_PROP_BOTTOM = str(result[4])
        global_settings.OBJ_PROP_TOP = str(result[5])

        global_settings.EXPORT_ERROR = not result[0]

        return {'FINISHED'}


class MTR_MeshToRaw(bpy.types.Operator):
    bl_idname = "object.mesh_to_raw"
    bl_label = "Mesh to Raw"


    def execute(self, context):
        result = fullcheck(self, context)
        if not result[0]:
            context.scene.MTR_ExportProperties.EXPORT_ERROR = True
            return {'CANCELLED'}

        res = result[1]
        bottom = result[4]
        top = result[5]
        h_scale = 65535.0 / (top - bottom)
        positions = result[2]
        heights = result[3]
        heightmap = [[0 for x in range(res)] for y in range(res)] # integers

        for i in range(len(positions)):
            pos = positions[i]
            x = int(pos[0])
            y = int(pos[1])
            heightmap[x][y] = round_int((heights[i] - bottom) * h_scale)

        global_settings = context.scene.MTR_ExportProperties

        y_start = 0
        y_stop = res
        y_step = 1
        x_start = 0
        x_stop = res
        x_step = 1
        if global_settings.EXPORT_INVERT_Y:
            y_start = res-1
            y_stop = -1
            y_step = -1
        if global_settings.EXPORT_INVERT_X:
            x_start = res-1
            x_stop = -1
            x_step = -1

        flattend_heightmap = list()
        for y in range(y_start, y_stop, y_step):
            for x in range(x_start, x_stop, x_step):
                flattend_heightmap.append(heightmap[x][y])

        bytes = struct.pack(f"<{res*res}H", *flattend_heightmap) # little-endian, ushort (aka unsigned 16-bit-integer)

        e_file = global_settings.EXPORT_FILE
        if not e_file.endswith(".raw"):
            e_file += ".raw"
        e_file =  "//" + e_file # make relative path from blend file

        export_path = bpy.path.abspath(e_file)
        export = open(export_path, 'bw') # open in binary-write mode
        export.write(bytes)
        export.close()

        global_settings.EXPORT_ERROR = False
        show_info_msg(self, "Export done")

        return {'FINISHED'}


# fullcheck returns a tuple defined as follows
# - bool: is True if no errors were found
# - int: Mesh resolution
# - list: positions, or empty on error
# - list: heights, or empty on error
# - float: lowest height value, or 0.0 on error
# - float: highest height value, or 0.0 on error
def fullcheck(self, context):
    global_settings = context.scene.MTR_ExportProperties

    obj = context.active_object
    global_settings.OBJ_PROP_FULL_NAME = obj.name_full
    res = int(math.sqrt(len(obj.data.vertices)))

    positions = list() # Vector2
    heights = list() # float
    # data is of type bpy.types.Mesh
    for v in obj.data.vertices:
        positions.append(v.co.to_2d())
        heights.append(v.co[2])

    ok = precheck(self, obj, res, positions)
    if not ok:
        return (False, res, [], [], 0.0, 0.0)

    bottom = heights[0]
    top = heights[0]
    for h in heights:
        if h > top:
            top = h
        elif h < bottom:
            bottom = h
    bottom = round_decimals(bottom, 4)
    top = round_decimals(top, 4)

    return (True, res, positions, heights, bottom, top)


def precheck(self, obj, res, positions):
    if not is_power_of_2(res-1):
        show_error_msg(self, f"Mesh resolution is not power of 2 + 1: got {res}")
        return False

    width = int(obj.dimensions[0])
    depth = int(obj.dimensions[1])

    if width != depth:
        show_error_msg(self, f"Dimensions are not equal: got {width}x{depth}")
        return False

    if not is_power_of_2(width):
        show_error_msg(self, f"Dimensions are not power of 2: got {width}")
        return False

    for i in range(len(positions)):
        pos = positions[i]
        x = int(pos[0])
        y = int(pos[1])
        if x < 0 or y < 0 or x >= res or y >= res:
            show_error_msg(self, f"Position ({x}, {y}) is out-of-bounds [0, {res - 1}]")
            return False

    return True


def show_error_msg(self, txt):
    msg = (txt)
    self.report({'ERROR'}, msg)


def show_info_msg(self, txt):
    msg = (txt)
    self.report({'INFO'}, msg)


# formula taken from: https://stackoverflow.com/a/57025941 (© @tomerikoo)
def is_power_of_2(n):
    return (n & (n-1) == 0) and n != 0


def round_int(v):
    return math.floor(v + 0.5)


def round_decimals(v, dec=0):
    mul = 10 ** dec
    return math.floor(v * mul + 0.5) / mul


def register():
    bpy.utils.register_class(MTR_PT_ExportSetting)
    bpy.utils.register_class(MTR_StatMesh)
    bpy.utils.register_class(MTR_MeshToRaw)
    bpy.utils.register_class(MTR_PT_ExportPanel)

    bpy.types.Scene.MTR_ExportProperties = bpy.props.PointerProperty(type=MTR_PT_ExportSetting)


def unregister():
    bpy.utils.unregister_class(MTR_PT_ExportPanel)
    bpy.utils.unregister_class(MTR_MeshToRaw)
    bpy.utils.unregister_class(MTR_StatMesh)
    bpy.utils.unregister_class(MTR_PT_ExportSetting)

    del bpy.types.Scene.MTR_ExportProperties


if __name__ == "__main__":
    register()
