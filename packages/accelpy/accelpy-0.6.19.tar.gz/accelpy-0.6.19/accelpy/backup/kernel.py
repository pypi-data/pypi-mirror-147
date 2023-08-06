"""accelpy Kernel module"""


import os, abc, time, threading, shutil, numpy, tempfile

from ctypes import c_int64
from numpy.ctypeslib import ndpointer, load_library
from collections import OrderedDict

from accelpy.const import (version, NOCACHE, MEMCACHE, FILECACHE, NODEBUG,
                            MINDEBUG, MAXDEBUG, NOPROF, MINPROF, MAXPROF,
                            accel_priority)
from accelpy.util import (Object, gethash, get_config, set_config,
                            pack_arguments, getname_varmap)
from accelpy.spec import Spec
from accelpy.compiler import Compiler, get_compilers
from accelpy.cache import slib_cache


class Task(Object):

    def __init__(self, liblang, libpath, bldpath):

        self.liblang = liblang
        self.libpath = libpath
        self.bldpath = bldpath
        self.synched = False

#    def __enter__(self, *data, specenv={}, timeout=None):
#        self.timeout = timeout
#        self.launch(*data, specenv=specenv)
#
#        return self
#
#    def __exit__(self, *exc):
#        self.wait(timeout = self.timeout)
#
#        return False

    def run(self, data):

        self.thread = threading.Thread(target=self._start_kernel,
                            args=(data,))
        self.start = time.time()
        self.thread.start()

    def varmap(self, arg, funcname):

        if self.liblang[1] == "cpp":
            flags = ["c_contiguous"]

        elif self.liblang[1] == "fortran":
            flags = ["f_contiguous"]

        else:
            raise Exception("Unknown language: %s" % self.liblang[1])

        # TODO consider to use "numpy.ascontiguousarray"

        datamap = getattr(self.liblang[0], funcname)
        datamap.restype = c_int64
        datamap.argtypes = [ndpointer(arg["data"].dtype, flags=",".join(flags))]

        res = datamap(arg["data"])

        return res

    def _start_kernel(self, data):

        lib = None

        if self.liblang[0] is None:
            if self.libpath is not None and os.path.isfile(self.libpath):
                try:
                    libdir, libname = os.path.split(self.libpath)
                    basename, _ = os.path.splitext(libname)

                    lib = load_library(basename, libdir)
                except:
                    pass

            if (lib is None and self.bldpath is not None and
                    os.path.isfile(self.bldpath)):
                blddir, bldname = os.path.split(self.bldpath)
                basename, _ = os.path.splitext(bldname)

                lib = load_library(basename, blddir)

        if lib is not None:
            with threading.Lock():
                self.liblang[0] = lib

        for arg in data:
            self.varmap(arg, getname_varmap(arg))

        start = getattr(self.liblang[0], "accelpy_start")
        start.restype = c_int64
        start.argtypes = []

        res = start()

        if res != 0:
            raise Exception("kernel returns non-zero: %d" % res)

    def wait(self, timeout=None):

        timeout = max(0, self.start+timeout-time.time()) if timeout else None

        while self.thread.ident is None:
            time.sleep(0.1)
            
        if self.thread.is_alive():
            self.thread.join(timeout=timeout)

        if (self.libpath and self.bldpath and not os.path.isfile(self.libpath)
            and os.path.isfile(self.bldpath)):
            try:
                shutil.copyfile(self.bldpath, self.libpath)

            except FileExistsError:
                pass

        self.synched = True

    def stop(self, timeout=None):

        if not self.synched:
            self.wait(timeout=timeout)

        accstop = getattr(self.liblang[0], "accelpy_stop")
        accstop.restype = c_int64
        accstop.argtypes = []

        res = accstop()

        return res


class KernelBase(Object):

    avails = OrderedDict()

    #def __init__(self, spec, compile=None, debug=NODEBUG):
    def __init__(self, section, data, cache=MEMCACHE, profile=NOPROF, debug=NODEBUG):

        self.section = section
        self.data = data
        self.debug = debug
        self.cache = cache
        self.profile = profile

#        self.spec = spec if isinstance(spec, Spec) else Spec(spec)
#        self.compile = compile
#        self.cachekey = None
#        self.liblang = [None, None]
#
#        if self.spec is None:
#            raise Exception("No kernel spec is found")

    @abc.abstractmethod
    def get_dtype(self, arg):
        pass

    def get_include(self):
        return ""

    def add_includes(self):

        incs = []

        # TODO: implement this
        #import pdb; pdb.set_trace()

        return incs

    @abc.abstractmethod
    def gen_code(self, compiler):
        pass


