"""accelpy Fortran Accelerator module"""

import abc

from uuid import uuid4
from accelpy.accel import AccelDataBase
from accelpy.kernel import KernelBase
from accelpy.util import fortline_pack, f_dtypemap, getname_varmap
from ctypes import c_int32, c_int64, c_float, c_double


##########################
#  Kernel Code templates
##########################

t_module = """
MODULE {modname}
    USE, INTRINSIC :: ISO_C_BINDING
    IMPLICIT NONE

{datavars}

END MODULE
"""

t_main = """
{include}

{varmap}

INTEGER (C_INT64_T) FUNCTION accelpy_start() BIND(C, name="accelpy_start")

    USE, INTRINSIC :: ISO_C_BINDING
    USE {modname}, ONLY : {usevarnames}
    IMPLICIT NONE

    accelpy_start = accelpy_kernel({usevarnames})

CONTAINS

{kernel}

END FUNCTION

INTEGER (C_INT64_T) FUNCTION accelpy_stop() BIND(C, name="accelpy_stop")
    USE, INTRINSIC :: ISO_C_BINDING
    USE {modname}, ONLY : {usevarnames}
    IMPLICIT NONE

    accelpy_stop = 0

END FUNCTION
"""

t_kernel = """
INTEGER (C_INT64_T) FUNCTION accelpy_kernel({varnames})
    USE, INTRINSIC :: ISO_C_BINDING
    IMPLICIT NONE

    {typedecls}

    {spec}

    accelpy_kernel = 0

END FUNCTION
"""

t_varmap = """
INTEGER (C_INT64_T) FUNCTION {funcname} (data) BIND(C, name="{funcname}")
    USE, INTRINSIC :: ISO_C_BINDING
    USE {modname}, ONLY : {varname}
    IMPLICIT NONE

    {dtype}, DIMENSION({bound}), INTENT(IN), TARGET :: data

    {varname} => data

    {funcname} = 0

END FUNCTION
"""

t_varmap_scalar = """
INTEGER (C_INT64_T) FUNCTION {funcname} (data) BIND(C, name="{funcname}")
    USE, INTRINSIC :: ISO_C_BINDING
    USE {modname}, ONLY : {varname}
    IMPLICIT NONE

    {dtype}, DIMENSION(1), INTENT(IN) :: data

    {varname} = data(1)

    {funcname} = 0

END FUNCTION
"""

class FortranKernel(KernelBase):

    name = "fortran"
    lang = "fortran"

