import os
import program
import PySimpleGUIWx as sg


if __name__ == '__main__':
    # Load/set parameters
    icon = os.path.join(os.getcwd(), 'src', 'assets', 'icon.ico')
    menu_def = ['MENU', ['Settings', 'Exit']]
    git_path, root_path, poll_frequency = program.get_config_info()
    
    # Start to system tray
    print("Starting git-watch (polling every {} seconds)".format(poll_frequency))
    tray = sg.SystemTray(menu=menu_def, filename=icon, tooltip="git-watch: running")
    tray.ShowMessage(title='git-watch', message='The application has started', time=500)
    
    # Main loop
    try:
        i = 0
        while True:
            # Read input from tray icon
            event = tray.Read(timeout=1000)

            # Handle tray input if needed
            if event == 'Exit': break
            elif event == 'Settings': print("TODO") # TODO
            else: pass #tray.ShowMessage('Event', '{}'.format(event))

            # Displays git information if needed
            if i >= poll_frequency:
                print("Looking up git status")
                program.display_git_information(git_path, root_path)
                i = 0
            # Increment counter
            i = i + 1
    finally:
        tray.close()
        print("Program exited")
