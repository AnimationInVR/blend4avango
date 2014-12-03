import bpy
    
from . import export_threejs   
from bpy.props import *
from bpy_extras.io_utils import ExportHelper

# ################################################################
# Custom properties
# ################################################################

bpy.types.Object.THREE_castShadow = bpy.props.BoolProperty()
bpy.types.Object.THREE_receiveShadow = bpy.props.BoolProperty()
bpy.types.Object.THREE_doubleSided = bpy.props.BoolProperty()
bpy.types.Object.THREE_exportGeometry = bpy.props.BoolProperty(default = True)
bpy.types.Object.THREE_visible = bpy.props.BoolProperty(default = True)

bpy.types.Material.THREE_useVertexColors = bpy.props.BoolProperty()
bpy.types.Material.THREE_depthWrite = bpy.props.BoolProperty(default = True)
bpy.types.Material.THREE_depthTest = bpy.props.BoolProperty(default = True)

THREE_material_types = [("Basic", "Basic", "Basic"), ("Phong", "Phong", "Phong"), ("Lambert", "Lambert", "Lambert")]
bpy.types.Material.THREE_materialType = EnumProperty(name = "Material type", description = "Material type", items = THREE_material_types, default = "Lambert")

THREE_blending_types = [("NoBlending", "NoBlending", "NoBlending"), ("NormalBlending", "NormalBlending", "NormalBlending"),
                        ("AdditiveBlending", "AdditiveBlending", "AdditiveBlending"), ("SubtractiveBlending", "SubtractiveBlending", "SubtractiveBlending"),
                        ("MultiplyBlending", "MultiplyBlending", "MultiplyBlending"), ("AdditiveAlphaBlending", "AdditiveAlphaBlending", "AdditiveAlphaBlending")]
bpy.types.Material.THREE_blendingType = EnumProperty(name = "Blending type", description = "Blending type", items = THREE_blending_types, default = "NormalBlending")

class OBJECT_PT_hello( bpy.types.Panel ):

    bl_label = "THREE"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.label(text="Selected object: " + obj.name )

        row = layout.row()
        row.prop( obj, "THREE_exportGeometry", text="Export geometry" )

        row = layout.row()
        row.prop( obj, "THREE_castShadow", text="Casts shadow" )

        row = layout.row()
        row.prop( obj, "THREE_receiveShadow", text="Receives shadow" )

        row = layout.row()
        row.prop( obj, "THREE_doubleSided", text="Double sided" )
        
        row = layout.row()
        row.prop( obj, "THREE_visible", text="Visible" )

class MATERIAL_PT_hello( bpy.types.Panel ):

    bl_label = "THREE"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    def draw(self, context):
        layout = self.layout
        mat = context.material

        row = layout.row()
        row.label(text="Selected material: " + mat.name )

        row = layout.row()
        row.prop( mat, "THREE_materialType", text="Material type" )

        row = layout.row()
        row.prop( mat, "THREE_blendingType", text="Blending type" )

        row = layout.row()
        row.prop( mat, "THREE_useVertexColors", text="Use vertex colors" )

        row = layout.row()
        row.prop( mat, "THREE_depthWrite", text="Enable depth writing" )

        row = layout.row()
        row.prop( mat, "THREE_depthTest", text="Enable depth testing" )

# ################################################################
# Exporter - settings
# ################################################################

SETTINGS_FILE_EXPORT = "threejs_settings_export.js"

import os
import json

def file_exists(filename):
    """Return true if file exists and accessible for reading.
    Should be safer than just testing for existence due to links and
    permissions magic on Unix filesystems.
    @rtype: boolean
    """

    try:
        f = open(filename, 'r')
        f.close()
        return True
    except IOError:
        return False

def get_settings_fullpath():
    return os.path.join(bpy.app.tempdir, SETTINGS_FILE_EXPORT)

