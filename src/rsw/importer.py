import os
import bpy
import bpy_extras
import math
from mathutils import Vector, Matrix, Quaternion
from bpy.props import StringProperty, BoolProperty, FloatProperty
from ..rsw.reader import RswReader
from ..gnd.reader import GndReader  # Adicionado para ler as dimensões do terreno
from ..gnd.importer import GndImportOptions, GND_OT_ImportOperator
from ..rsm.importer import RsmImportOptions, RSM_OT_ImportOperator

class RSW_OT_ImportOperator(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = 'io_scene_rsw.rsw_import'
    bl_label = 'Import Ragnarok Online RSW'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    filename_ext = ".rsw"

    filter_glob: StringProperty(
        default="*.rsw",
        options={'HIDDEN'},
        maxlen=255,
    )

    data_path: StringProperty(
        default='',
        maxlen=255,
        subtype='DIR_PATH'
    )

    should_import_gnd: BoolProperty(default=True)
    should_import_models: BoolProperty(default=True)

    def execute(self, context):
        # Load the RSW file
        rsw = RswReader.from_file(self.filepath)
        data_path = os.path.dirname(self.filepath)
        name = os.path.basename(self.filepath)

        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)

        # 1. Primeiro, lemos o terreno silenciosamente para pegar as dimensões e calcular o centro real
        gnd_path = os.path.join(data_path, rsw.gnd_file)
        try:
            gnd = GndReader.from_file(gnd_path)
            map_center_x = (gnd.width * gnd.scale) / 2.0
            map_center_y = (gnd.height * gnd.scale) / 2.0
        except FileNotFoundError:
            self.report({'ERROR'}, 'GND file ({}) could not be found for offset calculation.'.format(rsw.gnd_file))
            return {'CANCELLED'}

        # Load the GND file and import it into the scene.
        if self.should_import_gnd:
            try:
                options = GndImportOptions()
                gnd_object = GND_OT_ImportOperator.import_gnd(gnd_path, options)
                try:
                    collection.objects.link(gnd_object)
                except RuntimeError:
                    pass
            except Exception as e:
                print("Erro ao importar GND:", e)

        if self.should_import_models:
            # Load up all the RSM files and import them into the scene.
            models_path = os.path.join(data_path, 'model')
            rsm_options = RsmImportOptions()
            model_data = dict()
            
            for rsw_model in rsw.models:
                if rsw_model.filename in model_data:
                    model_object = bpy.data.objects.new(rsw_model.name, model_data[rsw_model.filename])
                else:
                    filename = rsw_model.filename.replace('\\', os.path.sep)
                    rsm_path = os.path.join(models_path, filename)
                    try:
                        model_object = RSM_OT_ImportOperator.import_rsm(rsm_path, rsm_options)
                        model_data[rsw_model.filename] = model_object.data
                    except FileNotFoundError:
                        print('RSM file ({}) could not be found. Pulando...'.format(filename))
                        continue 

                try:
                    collection.objects.link(model_object)
                except RuntimeError:
                    pass

                # --- APLICAÇÃO DO OFFSET GLOBAL E TRANSFORMAÇÕES ---
                
                # Translação: Soma o centro do mapa com a coordenada original do modelo
                x, z, y = rsw_model.position
                model_object.location += Vector((x + map_center_x, y + map_center_y, -z))

                # Rotação
                rx, rz, ry = rsw_model.rotation
                model_object.rotation_euler = (math.radians(rx), math.radians(ry), math.radians(-rz))

                # Escala: Atribuição direta e absoluta
                sx, sz, sy = rsw_model.scale
                model_object.scale = (sx, sy, sz)

        return {'FINISHED'}

    @staticmethod
    def menu_func_import(self, context):
        self.layout.operator(RSW_OT_ImportOperator.bl_idname, text='Ragnarok Online RSW (.rsw)')