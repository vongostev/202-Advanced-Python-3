from numba import njit, float64, types, prange
from numba.extending import typeof_impl, type_callable, models, register_model, make_attribute_wrapper, lower_builtin, unbox, NativeValue, box
from numba.core import cgutils
from numba.experimental import jitclass

#Класс со свойствами материалов
class Material(object):
    def __init__(self, a):
        self.H = a[0]
        self.Ksi = a[1]
        self.Ro = a[2]
        self.L = a[3]
        self.Type = a[4]
        self.Tc = a[5]
        self.Gb_FS = a[6]
        self.N = a[7]

#Код, необходимый, чтобы numba могла использовать класс
#https://numba.pydata.org/numba-doc/latest/extending/interval-example.html
class MaterialType(types.Type):
    def __init__(self):
        super(MaterialType, self).__init__(name='Material')

material_type=MaterialType()

@typeof_impl.register(Material)
def typeof_index(val, c):
    return material_type

@type_callable(Material)
def type_material(context):
    def typer(a):
        if isinstance(a, types.Tuple):
            return material_type
    return typer

@register_model(MaterialType)
class MaterialModel(models.StructModel):
    def __init__(self, dmm, fe_type):
        members = [
            ('H', types.float64),
            ('Ksi', types.float64),
            ('Ro', types.float64),
            ('L', types.float64),
            ('Type', types.float64),
            ('Tc', types.float64),
            ('Gb_FS', types.float64),
            ('N', types.float64),
            ]
        models.StructModel.__init__(self, dmm, fe_type, members)

make_attribute_wrapper(MaterialType, 'H', 'H')
make_attribute_wrapper(MaterialType, 'Ksi', 'Ksi')
make_attribute_wrapper(MaterialType, 'Ro', 'Ro')
make_attribute_wrapper(MaterialType, 'L', 'L')
make_attribute_wrapper(MaterialType, 'Type', 'Type')
make_attribute_wrapper(MaterialType, 'Tc', 'Tc')
make_attribute_wrapper(MaterialType, 'Gb_FS', 'Gb_FS')
make_attribute_wrapper(MaterialType, 'N', 'N')

@lower_builtin(Material, types.Float, types.Float, types.Float, types.Float, types.Float, types.Float, types.Float, types.Float)
def impl_interval(context, builder, sig, args):
    typ = sig.return_type
    H, Ksi, Ro, L, Type, Tc, Gb_FS, N = args
    material = cgutils.create_struct_proxy(typ)(context, builder)
    material.H = H
    material.Ksi = Ksi
    material.Ro = Ro
    material.L = L
    material.Type = Type
    material.Tc = Tc
    material.Gb_FS = Gb_FS
    material.N = N
    return material._getvalue()

@unbox(MaterialType)
def unbox_material(typ, obj, c):

    H_obj = c.pyapi.object_getattr_string(obj, "H")
    Ksi_obj = c.pyapi.object_getattr_string(obj, "Ksi")
    Ro_obj = c.pyapi.object_getattr_string(obj, "Ro")
    L_obj = c.pyapi.object_getattr_string(obj, "L")
    Type_obj = c.pyapi.object_getattr_string(obj, "Type")
    Tc_obj = c.pyapi.object_getattr_string(obj, "Tc")
    Gb_FS_obj = c.pyapi.object_getattr_string(obj, "Gb_FS")
    N_obj = c.pyapi.object_getattr_string(obj, "N")
    material = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    material.H = c.pyapi.float_as_double(H_obj)
    material.Ksi = c.pyapi.float_as_double(Ksi_obj)
    material.Ro = c.pyapi.float_as_double(Ro_obj)
    material.L = c.pyapi.float_as_double(L_obj)
    material.Type = c.pyapi.float_as_double(Type_obj)
    material.Tc = c.pyapi.float_as_double(Tc_obj)
    material.Gb_FS = c.pyapi.float_as_double(Gb_FS_obj)
    material.N = c.pyapi.float_as_double(N_obj)
    c.pyapi.decref(H_obj)
    c.pyapi.decref(Ksi_obj)
    c.pyapi.decref(Ro_obj)
    c.pyapi.decref(L_obj)
    c.pyapi.decref(Type_obj)
    c.pyapi.decref(Tc_obj)
    c.pyapi.decref(Gb_FS_obj)
    c.pyapi.decref(N_obj)
    is_error = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(material._getvalue(), is_error=is_error)

@box(MaterialType)
def box_Material(typ, val, c):

    Material = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val)
    H_obj = c.pyapi.float_from_double(Material.H)
    Ksi_obj = c.pyapi.float_from_double(Material.Ksi)
    Ro_obj = c.pyapi.float_from_double(Material.Ro)
    L_obj = c.pyapi.float_from_double(Material.L)
    Type_obj = c.pyapi.float_from_double(Material.Type)
    Tc_obj = c.pyapi.float_from_double(Material.Tc)
    Gb_FS_obj = c.pyapi.float_from_double(Material.Gb_FS)
    N_obj = c.pyapi.float_from_double(Material.N)
    class_obj = c.pyapi.unserialize(c.pyapi.serialize_object(Material))
    res = c.pyapi.call_function_objargs(class_obj, (H_obj, Ksi_obj, Ro_obj, L_obj, Type_obj, Tc_obj, Gb_FS_obj, N_obj))
    c.pyapi.decref(H_obj)
    c.pyapi.decref(Ksi_obj)
    c.pyapi.decref(Ro_obj)
    c.pyapi.decref(L_obj)
    c.pyapi.decref(Type_obj)
    c.pyapi.decref(Tc_obj)
    c.pyapi.decref(Gb_FS_obj)
    c.pyapi.decref(N_obj)
    c.pyapi.decref(class_obj)
    return res