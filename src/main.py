import os 
import sys
import subprocess 
import configparser
from win10toast import ToastNotifier


def git_status(git_path, root_path, folder_name): 
    '''Gets the git --porcelain status from repository at specified path

    Keyword arguments:
    git_path    -- path to the git executable (ignore if git is in PATH)
    root_path   -- path to the root folder containing all repos
    folder_name -- folder name to look for git changes
    '''
    output = ""
    err = None

    wd = os.getcwd()
    os.chdir(git_path)
    
    try: 
        root_path = os.path.normpath(root_path)
        path = os.path.join(root_path, folder_name)
        p = subprocess.Popen(["git", 
                              "--git-dir=" + os.path.join(path, ".git"), 
                              "--work-tree=" + path, 
                              "status", 
                              "--porcelain"], 
                              stdout = subprocess.PIPE)
        output , err = p.communicate()  
    except Exception as e:
        err = str(e)
    
    os.chdir(wd)
    return {"folder_name": folder_name, "output": output, "error": err}


if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read_file(open('./config.cfg'))

    git = cfg.get('GIT','PATH')
    root = cfg.get('SOURCE','PATH')

    toaster = ToastNotifier()

    repositories = []
    for item in os.listdir(root):
        if not os.path.isfile(os.path.join(root, item)):
            repositories.append(item)

    changes = []
    for folder in repositories:
        status = git_status(git, root, folder) 
        if status['output'] is not b'':
            changes.append(status)

    message = "in the following repositories:\n"

    for change in changes: 
        message = message + change['folder_name'] + "\n"
    
    toaster.show_toast("Git: Uncommitted changed",
                    message,
                    icon_path="src/assets/python.ico",
                    duration=15)
    
    pass # end