def save_settings_export(properties):

    settings = {
    "option_export_scene" : properties.option_export_scene,
    "option_embed_meshes" : properties.option_embed_meshes,
    "option_url_base_html" : properties.option_url_base_html,
    "option_copy_textures" : properties.option_copy_textures,

    "option_lights" : properties.option_lights,
    "option_cameras" : properties.option_cameras,

    "option_animation_morph" : properties.option_animation_morph,
    "option_animation_skeletal" : properties.option_animation_skeletal,
    "option_frame_index_as_time" : properties.option_frame_index_as_time,

    "option_frame_step" : properties.option_frame_step,
    "option_all_meshes" : properties.option_all_meshes,

    "option_flip_yz"      : properties.option_flip_yz,

    "option_materials"       : properties.option_materials,
    "option_normals"         : properties.option_normals,
    "option_colors"          : properties.option_colors,
    "option_uv_coords"       : properties.option_uv_coords,
    "option_faces"           : properties.option_faces,
    "option_vertices"        : properties.option_vertices,

    "option_skinning"        : properties.option_skinning,
    "option_bones"           : properties.option_bones,

    "option_vertices_truncate" : properties.option_vertices_truncate,
    "option_scale"        : properties.option_scale,

    "align_model"         : properties.align_model
    }

    fname = get_settings_fullpath()
    f = open(fname, "w")
    json.dump(settings, f)

def restore_settings_export(properties):

    settings = {}

    fname = get_settings_fullpath()
    if file_exists(fname):
        f = open(fname, "r")
        settings = json.load(f)

    properties.option_vertices = settings.get("option_vertices", True)
    properties.option_vertices_truncate = settings.get("option_vertices_truncate", True)
    properties.option_faces = settings.get("option_faces", True)
    properties.option_normals = settings.get("option_normals", True)

    properties.option_colors = settings.get("option_colors", True)
    properties.option_uv_coords = settings.get("option_uv_coords", True)
    properties.option_materials = settings.get("option_materials", True)

    properties.option_skinning = settings.get("option_skinning", True)
    properties.option_bones = settings.get("option_bones", True)

    properties.align_model = settings.get("align_model", "None")

    properties.option_scale = settings.get("option_scale", 1.0)
    properties.option_flip_yz = settings.get("option_flip_yz", True)

    properties.option_export_scene = settings.get("option_export_scene", True)
    properties.option_embed_meshes = settings.get("option_embed_meshes", True)
    properties.option_url_base_html = settings.get("option_url_base_html", True)
    properties.option_copy_textures = settings.get("option_copy_textures", True)

    properties.option_lights = settings.get("option_lights", True)
    properties.option_cameras = settings.get("option_cameras", True)

    properties.option_animation_morph = settings.get("option_animation_morph", False)
    properties.option_animation_skeletal = settings.get("option_animation_skeletal", False)
    properties.option_frame_index_as_time = settings.get("option_frame_index_as_time", False)

    properties.option_frame_step = settings.get("option_frame_step", 1)
    properties.option_all_meshes = settings.get("option_all_meshes", True)

# ################################################################
# Exporter
# ################################################################

