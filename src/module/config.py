import os
import sys
import subprocess
import configparser


__config_path__ = 'config.cfg'


def find_config_file():
    # get current directory 
    wd = os.getcwd()
    # Set current dir to working dir
    os.chdir(wd)
    # return filename if exists
    if os.path.isfile(__config_path__):
        return os.path.join(os.getcwd(), __config_path__)
    # Set current dir to parent dir    
    parent_dir = os.path.abspath(os.path.join(__config_path__, os.pardir))
    os.chdir(parent_dir)
    # return filename if exists
    if os.path.isfile(__config_path__):
        return os.path.join(os.getcwd(), __config_path__)
    # Reset and return None
    os.chdir(wd)
    return None


def get_git_info():
    '''Get git and repository root config information'''
    # Locate file
    cfg = find_config_file()
    if cfg is None:
        raise FileNotFoundError("Config file: {} not found".format(__config_path__))
    # Open file
    with open(cfg) as fp:
        config = configparser.ConfigParser()
        config.readfp(fp)
    
        git = config.get('GIT','PATH')
        root = config.get('SOURCE','PATH')
        freq = int(config.get('APPLICATION','POLL_FREQUENCY'))
        
    return git, root, freq


def open_config_file():
    '''Opens the config file in your favorite editor, and returns True if file can be opened'''
    # Locate file
    cfg = find_config_file()
    if cfg is None:
        raise FileNotFoundError("Config file: {} not found".format(cfg))
    # Open file
    if sys.platform.startswith('darwin'):
        try:
            os.system('open "{0}"'.format(cfg))
        except Exception:
            return False
    elif os.name == 'nt':
        try:
            os.startfile(cfg)
        except OSError:
            # [Error 22] No application is associated with the specified file for this operation
            os.system("notepad.exe " + cfg)
        except Exception:
            return False
    elif os.name == 'posix':
        try:
            os.system('xdg-open "{0}"'.format(cfg)) 
        except Exception:
            return False
        # If all fails, try to use webbrowser
        
    return True
        
