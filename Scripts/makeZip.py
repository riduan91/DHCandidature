# -*- coding: utf-8 -*-
# module to put all files in a folder in a zip

import os       # for dealing with paths
import zipfile  # for compression
import sys
from fixtures import *

# compress a file or folder src into a compressed file dst
# Arguments(2):
#   - src: source file/folder
#   - dst: resulting compressed file
# return zip file's name

SOURCE_FOLDER = "../Docs/"
DESTINATION_FOLDER = "../Docsreduce/ZIPPER/"
REDUCED_TARGET = '../Docsreduce/'

def simply_prepare(path):
        if (not(os.path.exists(path))):
            print('Đang tạo thư mục %s' % path)
            os.mkdir(path)

        if (not(os.path.exists(path + 'ZIPPER'))):
            print('Đang tạo thư mục ZIPPER')
            os.mkdir(path + 'ZIPPER/')


def zip(src, dst):
    if (os.path.isdir(src)):
        print 'Creating zip for folder %s' % src
        zfname = "%s.zip" % (dst)
        zf = zipfile.ZipFile(zfname, "w")
        abs_src = os.path.abspath(src)
        for dirname, subdirs, files in os.walk(src):
            #files = [fi for fi in files if fi.endswith(".pdf")]     # filter pdfs
            files = [fi for fi in files]
            nb_file = len(files)
            count=1
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                print 'zipping %s \t------------> %d/%d' % (os.path.join(dirname, filename),
                                                            count, nb_file)
                zf.write(absname, arcname)
                count = count + 1
        zf.close()
        return zfname, src
    else:
        print '%s is not a folder. Nothing to do here !!' % src
        return None, src

if __name__ == '__main__':
    simply_prepare(REDUCED_TARGET)
    for school_code in SCHOOL_CODE.values():
        zip(SOURCE_FOLDER + school_code, DESTINATION_FOLDER + school_code)
        zip(SOURCE_FOLDER + "INTERVIEW/" + school_code, DESTINATION_FOLDER + school_code + "_INTERVIEW")
