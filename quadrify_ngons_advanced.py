bl_info = {
    "name": "Quadrify N-Gons Advanced",
    "author": "BoogieTheUnit",
    "version": (1, 0, 0),
    "blender": (4, 2, 4),
    "location": "View3D > N-Panel > Quadrify",
    "description": "Advanced n-gon to quad conversion tool",
    "category": "Mesh",
}

import bpy

class QuadrifyNgonsOperator(bpy.types.Operator):
    """Convert N-Gons to Quads with multiple methods"""
    bl_idname = "mesh.quadrify_ngons_advanced"
    bl_label = "Quadrify N-Gons (Advanced)"
    bl_options = {'REGISTER', 'UNDO'}

    method: bpy.props.EnumProperty(
        name="Method",
        description="Choose quadrification method",
        items=[
            ('TRIS_TO_QUADS', "Triangulate + Tris to Quads", "Standard conversion"),
            ('GRID_FILL', "Grid Fill (Planar)", "Use Grid Fill for large n-gons"),
            ('KNIFE_SUBDIVIDE', "Knife Subdivide", "Subdivide large n-gons with edge loops")
        ],
        default='TRIS_TO_QUADS'
    )
    
    def execute(self, context):
        obj = bpy.context.object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No valid mesh object selected!")
            return {'CANCELLED'}
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER', extend=False)
        
        if self.method == 'TRIS_TO_QUADS':
            bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
            bpy.ops.mesh.tris_convert_to_quads(face_threshold=1.5708, shape_threshold=1.5708)
        
        elif self.method == 'GRID_FILL':
            bpy.ops.mesh.fill_grid()  # Works well for planar n-gons
        
        elif self.method == 'KNIFE_SUBDIVIDE':
            bpy.ops.mesh.knife_project()  # Requires an appropriate cutter object
        
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

class QuadrifyNgonsPanel(bpy.types.Panel):
    """UI Panel for Quadrify N-Gons"""
    bl_label = "Quadrify N-Gons"
    bl_idname = "VIEW3D_PT_quadrify_ngons"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Quadrify'
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Select Quadrification Method:")
        layout.operator_menu_enum("mesh.quadrify_ngons_advanced", "method")

# Registration
classes = [QuadrifyNgonsOperator, QuadrifyNgonsPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