class ExportTHREEJS(bpy.types.Operator, ExportHelper):
    '''Export selected object / scene for Three.js (ASCII JSON format).'''

    bl_idname = "export.threejs"
    bl_label = "Export Three.js"

    filename_ext = ".json"

    option_vertices = BoolProperty(name = "Vertices", description = "Export vertices", default = True)
    option_vertices_deltas = BoolProperty(name = "Deltas", description = "Delta vertices", default = True)
    option_vertices_truncate = BoolProperty(name = "Truncate", description = "Truncate vertices", default = True)

    option_faces = BoolProperty(name = "Faces", description = "Export faces", default = True)
    option_faces_deltas = BoolProperty(name = "Deltas", description = "Delta faces", default = True)

    option_normals = BoolProperty(name = "Normals", description = "Export normals", default = True)

    option_colors = BoolProperty(name = "Colors", description = "Export vertex colors", default = True)
    option_uv_coords = BoolProperty(name = "UVs", description = "Export texture coordinates", default = True)
    option_materials = BoolProperty(name = "Materials", description = "Export materials", default = True)

    option_skinning = BoolProperty(name = "Skinning", description = "Export skin data", default = True)
    option_bones = BoolProperty(name = "Bones", description = "Export bones", default = True)

    align_types = [("None","None","None"), ("Center","Center","Center"), ("Bottom","Bottom","Bottom"), ("Top","Top","Top")]
    align_model = EnumProperty(name = "Align model", description = "Align model", items = align_types, default = "None")

    option_scale = FloatProperty(name = "Scale", description = "Scale vertices", min = 0.01, max = 1000.0, soft_min = 0.01, soft_max = 1000.0, default = 1.0)
    option_flip_yz = BoolProperty(name = "Flip YZ", description = "Flip YZ", default = True)

    option_export_scene = BoolProperty(name = "Scene", description = "Export scene", default = True)
    option_embed_meshes = BoolProperty(name = "Embed meshes", description = "Embed meshes", default = True)
    option_copy_textures = BoolProperty(name = "Copy textures", description = "Copy textures", default = True)
    option_url_base_html = BoolProperty(name = "HTML as url base", description = "Use HTML as url base ", default = True)

    option_lights = BoolProperty(name = "Lights", description = "Export default scene lights", default = True)
    option_cameras = BoolProperty(name = "Cameras", description = "Export default scene cameras", default = True)

    option_animation_morph = BoolProperty(name = "Morph animation", description = "Export animation (morphs)", default = False)
    option_animation_skeletal = BoolProperty(name = "Skeletal animation", description = "Export animation (skeletal)", default = False)
    option_frame_index_as_time = BoolProperty(name = "Frame index as time", description = "Use (original) frame index as frame time", default = False)

    option_frame_step = IntProperty(name = "Frame step", description = "Animation frame step", min = 1, max = 1000, soft_min = 1, soft_max = 1000, default = 1)
    option_all_meshes = BoolProperty(name = "All meshes", description = "All meshes (merged)", default = True)

    def invoke(self, context, event):
        restore_settings_export(self.properties)
        return ExportHelper.invoke(self, context, event)

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        print("Selected: " + context.active_object.name)

        if not self.properties.filepath:
            raise Exception("filename not set")

        save_settings_export(self.properties)

        filepath = self.filepath

        return export_threejs.save(self, context, **self.properties)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Geometry:")

        row = layout.row()
        row.prop(self.properties, "option_vertices")
        # row = layout.row()
        # row.enabled = self.properties.option_vertices
        # row.prop(self.properties, "option_vertices_deltas")
        row.prop(self.properties, "option_vertices_truncate")
        layout.separator()

        row = layout.row()
        row.prop(self.properties, "option_faces")
        row = layout.row()
        row.enabled = self.properties.option_faces
        # row.prop(self.properties, "option_faces_deltas")
        layout.separator()

        row = layout.row()
        row.prop(self.properties, "option_normals")
        layout.separator()

        row = layout.row()
        row.prop(self.properties, "option_bones")
        row.prop(self.properties, "option_skinning")
        layout.separator()

        row = layout.row()
        row.label(text="Materials:")

        row = layout.row()
        row.prop(self.properties, "option_uv_coords")
        row.prop(self.properties, "option_colors")
        row = layout.row()
        row.prop(self.properties, "option_materials")
        layout.separator()

        row = layout.row()
        row.label(text="Settings:")

        row = layout.row()
        row.prop(self.properties, "align_model")
        row = layout.row()
        row.prop(self.properties, "option_flip_yz")
        row.prop(self.properties, "option_scale")
        layout.separator()

        row = layout.row()
        row.label(text="--------- Experimental ---------")
        layout.separator()

        row = layout.row()
        row.label(text="Scene:")

        row = layout.row()
        row.prop(self.properties, "option_export_scene")
        row.prop(self.properties, "option_embed_meshes")

        row = layout.row()
        row.prop(self.properties, "option_lights")
        row.prop(self.properties, "option_cameras")
        layout.separator()

        row = layout.row()
        row.label(text="Animation:")

        row = layout.row()
        row.prop(self.properties, "option_animation_morph")
        row = layout.row()
        row.prop(self.properties, "option_animation_skeletal")
        row = layout.row()
        row.prop(self.properties, "option_frame_index_as_time")
        row = layout.row()
        row.prop(self.properties, "option_frame_step")
        layout.separator()

        row = layout.row()
        row.label(text="Settings:")

        row = layout.row()
        row.prop(self.properties, "option_all_meshes")

        row = layout.row()
        row.prop(self.properties, "option_copy_textures")

        row = layout.row()
        row.prop(self.properties, "option_url_base_html")

        layout.separator()


# ################################################################
# Common
# ################################################################

def menu_func_export(self, context):
    default_path = bpy.data.filepath.replace(".blend", ".json")
    self.layout.operator(ExportTHREEJS.bl_idname, \
        text="Blend4Avango (.json)").filepath = default_path

def register():
    bpy.utils.register_class(ExportTHREEJS)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ExportTHREEJS)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

