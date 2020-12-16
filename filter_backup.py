from datetime import date
from calendar import monthrange
from re import search
from glob import glob
from os import remove
from os import path as osPath

class dateCheckUtil:
    def __init__(self, today_date=date.today(), last_n = 5):
        self.today_date = today_date
        self.last_n = last_n

    def is_saturday(self, date):
        return date.weekday() == 5

    def is_valid_saturday(self, date):
        day = self.today_date.weekday()
        if day == 5:
            saturday_distance = 28
        else:
            saturday_distance = ((day + 2) % 7) + 21

        date_difference = (self.today_date - date).days

        if self.is_saturday(date) and date_difference <= saturday_distance:
            return True
        else:
            return False

    def is_month_last_day(self, date):
        last_day = monthrange(date.year, date.month)[1]
        return last_day == date.day

    def is_last_n_days(self, date):
        return (self.today_date - date).days <= self.last_n

    def check_validity(self, date):
        #Probability of sat is high and probability of last few days is low
        return (self.is_month_last_day(date) or self.is_valid_saturday(date) or self.is_last_n_days(date))

class backupMaintain:
    def __init__(self, file_paths=None):
        if file_paths is None:
            self.file_paths = ['bucket1/', 'bucket2/']
        else:
            self.file_paths = file_paths

    def delete_unwanted(self):
        if self.file_paths is None:
            self.file_paths = ['bucket1/', 'bucket2/']

        for file_path in self.file_paths:
            list_of_files = [glob(file_path + "*.txt")][0]
            for file in list_of_files:
                filename = osPath.basename(file)
                #filter date
                date_from_file = str(search(r'(\d+-\d+-\d+)', filename).group(1))
                year, month, day = [int(var) for var in date_from_file.split('-')]
                param_date = date(year, month, day)
                util = dateCheckUtil(today_date=date(2020,9,18))
                if not util.check_validity(param_date):
                    remove(file)

operation_util = backupMaintain()
try:
    operation_util.delete_unwanted()
    print("Operation Done")
except:
    print("Error Occured")