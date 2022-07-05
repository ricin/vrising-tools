from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': ['libcrypto','tkinter','email','pydoc_data','test','logging','unittest','concurrent','xml','xmlrpc','urllib','http','html']}

base = 'Console'

executables = [
    Executable('edit-vrising-name.py', base=base)
]

setup(name='Edit V Rising Character Name',
      version = '1.1',
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
