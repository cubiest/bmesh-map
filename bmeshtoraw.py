bl_info = {
    "name": "Mesh To Raw",
    "author": "Cubiest, Benjamin Lösch",
    "version": (1, 0, 0),
    "blender": (3, 3, 0),
    "description": "Export your mesh as a RAW heightmap (uint16 little-endian)",
    "doc_url": "https://github.com/cubiest/bmesh-to-raw/blob/main/docs/README.md",
    "category": "Object",
}

import bpy, math, struct
from bpy import context


class MTR_PT_ExportSetting(bpy.types.PropertyGroup):
    EXPORT_FILE: bpy.props.StringProperty(name="Filename", default="heightmap", maxlen=30)

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


    def draw(self, context):
        global_settings = context.scene.MTR_ExportProperties

        self.layout.operator("object.stat_mesh", text="Get Status")

        obj = context.active_object
        self.layout.label(text="Stats: " + obj.name)

        res = "Res: </>"
        range = "Min-Max: </>"
        if global_settings.OBJ_PROP_RES:
            res = f"Res: {global_settings.OBJ_PROP_RES}x{global_settings.OBJ_PROP_RES}"
        if global_settings.OBJ_PROP_BOTTOM and global_settings.OBJ_PROP_TOP:
            range = f"Min-Max: {global_settings.OBJ_PROP_BOTTOM} - {global_settings.OBJ_PROP_TOP}"

        self.layout.label(text=res)
        self.layout.label(text=range)

        self.layout.label(text="Export Path:")
        self.layout.prop(global_settings, "EXPORT_FILE")
        self.layout.operator("object.mesh_to_raw", text="Export")


class MTR_StatMesh(bpy.types.Operator):
    bl_label = "Get mesh's heightmap info"
    bl_idname = "object.stat_mesh"

    def execute(self, context):
        obj = context.active_object
        heights = list() # float
        # data is of type bpy.types.Mesh
        for v in obj.data.vertices:
            heights.append(v.co[2])

        bottom = heights[0]
        top = heights[0]
        for h in heights:
            if h > top:
                top = h
            elif h < bottom:
                bottom = h
        bottom = round_decimals(bottom, 4)
        top = round_decimals(top, 4)

        res = str(int(math.sqrt(len(obj.data.vertices))))

        global_settings = context.scene.MTR_ExportProperties
        global_settings.OBJ_PROP_RES = res
        global_settings.OBJ_PROP_BOTTOM = str(bottom)
        global_settings.OBJ_PROP_TOP = str(top)

        return {'FINISHED'}


class MTR_MeshToRaw(bpy.types.Operator):
    bl_idname = "object.mesh_to_raw"
    bl_label = "Mesh to Raw"


    def execute(self, context):
        obj = context.active_object
        positions = list() # Vector2
        heights = list() # float
        # data is of type bpy.types.Mesh
        for v in obj.data.vertices:
            positions.append(v.co.to_2d())
            heights.append(v.co[2])

        width = int(obj.dimensions[0])+1
        depth = int(obj.dimensions[1])+1

        heightmap = [[0 for x in range(width)] for y in range(depth)] # integers

        bottom = heights[0]
        top = heights[0]
        for h in heights:
            if h > top:
                top = h
            elif h < bottom:
                bottom = h
        bottom = round_decimals(bottom, 4)
        top = round_decimals(top, 4)

        h_scale = 65535.0 / (top - bottom)

        for i in range(len(positions)):
            pos = positions[i]
            x = int(pos[0])
            y = int(pos[1])
            if x < 0 or y < 0 or x >= width or y >= depth:
                break
            heightmap[x][y] = round_int((heights[i] - bottom) * h_scale)
      
        flattend_heightmap = list()
        for y in range(depth):
            for x in range(width):
                flattend_heightmap.append(heightmap[x][y])

        bytes = struct.pack(f"<{width*depth}H", *flattend_heightmap) # little-endian, ushort (aka unsigned 16-bit-integer)

        global_settings = context.scene.MTR_ExportProperties

        e_file = global_settings.EXPORT_FILE
        if not e_file.endswith(".raw"):
            e_file += ".raw"
        e_file =  "//" + e_file # make relative path from blend file

        export_path = bpy.path.abspath(e_file)
        export = open(export_path, 'bw') # open in binary-write mode
        export.write(bytes)
        export.close()

        return {'FINISHED'}


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
