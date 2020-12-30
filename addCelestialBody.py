import bpy
from bpy.props import *
from .CreateIcosphere import *
from . import Celestial_Body
import mathutils

planetlist = []
class Stop_Simulation(bpy.types.Operator):
    """Stop Simulation"""
    bl_idname = "stop.simulationcb"
    bl_label = "Stop Simulation"
    

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        stop_play()
        return {'FINISHED'}

class Start_Simulation(bpy.types.Operator):
    """Start Simulation"""
    bl_idname = "start.simulationcb"
    bl_label = "Start Simulation"
    

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        start_play()
        return {'FINISHED'}

class SimplePropConfirmOperator(bpy.types.Operator):
    """Add Celestial Body?"""
    bl_idname = "my_category.custom_confirm_dialog"
    bl_label = "Add Celestial Body"
    bl_options = {'REGISTER', 'INTERNAL'}

    def update_func(self, context):
        #print("my test function", self)
        self.my_color = (0.5,0.5,0.9, 1.0) # Alpha

    my_enum : bpy.props.EnumProperty(
        items = (("RND", "Planet", ""),("SET", "Moon", "")),
        update = update_func)

    my_color : bpy.props.FloatVectorProperty(
        subtype='COLOR', 
        min=0.0, 
        max=1.0,
        size=4) # Alpha

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        add_object(self, context)
        self.report({'INFO'}, "%s added"%"Planet")
        planetlist.append(Celestial_Body.celestial_body(bpy.context.object.Mass,mathutils.Vector((bpy.context.object.Initial_Velocity[0],bpy.context.object.Initial_Velocity[1],bpy.context.object.Initial_Velocity[2])),bpy.context.object.name,"ObjPrueba"))
        return {'FINISHED'}

    '''
    def check(self, context): 
        return True
    '''

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        row = self.layout
        row.prop(self, "my_enum", text="Property A")
        if self.my_enum == "SET":
            row.prop(self, "my_color", text="Property B")

class CELESTIAL_BODY_PT_panel(bpy.types.Panel):
    bl_label = "CelestialBody Panel"
    bl_idname = "CELESTIAL_BODY_PT_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "CelestialBody"
    bl_context = "objectmode"
    bpy.types.Object.Name = StringProperty(name ="CB1")
    bpy.types.Object.Mass = FloatProperty(default=5.0 )
    bpy.types.Object.Initial_Velocity = IntVectorProperty(name ="Initial_Valocity")
    def draw(self, context):
        try:
            obj = context.object
            layout = self.layout
            layout.operator(SimplePropConfirmOperator.bl_idname)
            row = layout.row()  
            row.label(text="", icon='MATSPHERE')
            row.prop(obj, "name")
            row = layout.row()
            row.label(text="", icon='UGLYPACKAGE')
            row.prop(context.object, "Mass")
            row = layout.row()
            row.label(text="", icon='OBJECT_ORIGIN')
            row.prop(context.object, "Initial_Velocity")
            row = layout.row()
            row.label(text="", icon='OBJECT_ORIGIN')
            row.operator("start.simulationcb")
            row = layout.row()
            row.label(text="", icon='OBJECT_ORIGIN')
            row.operator("stop.simulationcb")
        except:
            pass
        #row.operator("speech_to_text.audio")
    
    #print(bpy.data.objects["Icosphere"].Name)
def start_play():
    bpy.app.handlers.frame_change_pre.append(my_handler)
def stop_play():
    bpy.app.handlers.frame_change_pre.remove(my_handler)
def register():
    bpy.utils.register_class(CELESTIAL_BODY_PT_panel)
    bpy.utils.register_class(SimplePropConfirmOperator)
    bpy.utils.register_class(Start_Simulation)
    bpy.utils.register_class(Stop_Simulation)

def unregister():
    bpy.utils.unregister_class(CELESTIAL_BODY_PT_panel)
    bpy.utils.unregister_class(SimplePropConfirmOperator) 
    bpy.utils.unregister_class(Start_Simulation) 
    bpy.utils.unregister_class(Stop_Simulation) 

def my_handler(Scene):
    for i in planetlist:
        i.UpdateVariables(bpy.data.objects[i.name].Mass,mathutils.Vector((bpy.data.objects[i.name].Initial_Velocity[0],bpy.data.objects[i.name].Initial_Velocity[1],bpy.data.objects[i.name].Initial_Velocity[2])))
        i.UpdateDicc()
        print("act")



