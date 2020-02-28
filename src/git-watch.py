import os
import sys
import time
import module.git as git
import module.config as config
import module.toasts as toasts
import PySimpleGUIWx as sg


__git__ = None
__root__ = None
__freq__ = None


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)    
    return os.path.join(os.path.abspath("."), relative_path)


def get_config_info():
    '''Get config information from config file'''
    global __git__, __root__, __freq__
    git_path, root_path, poll_frequency = config.get_git_info() 
    root_path = os.path.normpath(root_path) 
    if __git__ != git_path or __root__ != root_path or __freq__ != poll_frequency:
        print("Config data hot-reloaded")
        __git__ = git_path
        __root__ = root_path
        __freq__ = poll_frequency
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


def open_settings():
    '''Opens the config file in your favorite editor'''
    didopen = config.open_config_file()
    if not didopen:
        toasts.toastMessage("Error", "Could not open file: {}".format(config.__config_path__))



if __name__ == '__main__':
    wd = os.getcwd()

    # Load/set parameters
    icon = resource_path(os.path.join('src', 'assets', 'icon.ico'))
    menu_def = ['MENU', ['Open settings', 'Exit']]
    git_path, root_path, poll_frequency = get_config_info()

    # Start to system tray
    print("Starting git-watch (polling every {} seconds)".format(poll_frequency))
    tray = sg.SystemTray(menu=menu_def, filename=icon, tooltip="git-watch: running")
    tray.ShowMessage(title='git-watch', message='The application has started', time=500)
    
    # Main loop
    try:
        i = 0
        while True:
            # Reload config data
            os.chdir(wd)
            git_path, root_path, poll_frequency = get_config_info()
    
            # Read input from tray icon
            event = tray.Read(timeout=1000)

            # Handle tray input if needed
            if event == 'Exit': 
                break
            elif event == 'Open settings': 
                # Reset click is apparently needed
                tray.MenuItemChosen = sg.TIMEOUT_KEY
                tray.TaskBarIcon.menu_item_chosen = sg.TIMEOUT_KEY
                # Open settings if possible
                open_settings()
            else: 
                pass #tray.ShowMessage('Event', '{}'.format(event))

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
