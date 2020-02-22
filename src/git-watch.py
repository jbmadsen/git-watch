import os
import time
import module.git as git
import module.config as config
import module.toasts as toasts
import PySimpleGUIWx as sg


def get_config_info():
    '''Get config information from config file'''
    git_path, root_path, poll_frequency = config.get_git_info() 
    root_path = os.path.normpath(root_path) 
    return git_path, root_path, poll_frequency


def display_git_information(git_path, root_path):
    '''Get information for all repositories and display status for repositories not up to date
    
    git_path    -- path to the git executable (ignore if git is in PATH)
    root_path   -- root path of your repositories, e.g. ~/git/
    '''
    message = git.get_full_repo_status_messages(git_path, root_path)
    if message:
        toasts.toastMessage("Git-watch reminder", message)
        #tray.ShowMessage(title="Git-watch reminder", message=message, time=7000)


if __name__ == '__main__':
    # Load/set parameters
    icon = os.path.join(os.getcwd(), 'src', 'assets', 'icon.ico')
    menu_def = ['MENU', ['Settings', 'Exit']]
    git_path, root_path, poll_frequency = get_config_info()
    
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
                display_git_information(git_path, root_path)
                i = 0
            # Increment counter
            i = i + 1
    finally:
        tray.close()
        print("Program exited")
