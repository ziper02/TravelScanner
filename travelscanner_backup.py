import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from distutils.dir_util import copy_tree

from tqdm import tqdm

path_form = os.path.dirname(__file__)
path_to = os.path.dirname(__file__) + "\\..\\TravelScanner Backup\\{version}"


def backup():
    """
    save the data of project in TravelScanner Backup
    """
    folders_in_backup_folder = [dI for dI in os.listdir(os.path.dirname(__file__) + "\\..\\TravelScanner Backup")
                                if os.path.isdir(os.path.join(os.path.dirname(__file__) +
                                                              "\\..\\TravelScanner Backup", dI))]

    backup_folder = None

    today_str = datetime.today().strftime('%d%m%Y')
    if today_str not in folders_in_backup_folder:
        Path(path_to.format(version=today_str)).mkdir(parents=True, exist_ok=True)
        backup_folder = path_to.format(version=today_str)
    else:
        i = 1
        didnt_create = True
        today_str += "ver"
        while didnt_create:
            if not os.path.exists(path_to.format(version=(today_str + str(i)))):
                os.makedirs(path_to.format(version=(today_str + str(i))))
                backup_folder = path_to.format(version=(today_str + str(i)))
                didnt_create = False
            else:
                i += 1

    with open(os.path.dirname(__file__) + "\\backup dict.json", 'r', encoding='utf-8') as f:
        backup_list = json.load(f)

    if backup_folder is None:
        print('back up folder is not found')
        return

    backup_list = tqdm(backup_list)
    for backup_item in backup_list:
        backup_list.set_description(backup_item)
        if os.path.isdir(path_form + backup_item):
            copy_tree(path_form + backup_item, backup_folder + "\\" + backup_item)
        elif os.path.isfile(path_form + backup_item):
            shutil.copyfile(path_form + backup_item, backup_folder + "\\" + backup_item)


def restore(today_str=datetime.today().strftime('%d%m%Y')):
    """
    restore the latest backup
    :param today_str: the data of the latest backup that need to restore,by default its today
    :type today_str: str
    """
    folders_in_backup_folder = [dI for dI in os.listdir(os.path.dirname(__file__) + "\\..\\TravelScanner Backup")
                                if os.path.isdir(os.path.join(os.path.dirname(__file__) +
                                                              "\\..\\TravelScanner Backup", dI))]

    with open(os.path.dirname(__file__) + "\\backup dict.json", 'r', encoding='utf-8') as f:
        backup_list = json.load(f)

    if today_str not in folders_in_backup_folder:
        print("ERROR NO DATA FOLDER TO BACKUP")
    elif today_str in folders_in_backup_folder and today_str + "ver1" not in folders_in_backup_folder:
        backup_folder = path_to.format(version=today_str)
    else:
        didnt_found = True
        i = 1
        while didnt_found:
            if today_str + "ver" + str(i) in folders_in_backup_folder:
                backup_folder = path_to.format(version=today_str + "ver" + str(i))
                i += 1
            else:
                didnt_found = False
    backup_list = tqdm(backup_list)
    for backup_item in backup_list:
        backup_list.set_description(backup_item)
        if os.path.isdir(path_form + backup_item):
            shutil.rmtree(path_form + backup_item)
            copy_tree(backup_folder + "\\" + backup_item, path_form + backup_item)
        elif os.path.isfile(path_form + backup_item):
            os.remove(path_form + backup_item)
            shutil.copyfile(backup_folder + "\\" + backup_item, path_form + backup_item)
        else:
            print(f'{path_form + backup_item} is not found')
    print("FINISHED")


def update_data_for_test():
    data_project = path_form + "\\Data"
    data_updated_tests = path_form + "\\Tests\\Data Updated"
    shutil.rmtree(data_updated_tests)
    copy_tree(data_project, data_updated_tests)
    print("FINISHED")


if __name__ == "__main__":
    selection = input("Enter your selection: ")

    if selection == 'update':
        update_data_for_test()
    elif selection == 'backup':
        backup()
    elif selection == 'restore':
        restore()
    else:
        print("ERROR")
