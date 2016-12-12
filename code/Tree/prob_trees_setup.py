import os
import numpy

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

module = 'prob_trees'
ext = Extension(module, [module + '.pyx'],
                include_dirs=[numpy.get_include()],
                extra_compile_args=['-O2', '-march=native', '-mtune=native',
                                    '-funroll-loops', '-fpic', '-flto'])

setup(name=module, ext_modules=cythonize(ext))
