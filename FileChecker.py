__author__ = "Khitsko Konstantin <khitsko.konstantin@gmail.com>"
__date__ = "14.03.2021"

from os import listdir
from os.path import isfile, join

class FileChecker:

    files = None

    directory = None

    def __init__(self, args):
        self.directory = args.directory

    def getFilesList(self):
        print("Try to get files in directory: {}".format(self.directory))
        self.files = [join(self.directory, f) for f in listdir(self.directory) if isfile(join(self.directory, f))]
        print("Directory {} contain {} files".format(self.directory,len(self.files)))
        return self.files

