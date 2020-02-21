import os 
import sys
import subprocess 
import configparser


def git_status(git_path, repo_path): 
    '''Gets the git --porcelain status from repository at specified path

    Keyword arguments:
    git_path   -- path to the git executable (ignore if git is in PATH)
    repo_path  -- path to the repository
    '''
    output = ""
    err = ""

    wd = os.getcwd()
    os.chdir(git_path)
    
    try: 
        repo_path = os.path.normpath(repo_path)
        p = subprocess.Popen(["git", 
                              "--git-dir=" + os.path.join(repo_path, ".git"), 
                              "--work-tree=" + repo_path, 
                              "status", 
                              "--porcelain"], 
                              stdout = subprocess.PIPE)
        output , err = p.communicate()  
    except Exception as e:
        err = str(e)
    
    os.chdir(wd)
    return (output, err)


if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read_file(open('./config.cfg'))

    git = cfg.get('GIT','PATH')
    repos = cfg.get('REPOSITORY','PATH')
    
    status = git_status(git, repos) 
    print(status)
