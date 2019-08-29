# -*- coding: utf-8 -*-
import os
from sorter.sorter import Sorter, RequestError


def getAmountElements(path: str) -> int:
        count_file = 0
        for file in os.listdir(path):
            full_name = os.path.join(path, file)
            if os.path.isfile(full_name):
                count_file += 1
            elif os.path.isdir(full_name):
                count_file += getAmountElements(full_name)
                
        return count_file