import os
import module.git as git
import module.toasts as toasts
import module.config as config


if __name__ == '__main__':
    git_path, root_path = config.get_git_info()
    root_path = os.path.normpath(root_path) 
        
    repositories = []
    for item in os.listdir(root_path):
        path = os.path.join(root_path, item)
        if not os.path.isfile(path) and git.is_git_folder(git_path, path):
            repositories.append(item)

    changes = []
    for folder in repositories:
        path = os.path.join(root_path, folder)
        output, err = git.uncommitted_files(git_path, path) 
        if output is not b'':
            changes.append({'folder_name': folder, 'output': output})

    message = "in the following repositories:\n"

    for change in changes: 
        message = message + change['folder_name'] + "\n"
        print(change)
    
    toasts.toastMessage("Git: Uncommitted changed", message)
    pass # end