class Kernel:

    def __init__(self, spec, acctype=None, compile=None, cache=MEMCACHE, profile=0, debug=NODEBUG):

        self.acctype = acctype
        self.name = None
        self._kernel = None

        self.cache = cache
        self.profile = profile
        self.debug = debug
        self.compile = compile
        self.cachekey = None
        self.liblang = [None, None]

        if isinstance(spec, Spec):
            self.spec = spec
        elif spec is not None:
            self.spec = Spec(spec)
        else:
            raise Exception("No kernel spec is found")

        self.tasks = []

    def set_name(self, name):

        if self.acctype is None:
            self.name = name

        elif self.acctype == name:
            self.name = name

        elif isinstance(self.acctype, (list, tuple)) and name in self.acctype:
            self.name = name

        else:
            raise Exception("Can not set Kernel name: (%s | %s)" %
                            (str(self.acctype), name))

    def launch(self, *data, environ={}):

        self.spec.eval_pysection(environ)
        self.data = pack_arguments(data)

        if self.name is None or self._kernel is None:
            self.set_kernel()

        else:
            self.section = self.spec.get_section(self.name)

        if self._kernel is None:
            if self.name is None:
                raise Exception("Kernel type is not defined.")

            else:
                self._kernel = KernelBase.avails[self.name](self.section, self.data)

        if self.debug > 0:
            print("DEBUG: using '%s' kernel" % (self.name))

        self.spec.update_argnames(self.data)
        self.section.update_argnames(self.data)

        keys = [os.uname().release, version, self.name,
                self.compile, self.section.hash()]

        for item in self.data:
            keys.append(item["data"].shape)
            keys.append(item["data"].dtype)

        if self.liblang[0] is None or self.cache < MEMCACHE:
            lang, libpath, bldpath = self.build_sharedlib(gethash(str(keys)))
            self.liblang[0] = None
            self.liblang[1] = lang
            task = Task(self.liblang, libpath, bldpath)

        else:
            task = Task(self.liblang, None, None)

        task.run(self.data)

        self.tasks.append(task)

        return task

    def wait(self, *tasks, timeout=None):

        if len(tasks) > 0:
            for task in tasks:
                task.wait(timeout=timeout)

        else:
            for task in self.tasks:
                task.wait(timeout=timeout)

    def stop(self, timeout=None):

        for task in self.tasks:
            if not task.synched:
                task.wait(timeout=timeout)

            task.stop(timeout=timeout)

    def build_sharedlib(self, ckey):

        errmsgs = []

        compilers = get_compilers(self.name, self._kernel.lang,
                        compile=self.compile, debug=self.debug)

        for comp in compilers:

            cachekey = ckey + "_" + comp.hashkey

            if self.cache >= FILECACHE and cachekey in slib_cache:
                lang, basename, libext, libpath, bldpath = slib_cache[cachekey]
                self.cachekey = cachekey

                return lang, libpath, bldpath

            libdir = os.path.join(get_config("libdir"), comp.vendor, cachekey[:2])

            if not os.path.isdir(libdir):
                try:
                    os.makedirs(libdir)

                except FileExistsError:
                    pass

            basename = cachekey[2:]
            libname = basename + "." + comp.libext
            libpath = os.path.join(libdir, libname)

            if self.cache >= FILECACHE and os.path.isfile(libpath):
                self.cachekey = cachekey
                slib_cache[self.cachekey] = (comp.lang, basename, comp.libext,
                                                    libpath, None)
                return comp.lang, libpath, None

            try:
                codes, macros = self._kernel.gen_code(comp)

                if not os.path.isdir(get_config("blddir")):
                    set_config("blddir", tempfile.mkdtemp())

                bldpath = comp.compile(codes, macros)

                self.cachekey = cachekey
                slib_cache[self.cachekey] = (comp.lang, basename, comp.libext,
                                                    libpath, bldpath)
                return comp.lang, libpath, bldpath

            except Exception as err:
                errmsgs.append(str(err))

        raise Exception("\n".join(errmsgs))


    def set_kernel(self, acctype=None):

        if isinstance(self.acctype, str):
            acctype = (self.acctype,)

        accel = set(KernelBase.avails.keys()) if acctype is None else set(acctype)
        accel &= set(self.spec.list_sections())

        errmsgs = []

        for a in sorted(list(accel), key=(lambda x: accel_priority.index(x))):
            try:
                section = self.spec.get_section(a)
                self._kernel = KernelBase.avails[a](section, self.data, debug=self.debug)
                self.name = self._kernel.name
                self.section = section

                return

            except Exception as err:
                errmsgs.append(repr(err))

        raise Exception("No kernel is available: %s" % "\n".join(errmsgs))


