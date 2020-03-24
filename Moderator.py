import platform
from enum import Enum

if platform.system() == 'Windows':
    add_for_folders = ''
else:
    add_for_folders = '/home/ubuntu/TravelScanner/'

destination_list = ["LOND", "PRAG", "BERL", "MUC", "ZRH", "BCN", "MAD", "AMS", "MAN",
                    "BUD", "GVA", "PARI", "BOJ", "VAR", "MILA", "SOF", "SKG", "DUB", "LIS", "BELI"]

depart_list = ["TLV"]

class set(Enum):
    train = 1
    validation = 2
    test = 3
