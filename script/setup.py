from distutils.core import setup
import py2exe

import sys; sys.argv.append('py2exe')

py2exe_options = dict(
                      ascii=True,  # Exclude encodings
                      # excludes=['_ssl',  # Exclude _ssl
                                #'pyreadline', 'difflib', 'doctest', 
                                #'pickle', 'email'],  # Exclude standard library
                      dll_excludes=['msvcr71.dll', 'w9xpopen.exe'],  # Exclude msvcr71
                      compressed=True,  # Compress library.zip
                      )

setup(name='<Name>',
      version='1.0',
      description='<Control Volumen>',
      author='Marcos Trampal',

      console=['control-volumen.py'],
      options={'py2exe': py2exe_options},
      )