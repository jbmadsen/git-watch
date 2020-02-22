import configparser


def get_git_info():
    '''Get git and repository root config information'''
    cfg = configparser.ConfigParser()
    cfg.read_file(open('./config.cfg'))

    git = cfg.get('GIT','PATH')
    root = cfg.get('SOURCE','PATH')
    freq = int(cfg.get('APPLICATION','POLL_FREQUENCY'))
    
    return git, root, freq