#    dtypemap = {
#        "int32": ["INTEGER (C_INT32_T)", c_int32],
#        "int64": ["INTEGER (C_INT64_T)", c_int64],
#        "float32": ["REAL (C_FLOAT)", c_float],
#        "float64": ["REAL (C_DOUBLE)", c_double]
#    }

    def gen_code(self, compiler):

        macros = {}
        includes = self.add_includes()

        modname  = "mod_" + uuid4().hex[:10]

        module_fmt = {
            "modname": modname,
            "datavars": self._get_datavars(),
        }
        module = t_module.format(**module_fmt)

        main_fmt = {
            "modname":modname,
            "varmap":self._gen_varmap(modname),
            "kernel":self._gen_kernel(),
            "usevarnames":self._gen_usevars(),
            "include":self.get_include(),
        }
        main = t_main.format(**main_fmt)

        #print(module)
        #print(main)
        #import pdb; pdb.set_trace()

        return includes + [module, main], macros

    def get_dtype(self, arg):
        return f_dtypemap[arg["data"].dtype.name][0]

    def _get_datavars(self):

        out = []

        for arg in self.data:
            ndim = arg["data"].ndim
            dtype = self.get_dtype(arg)
            varname = arg["curname"]

            if ndim > 0:
                bound = ",".join([":"]*ndim)
                out.append("%s, DIMENSION(%s), POINTER :: %s" % (dtype, bound, varname))

            else:
                out.append("%s :: %s" % (dtype, varname))

        return "\n".join(out)

    def _gen_varmap(self, modname):

        out = []

        for arg in self.data:
            dtype = self.get_dtype(arg)
            funcname = getname_varmap(arg)
            ndim = arg["data"].ndim

            if ndim > 0:
                bound = ",".join([str(s) for s in arg["data"].shape])
                out.append(t_varmap.format(funcname=funcname, varname=arg["curname"],
                            modname=modname, bound=bound, dtype=dtype))
            else:
                out.append(t_varmap_scalar.format(funcname=funcname, modname=modname,
                            varname=arg["curname"], dtype=dtype))

        return "\n".join(out)

    def _gen_kernel(self):

        _names = []
        typedecls = []

        for arg in self.data:
            ndim = arg["data"].ndim
            dtype = self.get_dtype(arg)
            varname = arg["curname"]

            _names.append(varname)

            if ndim > 0:
                if ("attrspec" in self.section.kwargs and
                    varname in self.section.kwargs["attrspec"] and
                    "dimension" in self.section.kwargs["attrspec"][varname]):
                    bound = self.section.kwargs["attrspec"][varname]["dimension"]

                else:
                    bound = ",".join([":"]*ndim)


                typedecls.append("%s, DIMENSION(%s), INTENT(INOUT) :: %s" % (
                            dtype, bound, varname))

            else:
                typedecls.append("%s, INTENT(IN) :: %s" % (dtype, varname))

        names = fortline_pack(_names)

        return t_kernel.format(spec="\n".join(self.section.body),
                typedecls="\n".join(typedecls), varnames="\n".join(names))

    def _gen_usevars(self):

        names = []

        for arg in self.data:

            names.append(arg["curname"])

        lines = [""]
        maxlen = 72

        for name in names:
            if len(lines[-1]) + len(name) > maxlen:

                lines[-1] += " &"
                lines.append("        &, %s" % name)

            elif lines[-1] == "":
                lines[-1] += name

            else:
                lines[-1] += ", " + name

        return "\n".join(lines)

class OpenmpFortranKernel(FortranKernel):
    name = "openmp_fortran"

class OpenaccFortranKernel(FortranKernel):
    name = "openacc_fortran"

class OmptargetFortranKernel(OpenmpFortranKernel):
    name = "omptarget_fortran"

OmptargetFortranKernel.avails[OmptargetFortranKernel.name] = OmptargetFortranKernel
OpenaccFortranKernel.avails[OpenaccFortranKernel.name] = OpenaccFortranKernel
OpenmpFortranKernel.avails[OpenmpFortranKernel.name] = OpenmpFortranKernel
FortranKernel.avails[FortranKernel.name] = FortranKernel



##########################
#  AccelData Code templates
##########################

t_accdata = """
MODULE {modname}
    USE, INTRINSIC :: ISO_C_BINDING
    IMPLICIT NONE

{modvardecls}

PUBLIC {modpublics}

CONTAINS

INTEGER (C_INT64_T) FUNCTION dataenter({enterargs}) BIND(C, name="dataenter")
    USE, INTRINSIC :: ISO_C_BINDING

    {entertypedecls}

    {enterassigns}

    {enterdir} {entermaps}

    dataenter = 0

END FUNCTION

INTEGER (C_INT64_T) FUNCTION dataexit() BIND(C, name="dataexit")
    USE, INTRINSIC :: ISO_C_BINDING

    {exitdir} {exitmaps}

    dataexit = 0

END FUNCTION

END MODULE
"""

class FortranAccelData(AccelDataBase):

    name = "fortran"
    lang = "fortran"

