import cx_Freeze

executables = [cx_Freeze.Executable("snake.py")]
cx_Freeze.setup(
    name="Slither",
    options={"build_exe":{"packages":["pygame"], "include_files":["apple.png", "snake_head.png"]}},
    description = "Slither game tutorial",
    executables = executables
)
# python setup.py build
# python setup.py bdist_msi