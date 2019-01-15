import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Oleksii Build",
    options={"build_exe": {"includes":["header", "game_token", "inscriptions", "buttons"],
                           "packages":["pygame", "os", "sys", "random", "copy"],
                           "include_files":["HS.dat", "continue_data.dat", "background.jpg", "background_HS.jpg", "background_MM.jpg", "button_0.png", "button_0A.png", "button_1.png", "button_1A.png", "button_2.png", "button_2A.png", "button_3.png", "button_3A.png", "button_4.png", "button_4A.png", "button_5.png", "button_5A.png", "continue_butt.png", "Exit_butt.png", "start_butt.png"]}},
    executables = executables

    )