#    dtypemap = {
#        "int32": ["INTEGER (C_INT32_T)", c_int32],
#        "int64": ["INTEGER (C_INT64_T)", c_int64],
#        "float32": ["REAL (C_FLOAT)", c_float],
#        "float64": ["REAL (C_DOUBLE)", c_double]
#    }

    def get_dtype(self, arg):
        return f_dtypemap[arg["data"].dtype.name][0]

    def gen_code(self, compiler):
        pass

class OpenmpFortranAccelData(FortranAccelData):
    name = "openmp_fortran"


class FortranOpenAccelData(FortranAccelData):

    offload = True
    
    @abc.abstractmethod
    def clause_mapto(self, mapto):
        pass

    @abc.abstractmethod
    def clause_maptofrom(self, maptofrom):
        pass

    @abc.abstractmethod
    def clause_mapalloc(self, mapalloc):
        pass

    @abc.abstractmethod
    def clause_mapfrom(self, mapfrom):
        pass

    @abc.abstractmethod
    def enterdirect(self):
        pass

    @abc.abstractmethod
    def exitdirect(self):
        pass

    def gen_code(self, compiler):

        macros = {}

        modname  = "mod_" + uuid4().hex[:10]

        modvardecls = []
        modpublics = []
        enterargs = []
        entertypedecls = []
        enterassigns = []
        mapto = []
        maptofrom = []
        mapalloc = []
        mapfrom = []

        for item in self.mapto:
            ndim = item["data"].ndim
            dtype = self.get_dtype(item)
            lname = "apy_acceldata_lvar_" + str(item["index"])
            gname = "apy_acceldata_gvar_" + str(item["index"])

            item["modname"] = gname

            enterargs.append(lname)
            shape = ",".join([":"] * ndim)
            mapto.append("%s(%s)" % (gname, shape))
            bound = ",".join([str(s) for s in item["data"].shape])
            entertypedecls.append("%s, DIMENSION(%s), INTENT(INOUT), TARGET :: %s" % (
                            dtype, bound, lname))

            modpublics.append(gname)
            bound = ",".join([":"]*ndim)
            modvardecls.append("%s, DIMENSION(%s), POINTER :: %s" % (
                            dtype, bound, gname))

            enterassigns.append("%s => %s" % (gname, lname))

        for item in self.maptofrom:
            ndim = item["data"].ndim
            dtype = self.get_dtype(item)
            lname = "apy_acceldata_lvar_" + str(item["index"])
            gname = "apy_acceldata_gvar_" + str(item["index"])

            item["modname"] = gname

            enterargs.append(lname)
            shape = ",".join([":"] * ndim)
            maptofrom.append("%s(%s)" % (gname, shape))
            bound = ",".join([str(s) for s in item["data"].shape])
            entertypedecls.append("%s, DIMENSION(%s), INTENT(INOUT), TARGET :: %s" % (
                            dtype, bound, lname))

            modpublics.append(gname)
            bound = ",".join([":"]*ndim)
            modvardecls.append("%s, DIMENSION(%s), POINTER :: %s" % (
                            dtype, bound, gname))

            enterassigns.append("%s => %s" % (gname, lname))

        for item in self.mapalloc:
            ndim = item["data"].ndim
            dtype = self.get_dtype(item)
            lname = "l" + str(item["index"])
            gname = "g" + str(item["index"])

            item["modname"] = gname

            enterargs.append(lname)
            shape = ",".join([":"] * ndim)
            mapalloc.append("%s(%s)" % (gname, shape))
            bound = ",".join([str(s) for s in item["data"].shape])
            entertypedecls.append("%s, DIMENSION(%s), INTENT(INOUT), TARGET :: %s" % (
                            dtype, bound, lname))

            modpublics.append(gname)
            bound = ",".join([":"]*ndim)
            modvardecls.append("%s, DIMENSION(%s), POINTER :: %s" % (
                            dtype, bound, gname))

            enterassigns.append("%s => %s" % (gname, lname))

        for item in self.mapfrom:
            ndim = item["data"].ndim
            dtype = self.get_dtype(item)
            lname = "apy_acceldata_lvar_" + str(item["index"])
            gname = "apy_acceldata_gvar_" + str(item["index"])

            item["modname"] = gname

            enterargs.append(lname)
            shape = ",".join([":"] * ndim)
            mapfrom.append("%s(%s)" % (gname, shape))
            mapalloc.append("%s(%s)" % (gname, shape))
            bound = ",".join([str(s) for s in item["data"].shape])
            entertypedecls.append("%s, DIMENSION(%s), INTENT(INOUT), TARGET :: %s" % (
                            dtype, bound, lname))

            modpublics.append(gname)
            bound = ",".join([":"]*ndim)
            modvardecls.append("%s, DIMENSION(%s), POINTER :: %s" % (
                            dtype, bound, gname))

            enterassigns.append("%s => %s" % (gname, lname))

        entermaps = "%s %s %s" % (self.clause_mapto(mapto),
                        self.clause_maptofrom(maptofrom, True),
                        self.clause_mapalloc(mapalloc))
        exitmaps = "%s %s" % (self.clause_maptofrom(maptofrom, False),
                                self.clause_mapfrom(mapfrom))

        enterdir = self.enterdirect()
        exitdir = self.exitdirect()

        acceldata_fmt = {
            "modname": modname,
            "modvardecls": "\n".join(modvardecls),
            "modpublics": ", ".join(modpublics),
            "enterargs": ", ".join(enterargs),
            "entertypedecls": "\n".join(entertypedecls),
            "enterassigns": "\n".join(enterassigns),
            "enterdir": enterdir,
            "entermaps": entermaps,
            "exitdir": exitdir,
            "exitmaps": exitmaps,
        }

        acceldata = t_accdata.format(**acceldata_fmt)

        #print(acceldata)
        #import pdb; pdb.set_trace()

        return [acceldata], macros


