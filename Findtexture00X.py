# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Find texture00X in material",
    "author": "Ron Haertel (ronh991)",
    "version": (0, 1, 0),
    "blender": (3, 1, 2),
    "location": "Material Panel",
    "description": "Display the objects that use a material with texture name suffix 00X.",
    "category": "Material"}


import bpy

#------------------------------------------------------
# Action class
#------------------------------------------------------
class MSFS_OT_RunAction(bpy.types.Operator):
    bl_idname = "object.select_node"
    bl_label = "Select"
    bl_description = "Select objects with material texture name 00X"
    param_a: bpy.props.StringProperty(name = "param_a")
    param_b: bpy.props.StringProperty(name = "param_b")

    #------------------------------
    # Execute
    #------------------------------
    def execute(self, context):
        print("params")
        print("self.param_a:",self.param_a)
        print("self.param_b:",self.param_b)
        #self.report({"INFO"},"%s %s"%(self.param_a,self.param_b))
        # Get current material
        #currentMaterial = bpy.context.object.active_material
        
        #currentMaterial = bpy.context.active_object.active_material
        currentMaterial = []
        tempList= []
        tempList.append(self.param_a)
        tempList.append(self.param_b)
        currentMaterial.append(tempList)
    
        print("\n\nPARSING OBJECTS\n")
        bpy.context.active_object.select_set(False)
        # Loop material list
        for obj in context.scene.objects:
            
            #print("Obj: {0}".format(obj.name))
            obj.select_set(False)
            
            for slot in obj.material_slots:
                #print("Material: {0}".format(slot.name))
            
                if (slot.name == self.param_a and
                    context.view_layer.objects.get(obj.name) is not None):
                    print("Obj: {0}".format(obj.name))
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj     
                    #obj.select = True

        
        return {'FINISHED'}
        
            
#------------------------------------------------------
# UI Class
#------------------------------------------------------
class MSFS_PT_PanelUI(bpy.types.Panel):
    bl_label = "Material relationship"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"    
    
    #------------------------------
    # Draw UI
    #------------------------------
    def draw(self, context):
        
        #print("\n\n\n\n\nCurrMaterial: {0}\n".format(bpy.context.active_object.active_material.name))
        
        # for material check for texture nodes
        # if it has a digit check if the original exists
        # if original has also digits remove
        
        # Loop material list
        matList = []
        #textList = []
        for mat in bpy.data.materials:
            if mat.node_tree:
                for n in mat.node_tree.nodes:
                    if n.type == 'TEX_IMAGE':
                        if n.image is not None and n.image.name[-3:].isdigit():
                            #print(mat.name,'has an image node with texture.00X')
                            #name = n.image.name[:-4]
                            tempList = []
                            tempList.append(mat)
                            tempList.append(n.image.name)
                            matList.append(tempList)
                            #textList.append(n.image.name)
                            #exists = False
                            #for img in bpy.data.images:
                            #    if img.name in name:
                            #        exists = True
                            #if exists:
                            #    n.image = bpy.data.images[name]
                            #else:
                            #    n.image.name = name
                            
        layout = self.layout
        for currentMaterial in matList:
            
            if (currentMaterial[0].name is not None):
                
                # Button
                row = layout.row(align=False)
                
                props = row.operator("object.select_node", icon="SELECT_SET")
                row.label(text=" ")
                
                #row.operator("object.select_material", icon="SELECT_SET")
                #row.label(text=" ")
                props.param_a = currentMaterial[0].name
                props.param_b = currentMaterial[1]
                
                # info
                row = layout.row()
                
                # Get current material
                #currentMaterial = bpy.context.object.active_material
                #currentMaterial = bpy.context.active_object.active_material
                
                # Loop obj list
                objList = []
                
                #print("Obj List Here:\n")
                
                for obj in bpy.context.scene.objects:
                    for slot in obj.material_slots:
                        if slot.material == currentMaterial[0]:
                            objList.append(obj) 
                             
                            print("Found ", obj.name+"\n")
                
                # Display result
                str1 = currentMaterial[0].name + " texture name - " + currentMaterial[1] + "  (" + str(len(objList)) + " relationship)"
                row.label(text=str1, icon='MATERIAL_DATA')
                
                box = layout.box()
                for obj in bpy.context.scene.objects:
                    for slot in obj.material_slots:
                        if slot.material == currentMaterial[0]:
                            #print("current material ", currentMaterial[0])
                            objList.append(obj)  
                            row = box.row()
                            buf = obj.name
                            if (len(obj.material_slots) > 1):
                                buf = buf + "  (" + str(len(obj.material_slots)) + " materials)"
                            
                            row.label(text=buf, icon='OBJECT_DATAMODE')          
                
                
            else:
                buf = "** No selected material **"
                layout.label(text=buf, icon='MATERIAL_DATA')
            
#------------------------------------------------------
# Registration
#------------------------------------------------------
def register():
    bpy.utils.register_class(MSFS_OT_RunAction)
    bpy.utils.register_class(MSFS_PT_PanelUI)
    

def unregister():
    bpy.utils.unregister_class(MSFS_OT_RunAction)
    bpy.utils.unregister_class(MSFS_PT_PanelUI)


if __name__ == "__main__":
    register()
