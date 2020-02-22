import os
import subprocess


def execute_command(git_path, command):
    '''Executes a git command in the terminal at specified path

    Keyword arguments:
    git_path                                            
        -- path to the git executable (ignore if git is in PATH)
    git-command list to execute, using subprocess.Popen()
        -- folder to execute git command at
    '''
    output = ""
    err = None

    wd = os.getcwd()
    os.chdir(git_path)
    
    try: 
        p = subprocess.Popen(command, stdout = subprocess.PIPE)
        output , err = p.communicate()  
    except Exception as e:
        err = str(e)

    os.chdir(wd)
    return output, err


def is_git_folder(git_path, path):
    '''Checks wether .git folder exists at specified path

    Keyword arguments:
    git_path    -- path to the git executable (ignore if git is in PATH)
    path        -- folder to execute git command at
    '''
    path = os.path.join(path, ".git")
    return os.path.isdir(path)


def uncommitted_files(git_path, path): 
    '''Gets the git status --porcelain from repository at specified path

    Keyword arguments:
    git_path    -- path to the git executable (ignore if git is in PATH)
    path        -- folder to execute git command at
    '''
    command = ["git", 
                "--git-dir=" + os.path.join(path, ".git"), 
                "--work-tree=" + path, 
                "status",
                "--porcelain"]

    output, err = execute_command(git_path, command)

    return output, err


def is_ahead_of_branch(git_path, path): 
    '''Gets the git status --branch --porcelain from repository at specified path

    Keyword arguments:
    git_path    -- path to the git executable (ignore if git is in PATH)
    path        -- folder to execute git command at
    '''
    command = ["git", 
                "--git-dir=" + os.path.join(path, ".git"), 
                "--work-tree=" + path, 
                "status",
                "--branch", 
                "--porcelain"]

    output, err = execute_command(git_path, command)
    output = b'ahead ' in output
    return output, err