class OpenaccFortranAccelData(FortranOpenAccelData):
    name = "openacc_fortran"

    def clause_mapto(self, mapto):
        return "copyin(%s)" % ", ".join(mapto) if mapto else ""

    def clause_maptofrom(self, maptofrom, isenter):

        if isenter:
            return "copyin(%s)" % ", ".join(maptofrom) if maptofrom else ""

        else:
            return "copyout(%s)" % ", ".join(maptofrom) if maptofrom else ""

    def clause_mapalloc(self, mapalloc):
        return "create(%s)" % ", ".join(mapalloc) if mapalloc else ""

    def clause_mapfrom(self, mapfrom):
        return "copyout(%s)" % ", ".join(mapfrom) if mapfrom else ""

    def enterdirect(self):
        return "!$acc enter data"

    def exitdirect(self):
        return "!$acc exit data"

class OmptargetFortranAccelData(FortranOpenAccelData):
    name = "omptarget_fortran"

    def clause_mapto(self, mapto):
        return "map(to: %s)" % ", ".join(mapto) if mapto else ""

    def clause_maptofrom(self, maptofrom, isenter):
        if isenter:
            return ("map(tofrom: %s)" % ", ".join(maptofrom)
                    if maptofrom else "")
        else:
            return ""

    def clause_mapalloc(self, mapalloc):
        return "map(alloc: %s)" % ", ".join(mapalloc) if mapalloc else ""

    def clause_mapfrom(self, mapfrom):
        return "map(from: %s)" % ", ".join(mapfrom) if mapfrom else ""

    def enterdirect(self):
        return "!$omp target enter data"

    def exitdirect(self):
        return "!$omp target exit data"


AccelDataBase.avails[OmptargetFortranAccelData.name] = OmptargetFortranAccelData
AccelDataBase.avails[OpenaccFortranAccelData.name] = OpenaccFortranAccelData
AccelDataBase.avails[OpenmpFortranAccelData.name] = OpenmpFortranAccelData
AccelDataBase.avails[FortranAccelData.name] = FortranAccelData
