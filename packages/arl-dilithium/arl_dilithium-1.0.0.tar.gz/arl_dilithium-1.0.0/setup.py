import setuptools
from setuptools import setup, Extension

arl_dilithium_module = Extension('arl_dilithium',
                            sources = [
                                       'src/ntt.c',
                                       'src/packing.c',
                                       'src/poly.c',
                                       'src/polyvec.c',
                                       'src/reduce.c',
                                       'src/rounding.c',
                                       'src/sign.c',
                                       'src/symmetric-shake.c',
                                        'src/fips202.c',
                                        'src/randombytes.c',
                                        'src/module.c'
                                       ],

                            extra_compile_args=['-O2', '-funroll-loops', '-fomit-frame-pointer'],
                            include_dirs=['.','src'])

setup (name = 'arl_dilithium',
       version = '1.0.0',
       author_email = 'tidecoins@protonmail.com',
       author = 'likloadm',
       url = 'https://github.com/likloadm/arl_dilithium',
       description = 'Dilithium3 bindings for ArielCoin',
       package_dir={"": "src"},
       packages=setuptools.find_packages(where="src"),
       ext_modules = [arl_dilithium_module])
