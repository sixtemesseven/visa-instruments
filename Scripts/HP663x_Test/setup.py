from cx_Freeze import setup, Executable

base = None


executables = [Executable("HP663x_Test.py", base=base)]

packages = ["simplevisa"]
options = {
    'build_exe': {
        'packages':packages,
    },

}

setup(
    name = "HP663x_Test",
    options = options,
    version = "18.08.2017.1",
    description = 'Small Test Script',
    executables = executables
)