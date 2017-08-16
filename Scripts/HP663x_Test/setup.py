from cx_Freeze import setup, Executable

base = None


executables = [Executable("HP663x_Test.py", base=base)]

packages = ["numpy", "matplotlib"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "<any name>",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)