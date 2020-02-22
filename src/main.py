import os
import time
import module.git as git
import module.toasts as toasts
import module.config as config


def display_git_information(git_path, root_path):
    '''Get information for all repositories and display status for repositories not up to date
    
    git_path    -- path to the git executable (ignore if git is in PATH)
    root_path   -- root path of your repositories, e.g. ~/git/
    '''
    message = git.get_full_repo_status_messages(git_path, root_path)
    if message:
        toasts.toastMessage("Git-watch reminder", message)


def main_loop():
    '''Program main loop that fetches git information at regular intervals'''
    print('Starting git-watch...')
    git_path, root_path = config.get_git_info()
    root_path = os.path.normpath(root_path) 

    try:
        i = 0
        while True:
            if i > 60:
                print('Fetching repository information...')
                display_git_information(git_path, root_path)
                i = 0
            time.sleep(1)  
            i = i + 1
    except KeyboardInterrupt:
        print('Ending program...')


if __name__ == '__main__':
    main_loop()
