import os 
import json
import shutil
from subprocess import PIPE, run
import sys

FILE_DIR_PATTERN = '.pdf'


def find_all_file_path(source):
    file_paths = []

    for root, dirs, files in os.walk(source):
        for file in files:
            if FILE_DIR_PATTERN in file.lower():
                path = os.path.join(source, file)
                file_paths.append(path)
        break
    
    return file_paths


def get_name_from_path_file(paths):
    new_names = []
    for path in paths:
        _ ,dir_name = os.path.split(path)
        if path not in new_names:
            new_names.append(dir_name)
    return new_names

def get_name_from_path(paths):
    new_names = []
    for path in paths:
        # _, dir_name = os.path.split(path)
        # new_dir_name = dir_name.replace(to_strip,"")
        _ ,dir_name = os.path.split(path)
        firstPart_dir_name = dir_name.split('-')[0]
        new_dir_name = firstPart_dir_name
        if new_dir_name not in new_names:
            new_names.append(new_dir_name)
    return new_names

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def create_dir_file(path):
    if not os.path.exists(path):
        os.mkdir(path)

def copy_and_overwrite(source, dest):
    # if os.path.exists(dest):
    #     shutil.rmtree(dest)
    shutil.copy(source, dest)


def make_json_metadata_file(path, game_dirs):
    data = {
        "fileNames" : game_dirs,
        'numberOfFiles' : len(game_dirs)
    }

    # We use with so as soon as the command is done. we close the file. 
    with open(path, 'w') as f:  
        json.dump(data, f)
    
def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)
    
    file_paths = find_all_file_path(source_path)
    # print(game_paths)
    new_file_dirs = get_name_from_path(file_paths)
    # print(new_file_dirs)
    
    new_names_for_files = get_name_from_path_file(file_paths)
    # print(new_names_for_files)
    
    create_dir(target_path)
 
    for src, dest in zip(file_paths, new_file_dirs):
        # destination_folder_name = dest.split(".pdf")[0]
        dest_path = os.path.join(target_path, dest)
        # copy_and_overwrite(src, dest_path)
        new_dir = create_dir(dest_path)



    for root, dirs, files in os.walk(target_path):
        for src, directory, new_names in zip(file_paths, dirs, new_names_for_files):
            if directory in new_names:
                new_file_names = os.path.join(target_path,directory, new_names)
                copy_and_overwrite(src, new_file_names)
    
    
    # json_path = os.path.join(target_path, 'metadata.json')
    # make_json_metadata_file(json_path, new_file_dirs)

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and a target")
    
    source, target = args[1:]
    main(source, target)