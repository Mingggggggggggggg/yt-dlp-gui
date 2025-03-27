import cmd_command_use 
import gui
import settings

if __name__ == "__main__":
    cmd_command_use.updater()
    settings.initialize()
    gui.start_gui()