import os
import time
import module.git as git
import module.config as config
import module.toasts as toasts


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


def watch_loop():
    '''Program main loop that fetches git information at regular intervals'''
    print('Starting git-watch...')
    git_path, root_path, poll_frequency = get_config_info()

    try:
        i = 0
        while True:
            if i >= poll_frequency:
                print('Fetching repository information...')
                display_git_information(git_path, root_path)
                i = 0
            time.sleep(1)  
            i = i + 1
    except KeyboardInterrupt:
        print('Ending git-watch...')


if __name__ == '__main__':
    watch_loop()
