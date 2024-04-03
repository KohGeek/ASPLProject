import os
import shutil
import random

## get all files recursively in a directory with a specified keyword
def get_files(directory, keyword=None):

    files = []
    for root, directories, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    return [file for file in files if keyword in file]

## randomly pick a specified amount of files from a list
# based on the ratio provided, the files will be split into training and testing sets
# sets will not overlap
def random_pick(files, no_of_files, test_file_ratio):
    random.shuffle(files)
    files = files[:no_of_files]
    delimiter = int(len(files) * test_file_ratio)
    return files[delimiter:], files[:delimiter]

## copy files from a list to a specified directory
def copy_files(files, directory):
    x = 0
    
    if not os.path.exists(directory):
            os.makedirs(directory)

    for file in files:
        shutil.copy(file, directory)
        x += 1
        if x % 25 == 0 or x == len(files):
            print("Copied {} files. Last file copied was {}".format(x, file))

## main function
if __name__ == "__main__":
    source_directory = "C:\\Users\\KohCo\\Desktop\\FYP\\!ref - Sherlock"
    target_directory = "C:\\Users\\KohCo\\Desktop\\FYP\\Selected"

    keyword = "_1.jpg"
    test_file_ratio = 0.2

    # dict of source folders, target folders and no of files to be copied
    folders = {
        "1 - Good unit": ["good_unit", 500],
        "54 - MISSING DIE (PD)": ["missing_die", 100],
        "55 - DIE  PLACEMENT": ["die_placement", 500],
        "55 - Die Placement incorrect_ offset_ rotate": ["die_placement_incorrect", 90],
        "56 - Missing LED": ["missing_led", 90],
        "56- MISSING DIE (LED)": ["missing_die", 90],
        "72 - Missing Wire": ["missing_wire", 70],
        "76 - Unbonded Wire": ["unbonded_wire", 60]
    }

    for source_folder, target_folder in folders.items():
        actual_source_directory = os.path.join(source_directory, source_folder)
        
        print("Copying files from {} to {}, total files {}.".format(source_folder, target_folder[0], target_folder[1]))

        files = get_files(actual_source_directory, keyword)
        train_files, test_files = random_pick(files, target_folder[1], test_file_ratio)

        actual_target_directory = os.path.join(target_directory, "train", target_folder[0])
        print("Copying train files...")
        copy_files(train_files, actual_target_directory)

        actual_target_directory = os.path.join(target_directory, "test", target_folder[0])
        print("Copying test files...")
        copy_files(test_files, actual_target_directory)

        print("Done copying files from {} to {}.\n".format(source_folder, target_folder[0]))

        

