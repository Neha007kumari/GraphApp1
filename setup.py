from distutils.core import setup, Extension
setup(name='cycles',
        ext_modules=[
          Extension('cycles',
                    ['cycles.c'],
                    include_dirs = ['.'],
                    define_macros = [('FOO','1')],
                    undef_macros = ['BAR'],
                    library_dirs = ['/usr/local/lib'])])