#def Kernel(spec, accel=None, compile=None, cache=MEMCACHE, profile=0, debug=NODEBUG):
#
#    if isinstance(accel, str):
#        return KernelBase.avails[accel](spec, compile=compile, cache=cache,
#                                        profile=profile, debug=debug)
#
#    elif accel is None or isinstance(accel, (list, tuple)):
#
#        if accel is None:
#            accel = KernelBase.avails.keys()
#
#        errmsgs = []
#
#        for k in accel:
#            try:
#                kernel = KernelBase.avails[k](spec, compile=compile, cache=cache,
#                                                profile=profile, debug=debug)
#                return kernel
#
#            except Exception as err:
#                errmsgs.append(repr(err))
#
#        raise Exception("No kernel is available: %s" % "\n".join(errmsgs))
#
#    raise Exception("Kernel '%s' is not valid." % str(accel))
#
#
#def generate_compiler(compile):
#
#    clist = compile.split()
#
#    compcls = Compiler.from_path(clist[0])
#    comp = compcls(option=" ".join(clist[1:]))
#
#    return comp
#
#
#def get_compilers(kernel, compile=None):
#    """
#        parameters:
#
#        kernel: the kernel id or a list of them
#        compile: compiler path or compiler id, or a list of them
#                  syntax: "vendor|path [{default}] [additional options]"
#"""
#
#    kernels = []
#
#    if isinstance(kernel, str):
#        kernels.append((kernel, KernelBase.avails[kernel].lang))
#
#    elif isinstance(kernel, KernelBase):
#        kernels.append((kernel.name, kernel.lang))
#
#    elif isinstance(kernel, (list, tuple)):
#        for k in kernel:
#            if isinstance(k, str):
#                kernels.append((k, KernelBase.avails[k].lang))
#
#            elif isinstance(k, KernelBase):
#                kernels.append((k.name, k.lang))
#
#            else:
#                raise Exception("Unknown kernel type: %s" % str(k))
#
#    else:
#        raise Exception("Unknown kernel type: %s" % str(kernel))
#
#    compilers = []
#
#    if compile:
#        if isinstance(compile, str):
#            citems = compile.split()
#
#            if not citems:
#                raise Exception("Blank compile")
#
#            if os.path.isfile(citems[0]):
#                compilers.append(generate_compiler(compile))
#
#            else:
#                # TODO: vendor name search
#                for lang, langsubc in Compiler.avails.items():
#                    for kernel, kernelsubc in langsubc.items():
#                        for vendor, vendorsubc in kernelsubc.items():
#                            if vendor == citems[0]:
#                                try:
#                                    compilers.append(vendorsubc(option=" ".join(citems[1:])))
#                                except:
#                                    pass
#
#        elif isinstance(compile, Compiler):
#            compilers.append(compile)
#
#        elif isinstance(compile, (list, tuple)):
#
#            for comp in compile:
#                if isinstance(comp, str):
#                    citems = comp.split()
#
#                    if not citems:
#                        raise Exception("Blank compile")
#
#                    if os.path.isfile(citems[0]):
#                        try:
#                            compilers.append(generate_compiler(comp))
#                        except:
#                            pass
#
#                    else:
#                        # TODO: vendor name search
#                        for lang, langsubc in Compiler.avails.items():
#                            for kernel, kernelsubc in langsubc.items():
#                                for vendor, vendorsubc in kernelsubc.items():
#                                    if vendor == citems[0]:
#                                        try:
#                                            compilers.append(vendorsubc(option=" ".join(citems[1:])))
#                                        except:
#                                            pass
#
#                elif isinstance(comp, Compiler):
#                    compilers.append(comp)
#
#                else:
#                    raise Exception("Unsupported compiler type: %s" % str(comp))
#        else:
#            raise Exception("Unsupported compiler type: %s" % str(compile))
#
#    return_compilers = []
#    errmsgs = []
#
#
#    if compilers:
#        for comp in compilers:
#            if any(comp.accel==k[0] and comp.lang==k[1] for k in kernels):
#                return_compilers.append(comp)
#
#    elif compile is None:
#        for acc, lang in kernels:
#
#            if lang not in Compiler.avails:
#                continue
#
#            if acc not in Compiler.avails[lang]:
#                continue
#
#            vendors = Compiler.avails[lang][acc]
#
#            for vendor, cls in vendors.items():
#                try:
#                    return_compilers.append(cls())
#                except Exception as err:
#                    errmsgs.append(str(err))
#
#
#    if not return_compilers:
#        if errmsgs:
#            raise Exception("No compiler is found: %s" % "\n".join(errmsgs))
#        else:
#            raise Exception("No compiler is found: %s" % str(kernels))
#
#    return return_compilers
#
