import os
import module.git as git
import module.toasts as toasts
import module.config as config


def get_uncommitted_message(git_path, root_path, repositories):
    message = "Uncommitted changes in:\n"
    for folder in repositories:
        path = os.path.join(root_path, folder)
        output, _ = git.uncommitted_files(git_path, path) 
        if output is not b'':
            message = message + folder + "\n"
    return message


def get_unpushed_message(git_path, root_path, repositories):
    message = "Unpushed commits in:\n"
    for folder in repositories:
        path = os.path.join(root_path, folder)
        output, _ = git.is_ahead_of_branch(git_path, path) 
        if output:
            message = message + folder + "\n"
    return message


if __name__ == '__main__':
    git_path, root_path = config.get_git_info()
    root_path = os.path.normpath(root_path) 
        
    repositories = []
    for item in os.listdir(root_path):
        path = os.path.join(root_path, item)
        if not os.path.isfile(path) and git.is_git_folder(git_path, path):
            repositories.append(item)

    uncommitted = get_uncommitted_message(git_path, root_path, repositories)
    unpushed = get_unpushed_message(git_path, root_path, repositories)
    
    if uncommitted.count('\n') <= 1: uncommitted = ""
    if unpushed.count('\n') <= 1: unpushed = ""

    message = uncommitted + unpushed
    toasts.toastMessage("Git-watch reminder", message)
    pass # end
